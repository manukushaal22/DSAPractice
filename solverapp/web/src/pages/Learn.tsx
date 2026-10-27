import { useEffect, useMemo, useState } from "react";
import { Link } from "react-router-dom";

import { fetchTopics } from "../api";
import NavTabs from "../components/NavTabs";
import type { ProblemSummary, TopicSummary } from "../types";

export function ProgressBar({ done, total }: { done: number; total: number }) {
  const percent = total ? Math.round((100 * done) / total) : 0;
  return (
    <span className="progress" title={`${done} of ${total} required rungs solved`}>
      <span className="progress-track">
        <span className="progress-fill" style={{ width: `${percent}%` }} />
      </span>
      <span className="progress-label">
        {done}/{total}
      </span>
    </span>
  );
}

export function TopicStatusBadge({ topic }: { topic: TopicSummary }) {
  if (topic.isCurrent && topic.status !== "complete") {
    return <span className="badge current">current</span>;
  }
  return <span className={`badge ${topic.status}`}>{topic.status.replace("-", " ")}</span>;
}

/** The first exercise of a topic that is not solved yet, if any. */
export function nextExercise(topic: TopicSummary): ProblemSummary | undefined {
  return topic.exercises.find((exercise) => exercise.status !== "solved");
}

export default function Learn() {
  const [topics, setTopics] = useState<TopicSummary[] | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchTopics()
      .then(setTopics)
      .catch((err: Error) => setError(err.message));
  }, []);

  const phases = useMemo(() => {
    const grouped = new Map<string, TopicSummary[]>();
    for (const topic of topics ?? []) {
      const phase = topic.phase || "Other";
      grouped.set(phase, [...(grouped.get(phase) ?? []), topic]);
    }
    return [...grouped.entries()];
  }, [topics]);

  if (error) {
    return (
      <div className="centered">
        Could not reach the API: {error}
        <br />
        Is <code>serve.py</code> running?
      </div>
    );
  }
  if (!topics) return <div className="centered">Loading the learning path…</div>;

  const byId = new Map(topics.map((topic) => [topic.id, topic]));
  const core = topics.filter((topic) => topic.phase !== "Stretch");
  const complete = core.filter((topic) => topic.status === "complete").length;
  const current = topics.find((topic) => topic.isCurrent);
  const upNext = current && nextExercise(current);

  return (
    <div className="list-page">
      <header>
        <NavTabs />
        <h1>Learning path</h1>
        <div className="subtitle">
          {complete} of {core.length} core topics complete · each topic is a lesson plus a
          ladder of exercises, read live from <code>learn/</code>
        </div>
      </header>

      {current && (
        <div className="continue-card">
          <div>
            <div className="eyebrow">Current topic</div>
            <Link className="continue-title" to={`/learn/${current.id}`}>
              {current.id} · {current.title}
            </Link>
            <div className="continue-meta">
              <ProgressBar done={current.requiredSolved} total={current.required} />
            </div>
          </div>
          <span className="spacer" />
          {upNext ? (
            <Link className="button primary" to={`/p/${upNext.id}`}>
              Continue: {upNext.id} {upNext.title} →
            </Link>
          ) : (
            <span className="continue-hint">
              No open exercise. Ask the agent for the <b>next rung</b>.
            </span>
          )}
        </div>
      )}

      {phases.map(([phase, phaseTopics]) => (
        <section key={phase} className="phase">
          <h2>
            {phase}
            {phase === "Stretch" && <span className="phase-note"> · scheduled only on request</span>}
          </h2>
          <table className="problem-table topic-table">
            <thead>
              <tr>
                <th className="num">#</th>
                <th>Topic</th>
                <th>Progress</th>
                <th>Status</th>
                <th>Starts at</th>
                <th>Needs</th>
                <th>Related drill</th>
              </tr>
            </thead>
            <tbody>
              {phaseTopics.map((topic) => (
                <tr key={topic.id} className={topic.isCurrent ? "current-row" : undefined}>
                  <td className="num">{topic.id}</td>
                  <td className="title">
                    {topic.hasLesson || topic.exercises.length ? (
                      <Link to={`/learn/${topic.id}`}>{topic.title}</Link>
                    ) : (
                      <span className="dim-title">{topic.title}</span>
                    )}
                  </td>
                  <td>
                    <ProgressBar done={topic.requiredSolved} total={topic.required} />
                  </td>
                  <td>
                    <TopicStatusBadge topic={topic} />
                  </td>
                  <td className="mono">.{topic.startRung}</td>
                  <td>
                    {topic.needs.length ? (
                      topic.needs.map((need) => (
                        <span
                          key={need}
                          className={`chip ${byId.get(need)?.status === "complete" ? "met" : ""}`}
                          title={byId.get(need)?.title}
                        >
                          {need}
                        </span>
                      ))
                    ) : (
                      <span className="none">—</span>
                    )}
                  </td>
                  <td>
                    {topic.related.length ? (
                      topic.related.map((pid) => (
                        <Link key={pid} className="chip link" to={`/p/${pid}`}>
                          {pid}
                        </Link>
                      ))
                    ) : (
                      <span className="none">—</span>
                    )}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </section>
      ))}
    </div>
  );
}
