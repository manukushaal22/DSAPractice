import { useEffect, useState } from "react";
import { Link, useParams } from "react-router-dom";

import { fetchTopic } from "../api";
import { difficultyClass, LastRunCell } from "../components/badges";
import MarkdownPane from "../components/MarkdownPane";
import NavTabs from "../components/NavTabs";
import type { TopicDetail } from "../types";
import { nextExercise, ProgressBar, TopicStatusBadge } from "./Learn";

export default function Topic() {
  const { topicId = "" } = useParams();
  const [topic, setTopic] = useState<TopicDetail | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let cancelled = false;
    setTopic(null);
    fetchTopic(topicId)
      .then((detail) => !cancelled && setTopic(detail))
      .catch((err: Error) => !cancelled && setError(err.message));
    return () => {
      cancelled = true;
    };
  }, [topicId]);

  useEffect(() => {
    if (topic) document.title = `${topic.id} — ${topic.title}`;
  }, [topic]);

  if (error) {
    return (
      <div className="centered">
        {error} — <Link to="/learn">back to the learning path</Link>
      </div>
    );
  }
  if (!topic) return <div className="centered">Loading…</div>;

  const upNext = nextExercise(topic);

  return (
    <div className="list-page">
      <header>
        <NavTabs />
        <div className="topic-heading">
          <Link className="back-link" to="/learn" title="Back to the learning path">
            ← Learning path
          </Link>
          <h1>
            <span className="topic-num">{topic.id}</span> {topic.title}
          </h1>
          <div className="subtitle topic-meta">
            <TopicStatusBadge topic={topic} />
            <ProgressBar done={topic.requiredSolved} total={topic.required} />
            <span>
              {topic.phase} · starts at rung .{topic.startRung} · rungs .{topic.startRung}–.5
              required, .6 optional
            </span>
          </div>
        </div>
      </header>

      <h2 className="section-title">Ladder</h2>
      {topic.exercises.length ? (
        <table className="problem-table">
          <thead>
            <tr>
              <th className="num">ID</th>
              <th>Exercise</th>
              <th>Rung</th>
              <th>Difficulty</th>
              <th>Status</th>
              <th>Last run</th>
            </tr>
          </thead>
          <tbody>
            {topic.exercises.map((exercise) => (
              <tr
                key={exercise.id}
                className={exercise.id === upNext?.id ? "current-row" : undefined}
              >
                <td className="num">{exercise.id}</td>
                <td className="title">
                  <Link to={`/p/${exercise.id}`}>{exercise.title}</Link>
                </td>
                <td className="mono">.{exercise.rung}</td>
                <td>
                  <span className={`badge ${difficultyClass(exercise.difficulty)}`}>
                    {exercise.difficulty}
                  </span>
                </td>
                <td>
                  <span className={`badge ${exercise.status}`} title={exercise.statusDetail}>
                    {exercise.status}
                  </span>
                </td>
                <td className="lastrun">
                  <LastRunCell run={exercise.lastRun} />
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      ) : (
        <p className="empty-note">
          No exercises yet. Ask the agent to <b>start topic {topic.id}</b>.
        </p>
      )}
      {topic.exercises.length > 0 && !upNext && topic.status !== "complete" && (
        <p className="empty-note">
          Every exercise so far is solved. Ask the agent for the <b>next rung</b>.
        </p>
      )}

      <h2 className="section-title">Lesson</h2>
      {topic.lesson ? (
        <div className="lesson-panel">
          <MarkdownPane source={topic.lesson} baseDir={`learn/${topic.folder}`} />
        </div>
      ) : (
        <p className="empty-note">
          The lesson is written when the topic starts. Ask the agent to{" "}
          <b>start topic {topic.id}</b>.
        </p>
      )}
    </div>
  );
}
