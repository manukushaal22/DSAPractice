import type { ProblemDetail, ProblemSummary, RunEvent, SaveConflict } from "./types";

async function json<T>(response: Response): Promise<T> {
  if (!response.ok) {
    const body = await response.text();
    throw new Error(`${response.status} ${response.statusText}: ${body}`);
  }
  return (await response.json()) as T;
}

export async function fetchProblems(): Promise<ProblemSummary[]> {
  const data = await json<{ problems: ProblemSummary[] }>(await fetch("/api/problems"));
  return data.problems;
}

export async function fetchProblem(id: string): Promise<ProblemDetail> {
  return json<ProblemDetail>(await fetch(`/api/problems/${encodeURIComponent(id)}`));
}

export class SaveConflictError extends Error {
  constructor(public readonly conflict: SaveConflict) {
    super(conflict.message);
    this.name = "SaveConflictError";
  }
}

export async function saveSolution(
  id: string,
  code: string,
  baseMtime: string | null,
  force = false,
): Promise<{ saved: boolean; mtime: string | null }> {
  const response = await fetch(`/api/problems/${encodeURIComponent(id)}/solution`, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ code, baseMtime, force }),
  });
  if (response.status === 409) {
    const body = await response.json();
    throw new SaveConflictError(body.detail as SaveConflict);
  }
  return json(response);
}

/**
 * POST the buffer and invoke `onEvent` for each NDJSON line as it arrives.
 * Aborting the signal kills the server-side subprocess.
 */
export async function runSolution(
  id: string,
  code: string,
  onEvent: (event: RunEvent) => void,
  signal: AbortSignal,
): Promise<void> {
  const response = await fetch(`/api/problems/${encodeURIComponent(id)}/run`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ code }),
    signal,
  });

  if (!response.ok || !response.body) {
    throw new Error(`run failed: ${response.status} ${response.statusText}`);
  }

  const reader = response.body.getReader();
  const decoder = new TextDecoder();
  let buffer = "";

  const consume = (chunk: string) => {
    buffer += chunk;
    let newline = buffer.indexOf("\n");
    while (newline !== -1) {
      const line = buffer.slice(0, newline).trim();
      buffer = buffer.slice(newline + 1);
      if (line) {
        try {
          onEvent(JSON.parse(line) as RunEvent);
        } catch {
          onEvent({ type: "noise", text: line });
        }
      }
      newline = buffer.indexOf("\n");
    }
  };

  for (;;) {
    const { done, value } = await reader.read();
    if (done) break;
    consume(decoder.decode(value, { stream: true }));
  }
  consume(decoder.decode());
  // A final line with no trailing newline would otherwise be stranded.
  if (buffer.trim()) consume("\n");
}
