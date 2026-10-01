/**
 * Bundle Monaco locally instead of letting @monaco-editor/react pull it from a CDN.
 *
 * This app runs offline on localhost, so a CDN dependency would mean the editor
 * silently fails to load without internet. Only the editor core and the Python
 * grammar are imported - pulling `monaco-editor` wholesale would drag in every
 * language it ships with.
 */
import { loader } from "@monaco-editor/react";
import * as monaco from "monaco-editor/esm/vs/editor/editor.api";
import "monaco-editor/esm/vs/editor/editor.all.js";
import "monaco-editor/esm/vs/basic-languages/python/python.contribution.js";
import EditorWorker from "monaco-editor/esm/vs/editor/editor.worker?worker";

self.MonacoEnvironment = {
  getWorker: () => new EditorWorker(),
};

loader.config({ monaco });

export default monaco;
