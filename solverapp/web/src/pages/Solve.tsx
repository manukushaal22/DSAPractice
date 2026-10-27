import { useCallback, useEffect, useRef, useState } from "react";
import { Link, useParams } from "react-router-dom";

import { fetchProblem, runSolution, SaveConflictError, saveSolution } from "../api";
import CodeEditor from "../components/CodeEditor";
import MarkdownPane from "../components/MarkdownPane";
import ResultsPanel from "../components/ResultsPanel";
import SplitPane from "../components/SplitPane";
import type { CaseEvent, DoneEvent, FatalEvent, ProblemDetail } from "../types";

const SUGGESTIONS_KEY = "lcp.editor.suggestions";

export default function Solve() {
  const { problemId = "" } = useParams();

  const [problem, setProblem] = useState<ProblemDetail | null>(null);
  const [loadError, setLoadError] = useState<string | null>(null);

  const [code, setCode] = useState("");
  const [savedCode, setSavedCode] = useState("");
  const [mtime, setMtime] = useState<string | null>(null);
  const [conflict, setConflict] = useState<string | null>(null);
  const [notice, setNotice] = useState<string | null>(null);

  const [running, setRunning] = useState(false);
  const [cases, setCases] = useState<CaseEvent[]>([]);
  const [done, setDone] = useState<DoneEvent | null>(null);
  const [fatal, setFatal] = useState<FatalEvent | null>(null);
  const [runError, setRunError] = useState<string | null>(null);
  const [total, setTotal] = useState<number | null>(null);

  const [suggestions, setSuggestions] = useState(
    () => window.localStorage.getItem(SUGGESTIONS_KEY) === "on",
  );

  const abortRef = useRef<AbortController | null>(null);
  const codeRef = useRef(code);
  codeRef.current = code;

  useEffect(() => {
    let cancelled = false;
    fetchProblem(problemId)
      .then((detail) => {
        if (cancelled) return;
        setProblem(detail);
        setCode(detail.code);
        setSavedCode(detail.code);
        setMtime(detail.mtime);
      })
      .catch((err: Error) => !cancelled && setLoadError(err.message));
    return () => {
      cancelled = true;
    };
  }, [problemId]);

  useEffect(() => {
    window.localStorage.setItem(SUGGESTIONS_KEY, suggestions ? "on" : "off");
  }, [suggestions]);

  // Kill any in-flight run when leaving the page.
  useEffect(() => () => abortRef.current?.abort(), []);

  useEffect(() => {
    if (problem) document.title = `${problem.id} — ${problem.title}`;
  }, [problem]);

  const stop = useCallback(() => {
    abortRef.current?.abort();
    abortRef.current = null;
    setRunning(false);
  }, []);

  const run = useCallback(async () => {
    if (abortRef.current) return; // already running
    const controller = new AbortController();
    abortRef.current = controller;

    setRunning(true);
    setCases([]);
    setDone(null);
    setFatal(null);
    setRunError(null);
    setTotal(null);
    setNotice(null);

    try {
      await runSolution(
        problemId,
        codeRef.current,
        (event) => {
          switch (event.type) {
            case "start":
              setTotal(event.total);
              break;
            case "case":
              setCases((previous) => [...previous, event]);
              break;
            case "done":
              setDone(event);
              break;
            case "fatal":
              setFatal(event);
              break;
            case "noise":
              break;
          }
        },
        controller.signal,
      );
    } catch (err) {
      if ((err as Error).name !== "AbortError") {
        setRunError((err as Error).message);
      }
    } finally {
      abortRef.current = null;
      setRunning(false);
    }
  }, [problemId]);

  const save = useCallback(
    async (force = false) => {
      setConflict(null);
      try {
        const result = await saveSolution(problemId, codeRef.current, mtime, force);
        setMtime(result.mtime);
        setSavedCode(codeRef.current);
        setNotice("Saved to solution.py");
        window.setTimeout(() => setNotice(null), 2500);
      } catch (err) {
        if (err instanceof SaveConflictError) {
          setConflict(err.conflict.message);
        } else {
          setRunError((err as Error).message);
        }
      }
    },
    [problemId, mtime],
  );

  useEffect(() => {
    const onKeyDown = (event: KeyboardEvent) => {
      if ((event.ctrlKey || event.metaKey) && event.key === "Enter") {
        event.preventDefault();
        void run();
      } else if ((event.ctrlKey || event.metaKey) && event.key.toLowerCase() === "s") {
        event.preventDefault();
        void save();
      } else if (event.key === "Escape" && abortRef.current) {
        event.preventDefault();
        stop();
      }
    };
    window.addEventListener("keydown", onKeyDown);
    return () => window.removeEventListener("keydown", onKeyDown);
  }, [run, save, stop]);

  if (loadError) {
    return (
      <div className="centered">
        {loadError} — <Link to="/">back to the list</Link>
      </div>
    );
  }
  if (!problem) return <div className="centered">Loading…</div>;

  const dirty = code !== savedCode;
  const backTo = problem.track === "learn" ? `/learn/${problem.topic}` : "/";

  return (
    <div className="solve-page">
      <div className="solve-header">
        <Link
          className="back"
          to={backTo}
          title={problem.track === "learn" ? "Back to the topic" : "Back to problems"}
        >
          ←
        </Link>
        <span className="pid">{problem.id}</span>
        <h2>{problem.title}</h2>
        <span className={`badge ${problem.difficulty.toLowerCase()}`}>{problem.difficulty}</span>
        <span className={`badge ${problem.status}`}>{problem.status}</span>
        <span className="spacer" />
        {notice && <span style={{ color: "var(--green)", fontSize: 12 }}>{notice}</span>}
        <span className="hint">Ctrl+Enter run · Ctrl+S save · Esc stop</span>
        <button onClick={() => void save()} disabled={!dirty}>
          {dirty ? "Save" : "Saved"}
        </button>
        {running ? (
          <button className="danger" onClick={stop}>
            Stop
          </button>
        ) : (
          <button className="primary" onClick={() => void run()}>
            Run
          </button>
        )}
      </div>

      {conflict && (
        <div className="banner warn">
          <span>
            {conflict}. Someone (probably you, in VS Code) edited it after this tab opened.
          </span>
          <span className="spacer" />
          <button
            onClick={() => {
              void save(true);
            }}
          >
            Overwrite anyway
          </button>
          <button
            onClick={() => {
              void fetchProblem(problemId).then((detail) => {
                setCode(detail.code);
                setSavedCode(detail.code);
                setMtime(detail.mtime);
                setConflict(null);
              });
            }}
          >
            Reload from disk
          </button>
        </div>
      )}

      <SplitPane
        direction="horizontal"
        initial={44}
        storageKey="lcp.split.main"
        first={
          <>
            <div className="pane-title">Description</div>
            <MarkdownPane source={problem.readme} baseDir={problem.relDir} />
          </>
        }
        second={
          <SplitPane
            direction="vertical"
            initial={62}
            storageKey="lcp.split.editor"
            first={
              <>
                <div className="pane-title">
                  <span>solution.py</span>
                  {dirty && <span style={{ color: "var(--yellow)" }}>● unsaved</span>}
                  <span className="spacer" />
                  <label title="Off by default: this repo disables autocomplete while practising">
                    <input
                      type="checkbox"
                      checked={suggestions}
                      onChange={(event) => setSuggestions(event.target.checked)}
                    />
                    suggestions
                  </label>
                </div>
                <div style={{ flex: 1, minHeight: 0 }}>
                  <CodeEditor
                    value={code}
                    onChange={setCode}
                    onRun={() => void run()}
                    onSave={() => void save()}
                    suggestions={suggestions}
                  />
                </div>
              </>
            }
            second={
              <>
                <div className="pane-title">Test results</div>
                <ResultsPanel
                  running={running}
                  cases={cases}
                  done={done}
                  fatal={fatal}
                  error={runError}
                  total={total}
                />
              </>
            }
          />
        }
      />
    </div>
  );
}
