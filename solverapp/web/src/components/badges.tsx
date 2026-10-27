import type { LastRun } from "../types";

export function difficultyClass(difficulty: string): string {
  const key = difficulty.trim().toLowerCase();
  return ["easy", "medium", "hard"].includes(key) ? key : "unknown";
}

export function LastRunCell({ run }: { run: LastRun | null }) {
  if (!run) return <span className="none">—</span>;
  if (run.verdict === "stub") return <span className="none">stub</span>;
  const ok = run.verdict === "pass";
  return (
    <span className={ok ? "ok" : "bad"} title={`last run ${run.at.replace("T", " ")}`}>
      {run.passed}/{run.total} {ok ? "✓" : "✗"}
    </span>
  );
}
