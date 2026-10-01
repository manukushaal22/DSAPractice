import { useState } from "react";

import type { CaseEvent, CaseStatus, DoneEvent, FatalEvent } from "../types";

const VERDICT_LABEL: Record<CaseStatus, string> = {
  pass: "PASS",
  fail: "FAIL",
  error: "ERR",
  tle: "TLE",
  mle: "MLE",
  stub: "TODO",
};

function formatMemory(bytes: number): string | null {
  if (bytes < 1024 * 1024) return null;
  return `${(bytes / (1024 * 1024)).toFixed(1)} MB`;
}

function Row({ label, value, className }: { label: string; value: string; className?: string }) {
  return (
    <div className="row">
      <span className="key">{label}</span>
      <span className={`val ${className ?? ""}`}>{value}</span>
    </div>
  );
}

function CaseRow({ event, defaultOpen }: { event: CaseEvent; defaultOpen: boolean }) {
  const [open, setOpen] = useState(defaultOpen);
  const memory = formatMemory(event.peakBytes);
  const hasDetail =
    event.status !== "pass" || Boolean(event.stdout) || Boolean(event.note);

  return (
    <div className={`case ${event.status}`}>
      <div className="case-head" onClick={() => hasDetail && setOpen(!open)}>
        <span className="verdict">{VERDICT_LABEL[event.status]}</span>
        <span className="idx">{event.index}</span>
        <span className="name">{event.name}</span>
        <span className="timing">
          {event.elapsedMs.toFixed(2)} ms{memory ? ` · ${memory}` : ""}
        </span>
        <span className="chev">{hasDetail ? (open ? "▾" : "▸") : ""}</span>
      </div>

      {open && hasDetail && (
        <div className="case-body">
          {event.status === "stub" && (
            <div className="note">
              solution.py is still a stub — implement the function, then run again.
            </div>
          )}

          {event.status !== "stub" && <Row label="input" value={event.input} />}

          {event.status === "fail" && (
            <>
              {event.mutationOk === false ? null : (
                <>
                  <Row label="expected" value={event.expected ?? ""} className="expected" />
                  <Row label="actual" value={event.actual ?? ""} className="actual" />
                </>
              )}
              {event.mutationOk === false && (
                <>
                  <Row
                    label="args after"
                    value={event.expectedArgs ?? ""}
                    className="expected"
                  />
                  <Row label="but were" value={event.actualArgs ?? ""} className="actual" />
                </>
              )}
              {event.comparedByCmp && (
                <div className="note">
                  Compared with the suite's custom comparator — more than one answer may be
                  valid here.
                </div>
              )}
            </>
          )}

          {(event.status === "tle" || event.status === "mle") && (
            <div className="note">
              {event.status === "tle"
                ? `Exceeded the ${event.budget ?? "?"} ms budget — aborted after ${event.elapsedMs.toFixed(0)} ms. Too slow for this input size; re-read "Target complexity".`
                : `Exceeded the ${event.budget ?? "?"} MB budget — peaked at ${memory ?? "?"}. Allocating far more than the input warrants: look for copies, slices, or tables built inside a loop.`}
            </div>
          )}

          {event.status === "error" && event.error && (
            <pre className="trace">{event.error}</pre>
          )}

          {event.note && <div className="note">note: {event.note}</div>}

          {event.stdout && (
            <>
              <div className="row">
                <span className="key">stdout</span>
              </div>
              <pre className="stdout">{event.stdout.replace(/\n$/, "")}</pre>
            </>
          )}

          {event.zombie && (
            <div className="zombie">
              This case did not stop immediately after being aborted — it was stuck inside a
              long C-level call. It has been abandoned and dies with the run.
            </div>
          )}
        </div>
      )}
    </div>
  );
}

function FatalBox({ event }: { event: FatalEvent }) {
  const title =
    event.kind === "syntax"
      ? "Syntax error"
      : event.kind === "import"
        ? "Could not load your code"
        : "Runner failed";
  return (
    <div className="fatal">
      <h4>{title}</h4>
      <div className="where">
        {event.message}
        {event.line ? ` (line ${event.line}${event.column ? `, col ${event.column}` : ""})` : ""}
      </div>
      {event.text && <pre>{event.text}</pre>}
      {event.traceback && <pre>{event.traceback}</pre>}
    </div>
  );
}

interface Props {
  running: boolean;
  cases: CaseEvent[];
  done: DoneEvent | null;
  fatal: FatalEvent | null;
  error: string | null;
  total: number | null;
}

export default function ResultsPanel({ running, cases, done, fatal, error, total }: Props) {
  const nothingYet = !running && !cases.length && !done && !fatal && !error;

  if (nothingYet) {
    return (
      <div className="results">
        <div className="empty">
          Press <kbd>Ctrl</kbd> + <kbd>Enter</kbd> or hit <b>Run</b> to execute the full test
          suite against the code in the editor. Your <code>solution.py</code> on disk is not
          touched unless you press <b>Save</b>.
        </div>
      </div>
    );
  }

  const failed = cases.filter((c) => c.status !== "pass").length;
  const passed = cases.filter((c) => c.status === "pass").length;

  let barClass = "running";
  let barText = `running… ${cases.length}${total ? ` / ${total}` : ""}`;
  if (done) {
    barClass = done.verdict;
    barText =
      done.verdict === "stub"
        ? "solution is still a stub"
        : `${done.passed}/${done.total} passed`;
  } else if (error || fatal) {
    barClass = "fail";
    barText = "run did not complete";
  } else if (!running) {
    barClass = failed ? "fail" : "running";
    barText = `stopped after ${cases.length}${total ? ` / ${total}` : ""} — ${passed} passed`;
  }

  return (
    <div className="results">
      <div className={`summary-bar ${barClass}`}>
        <span>{barText}</span>
        {done && (
          <span className="metrics">
            total {done.totalMs.toFixed(2)} ms · slowest {done.slowestMs.toFixed(2)} ms
            {formatMemory(done.peakBytes) ? ` · peak ${formatMemory(done.peakBytes)}` : ""}
          </span>
        )}
      </div>

      {error && (
        <div className="fatal">
          <h4>Request failed</h4>
          <div className="where">{error}</div>
        </div>
      )}
      {fatal && <FatalBox event={fatal} />}

      {cases.map((event) => (
        <CaseRow
          key={event.index}
          event={event}
          defaultOpen={event.status !== "pass"}
        />
      ))}
    </div>
  );
}
