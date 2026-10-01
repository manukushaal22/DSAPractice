import Editor, { type OnMount } from "@monaco-editor/react";
import { useRef } from "react";

interface Props {
  value: string;
  onChange: (value: string) => void;
  onRun: () => void;
  onSave: () => void;
  /** Word-based suggestions are off by default: this repo deliberately disables
   *  autocomplete while practising (see .vscode/settings.json). */
  suggestions: boolean;
}

export default function CodeEditor({ value, onChange, onRun, onSave, suggestions }: Props) {
  const runRef = useRef(onRun);
  const saveRef = useRef(onSave);
  runRef.current = onRun;
  saveRef.current = onSave;

  const handleMount: OnMount = (editor, monaco) => {
    editor.addCommand(monaco.KeyMod.CtrlCmd | monaco.KeyCode.Enter, () => runRef.current());
    editor.addCommand(monaco.KeyMod.CtrlCmd | monaco.KeyCode.KeyS, () => saveRef.current());
    editor.focus();
  };

  return (
    <Editor
      height="100%"
      defaultLanguage="python"
      theme="vs-dark"
      value={value}
      onChange={(next) => onChange(next ?? "")}
      onMount={handleMount}
      options={{
        fontSize: 13.5,
        fontFamily: '"Cascadia Code", Consolas, "SF Mono", Menlo, monospace',
        fontLigatures: true,
        minimap: { enabled: false },
        scrollBeyondLastLine: false,
        renderWhitespace: "selection",
        tabSize: 4,
        insertSpaces: true,
        rulers: [88],
        automaticLayout: true,
        padding: { top: 12, bottom: 12 },
        smoothScrolling: true,
        bracketPairColorization: { enabled: true },
        quickSuggestions: suggestions,
        suggestOnTriggerCharacters: suggestions,
        wordBasedSuggestions: suggestions ? "currentDocument" : "off",
        parameterHints: { enabled: suggestions },
        tabCompletion: suggestions ? "on" : "off",
      }}
    />
  );
}
