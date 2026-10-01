"""Process memory sampling and time/memory limit enforcement.

Cross-platform, standard library only. Used by the harness to abort runaway
solutions instead of waiting on them without bound.
"""

from __future__ import annotations

import ctypes
import os
import sys
import threading
import time
import traceback
from typing import Any, Callable, Optional, Sequence


class LimitExceeded(BaseException):
    """Base for injected aborts.

    Deliberately derives from BaseException, not Exception, so that a bare
    ``except Exception`` inside a solution cannot swallow the abort.
    """


class TimeLimitExceeded(LimitExceeded):
    pass


class MemoryLimitExceeded(LimitExceeded):
    pass


# --------------------------------------------------------------------------
# memory sampling
# --------------------------------------------------------------------------


def _make_windows_sampler() -> Optional[Callable[[], Optional[int]]]:
    try:
        kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
    except Exception:
        return None

    class PROCESS_MEMORY_COUNTERS(ctypes.Structure):
        _fields_ = [
            ("cb", ctypes.c_ulong),
            ("PageFaultCount", ctypes.c_ulong),
            ("PeakWorkingSetSize", ctypes.c_size_t),
            ("WorkingSetSize", ctypes.c_size_t),
            ("QuotaPeakPagedPoolUsage", ctypes.c_size_t),
            ("QuotaPagedPoolUsage", ctypes.c_size_t),
            ("QuotaPeakNonPagedPoolUsage", ctypes.c_size_t),
            ("QuotaNonPagedPoolUsage", ctypes.c_size_t),
            ("PagefileUsage", ctypes.c_size_t),
            ("PeakPagefileUsage", ctypes.c_size_t),
        ]

    get_info = None
    for source, name in (
        (kernel32, "K32GetProcessMemoryInfo"),
        (None, "GetProcessMemoryInfo"),
    ):
        try:
            lib = source if source is not None else ctypes.WinDLL("psapi")
            get_info = getattr(lib, name)
            break
        except Exception:
            continue
    if get_info is None:
        return None

    # Without explicit signatures ctypes truncates the 64-bit pseudo-handle and
    # the call silently fails.
    get_info.argtypes = [
        ctypes.c_void_p,
        ctypes.POINTER(PROCESS_MEMORY_COUNTERS),
        ctypes.c_ulong,
    ]
    get_info.restype = ctypes.c_int
    kernel32.GetCurrentProcess.restype = ctypes.c_void_p
    kernel32.GetCurrentProcess.argtypes = []

    handle = kernel32.GetCurrentProcess()
    counters = PROCESS_MEMORY_COUNTERS()
    counters.cb = ctypes.sizeof(PROCESS_MEMORY_COUNTERS)
    size = ctypes.c_ulong(ctypes.sizeof(PROCESS_MEMORY_COUNTERS))
    ref = ctypes.byref(counters)

    def sample() -> Optional[int]:
        # PagefileUsage is private committed bytes: it counts memory the process
        # asked for even if the pages have not all been touched yet.
        try:
            if not get_info(handle, ref, size):
                return None
        except Exception:
            return None
        return int(counters.PagefileUsage)

    return sample


def _make_linux_sampler() -> Optional[Callable[[], Optional[int]]]:
    path = "/proc/self/statm"
    if not os.path.exists(path):
        return None
    page = os.sysconf("SC_PAGE_SIZE")

    def sample() -> Optional[int]:
        try:
            with open(path, "rb") as fh:
                fields = fh.read().split()
            return int(fields[1]) * page  # resident pages
        except Exception:
            return None

    return sample


def _make_rusage_sampler() -> Optional[Callable[[], Optional[int]]]:
    try:
        import resource
    except ImportError:
        return None

    # ru_maxrss is kilobytes on Linux, bytes on macOS.
    scale = 1 if sys.platform == "darwin" else 1024

    def sample() -> Optional[int]:
        return int(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss) * scale

    return sample


def _pick_sampler() -> Optional[Callable[[], Optional[int]]]:
    candidates = (
        [_make_windows_sampler]
        if os.name == "nt"
        else [_make_linux_sampler, _make_rusage_sampler]
    )
    for factory in candidates:
        try:
            sampler = factory()
        except Exception:
            continue
        if sampler is None:
            continue
        try:
            probe = sampler()
        except Exception:
            continue
        if isinstance(probe, int) and probe > 0:
            return sampler
    return None


sample_memory = _pick_sampler()
MEMORY_SUPPORTED = sample_memory is not None


# --------------------------------------------------------------------------
# abort injection
# --------------------------------------------------------------------------


def _async_raise(thread_id: int, exctype: type) -> bool:
    """Ask CPython to raise ``exctype`` inside the given thread.

    The exception lands at the next bytecode boundary, so a thread parked in a
    long C-level call (a single huge ``sorted()``, say) keeps running until that
    call returns. Callers must treat this as best-effort.
    """
    try:
        set_exc = ctypes.pythonapi.PyThreadState_SetAsyncExc
    except AttributeError:
        return False
    set_exc.argtypes = (ctypes.c_ulong, ctypes.py_object)
    try:
        affected = set_exc(ctypes.c_ulong(thread_id), ctypes.py_object(exctype))
    except Exception:
        return False
    if affected > 1:  # should never happen; undo to stay safe
        set_exc(ctypes.c_ulong(thread_id), ctypes.py_object(0))
        return False
    return affected == 1


INJECTION_SUPPORTED = hasattr(ctypes, "pythonapi") and hasattr(
    ctypes.pythonapi, "PyThreadState_SetAsyncExc"
)

MIN_POLL = 0.002
MAX_POLL = 0.05
GRACE_SECONDS = 1.0


class Outcome:
    """Result of one guarded call."""

    __slots__ = ("status", "value", "elapsed_ms", "peak_bytes", "error", "zombie")

    def __init__(self) -> None:
        self.status = "ok"  # ok | error | stub | timeout | memory
        self.value: Any = None
        self.elapsed_ms = 0.0
        self.peak_bytes = 0
        self.error: Optional[str] = None
        self.zombie = False


def call_with_limits(
    func: Callable[..., Any],
    args: Sequence[Any],
    kwargs: dict,
    time_limit_s: Optional[float],
    memory_limit_b: Optional[int],
) -> Outcome:
    """Call ``func`` on a worker thread, aborting it if it blows a limit."""

    outcome = Outcome()

    if not INJECTION_SUPPORTED or (time_limit_s is None and memory_limit_b is None):
        return _call_direct(func, args, kwargs, outcome)

    box: dict = {}

    def target() -> None:
        started = time.perf_counter()
        try:
            box["value"] = func(*args, **kwargs)
            box["status"] = "ok"
        except NotImplementedError:
            box["status"] = "stub"
        except LimitExceeded:
            box["status"] = "aborted"
        except BaseException:
            box["status"] = "error"
            box["error"] = traceback.format_exc()
        finally:
            box["ms"] = (time.perf_counter() - started) * 1000

    worker = threading.Thread(target=target, daemon=True, name="dsakit-case")

    baseline = sample_memory() if sample_memory else None
    peak_delta = 0
    verdict: Optional[str] = None
    poll = MIN_POLL

    started = time.perf_counter()
    worker.start()

    while True:
        worker.join(poll)
        if not worker.is_alive():
            break

        if sample_memory is not None and baseline is not None:
            current = sample_memory()
            if current is not None:
                peak_delta = max(peak_delta, current - baseline)
                if memory_limit_b is not None and peak_delta > memory_limit_b:
                    verdict = "memory"
                    break

        if time_limit_s is not None and (time.perf_counter() - started) > time_limit_s:
            verdict = "timeout"
            break

        poll = min(MAX_POLL, poll * 1.5)

    if verdict is not None:
        exctype = TimeLimitExceeded if verdict == "timeout" else MemoryLimitExceeded
        if worker.ident is not None:
            _async_raise(worker.ident, exctype)
        worker.join(GRACE_SECONDS)
        outcome.status = verdict
        outcome.zombie = worker.is_alive()
        outcome.elapsed_ms = (time.perf_counter() - started) * 1000
        outcome.peak_bytes = max(peak_delta, 0)
        return outcome

    outcome.elapsed_ms = box.get("ms", (time.perf_counter() - started) * 1000)
    outcome.peak_bytes = max(peak_delta, 0)
    status = box.get("status", "error")
    if status == "ok":
        outcome.value = box.get("value")
    elif status == "stub":
        outcome.status = "stub"
    elif status == "aborted":
        # The abort landed just as the worker was finishing; treat as a limit hit.
        outcome.status = verdict or "timeout"
    else:
        outcome.status = "error"
        outcome.error = box.get("error") or "unknown error"
    return outcome


def _call_direct(func, args, kwargs, outcome: Outcome) -> Outcome:
    """Fallback path when limits are off or exception injection is unavailable."""
    started = time.perf_counter()
    try:
        outcome.value = func(*args, **kwargs)
    except NotImplementedError:
        outcome.status = "stub"
    except BaseException:
        outcome.status = "error"
        outcome.error = traceback.format_exc()
    outcome.elapsed_ms = (time.perf_counter() - started) * 1000
    return outcome
