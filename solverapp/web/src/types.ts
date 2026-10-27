export type ProblemStatus = "todo" | "solved" | "revisit";

export interface LastRun {
  passed: number;
  total: number;
  verdict: string;
  at: string;
}

export interface ProblemSummary {
  id: string;
  slug: string;
  number: number;
  title: string;
  difficulty: string;
  topics: string[];
  status: ProblemStatus;
  statusDetail: string;
  complexity: string;
  solvedOn: string;
  isStub: boolean;
  track: "problems" | "learn";
  /** learn only: "01" */
  topic: string;
  /** learn only: "3", "3b" */
  rung: string;
  relDir: string;
  lastRun: LastRun | null;
}

export type TopicStatus = "upcoming" | "in-progress" | "complete";

export interface TopicSummary {
  id: string;
  number: number;
  title: string;
  folder: string;
  phase: string;
  needs: string[];
  startRung: number;
  related: string[];
  hasLesson: boolean;
  status: TopicStatus;
  required: number;
  requiredSolved: number;
  isCurrent: boolean;
  exercises: ProblemSummary[];
}

export interface TopicDetail extends TopicSummary {
  lesson: string;
}

export interface ProblemDetail extends ProblemSummary {
  readme: string;
  code: string;
  mtime: string | null;
}

export type CaseStatus = "pass" | "fail" | "error" | "tle" | "mle" | "stub";

export interface StartEvent {
  type: "start";
  total: number;
  function: string;
}

export interface CaseEvent {
  type: "case";
  index: number;
  name: string;
  isPerf: boolean;
  note: string | null;
  status: CaseStatus;
  elapsedMs: number;
  peakBytes: number;
  stdout: string;
  zombie: boolean;
  input: string;
  expected?: string;
  actual?: string;
  comparedByCmp?: boolean;
  expectedArgs?: string | null;
  actualArgs?: string | null;
  mutationOk?: boolean;
  error?: string;
  budget?: number | null;
}

export interface DoneEvent {
  type: "done";
  verdict: "pass" | "fail" | "stub";
  passed: number;
  total: number;
  failed: string[];
  totalMs: number;
  slowestMs: number;
  peakBytes: number;
  memorySupported: boolean;
}

export interface FatalEvent {
  type: "fatal";
  kind: "syntax" | "import" | "io" | "crash" | "usage" | "internal";
  message: string;
  line?: number;
  column?: number;
  text?: string;
  traceback?: string;
}

export interface NoiseEvent {
  type: "noise";
  text: string;
}

export type RunEvent = StartEvent | CaseEvent | DoneEvent | FatalEvent | NoiseEvent;

export interface SaveConflict {
  message: string;
  diskCode: string;
  mtime: string | null;
}
