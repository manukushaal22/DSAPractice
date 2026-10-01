import { useCallback, useEffect, useRef, useState, type ReactNode } from "react";

interface Props {
  direction: "horizontal" | "vertical";
  /** Initial size of the first pane, as a percentage of the container. */
  initial: number;
  min?: number;
  max?: number;
  storageKey?: string;
  first: ReactNode;
  second: ReactNode;
}

function readStored(key: string | undefined, fallback: number): number {
  if (!key) return fallback;
  const raw = window.localStorage.getItem(key);
  const parsed = raw === null ? NaN : Number(raw);
  return Number.isFinite(parsed) ? parsed : fallback;
}

/** Two panes with a draggable gutter. Position persists per storageKey. */
export default function SplitPane({
  direction,
  initial,
  min = 15,
  max = 85,
  storageKey,
  first,
  second,
}: Props) {
  const containerRef = useRef<HTMLDivElement>(null);
  const [percent, setPercent] = useState(() => readStored(storageKey, initial));
  const [dragging, setDragging] = useState(false);

  useEffect(() => {
    if (storageKey) window.localStorage.setItem(storageKey, String(percent));
  }, [percent, storageKey]);

  const onPointerMove = useCallback(
    (event: PointerEvent) => {
      const container = containerRef.current;
      if (!container) return;
      const rect = container.getBoundingClientRect();
      const ratio =
        direction === "horizontal"
          ? (event.clientX - rect.left) / rect.width
          : (event.clientY - rect.top) / rect.height;
      setPercent(Math.min(max, Math.max(min, ratio * 100)));
    },
    [direction, min, max],
  );

  useEffect(() => {
    if (!dragging) return;
    const stop = () => setDragging(false);
    window.addEventListener("pointermove", onPointerMove);
    window.addEventListener("pointerup", stop);
    // Without this the iframe-less Monaco canvas still eats the cursor mid-drag.
    const previous = document.body.style.cursor;
    document.body.style.cursor = direction === "horizontal" ? "col-resize" : "row-resize";
    document.body.style.userSelect = "none";
    return () => {
      window.removeEventListener("pointermove", onPointerMove);
      window.removeEventListener("pointerup", stop);
      document.body.style.cursor = previous;
      document.body.style.userSelect = "";
    };
  }, [dragging, onPointerMove, direction]);

  const firstStyle = direction === "horizontal"
    ? { width: `${percent}%` }
    : { height: `${percent}%` };

  return (
    <div ref={containerRef} className={`split ${direction === "vertical" ? "vertical" : ""}`}>
      <div className="split-pane" style={firstStyle}>
        {first}
      </div>
      <div
        className={`gutter ${direction} ${dragging ? "dragging" : ""}`}
        onPointerDown={(event) => {
          event.preventDefault();
          setDragging(true);
        }}
        onDoubleClick={() => setPercent(initial)}
        role="separator"
        aria-orientation={direction === "horizontal" ? "vertical" : "horizontal"}
      />
      <div className="split-pane" style={{ flex: 1 }}>
        {second}
      </div>
    </div>
  );
}
