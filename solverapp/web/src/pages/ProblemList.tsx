import { useEffect, useMemo, useState } from "react";
import { Link } from "react-router-dom";

import { fetchProblems } from "../api";
import { difficultyClass, LastRunCell } from "../components/badges";
import NavTabs from "../components/NavTabs";
import type { ProblemSummary } from "../types";

export default function ProblemList() {
  const [problems, setProblems] = useState<ProblemSummary[] | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [query, setQuery] = useState("");
  const [hideSolved, setHideSolved] = useState(false);

  useEffect(() => {
    fetchProblems()
      .then(setProblems)
      .catch((err: Error) => setError(err.message));
  }, []);

  const visible = useMemo(() => {
    if (!problems) return [];
    const needle = query.trim().toLowerCase();
    return problems.filter((problem) => {
      if (hideSolved && problem.status === "solved") return false;
      if (!needle) return true;
      const haystack = [
        problem.id,
        problem.title,
        problem.difficulty,
        problem.status,
        ...problem.topics,
      ]
        .join(" ")
        .toLowerCase();
      return haystack.includes(needle);
    });
  }, [problems, query, hideSolved]);

  if (error) {
    return (
      <div className="centered">
        Could not reach the API: {error}
        <br />
        Is <code>serve.py</code> running?
      </div>
    );
  }
  if (!problems) return <div className="centered">Loading problems…</div>;

  const solved = problems.filter((p) => p.status === "solved").length;

  return (
    <div className="list-page">
      <header>
        <NavTabs />
        <h1>DSA Practice</h1>
        <div className="subtitle">
          {problems.length} problems · {solved} solved · the mixed interview drill, read live
          from <code>problems/</code>, so a new folder shows up on refresh
        </div>
      </header>

      <div className="toolbar">
        <input
          type="search"
          placeholder="Filter by title, topic, difficulty or status…"
          value={query}
          onChange={(event) => setQuery(event.target.value)}
        />
        <label style={{ display: "flex", alignItems: "center", gap: 6, color: "var(--text-dim)" }}>
          <input
            type="checkbox"
            checked={hideSolved}
            onChange={(event) => setHideSolved(event.target.checked)}
          />
          hide solved
        </label>
        <button onClick={() => fetchProblems().then(setProblems).catch(() => undefined)}>
          Refresh
        </button>
      </div>

      <table className="problem-table">
        <thead>
          <tr>
            <th className="num">#</th>
            <th>Problem</th>
            <th>Difficulty</th>
            <th>Topics</th>
            <th>Status</th>
            <th>Last run</th>
          </tr>
        </thead>
        <tbody>
          {visible.map((problem) => (
            <tr key={problem.id}>
              <td className="num">{problem.id}</td>
              <td className="title">
                <Link to={`/p/${problem.id}`}>{problem.title}</Link>
              </td>
              <td>
                <span className={`badge ${difficultyClass(problem.difficulty)}`}>
                  {problem.difficulty}
                </span>
              </td>
              <td className="topics">
                {problem.topics.map((topic) => (
                  <span className="topic" key={topic}>
                    {topic}
                  </span>
                ))}
              </td>
              <td>
                <span className={`badge ${problem.status}`} title={problem.statusDetail}>
                  {problem.status}
                </span>
              </td>
              <td className="lastrun">
                <LastRunCell run={problem.lastRun} />
              </td>
            </tr>
          ))}
          {!visible.length && (
            <tr>
              <td colSpan={6} style={{ color: "var(--text-faint)", padding: "22px 12px" }}>
                Nothing matches that filter.
              </td>
            </tr>
          )}
        </tbody>
      </table>
    </div>
  );
}
