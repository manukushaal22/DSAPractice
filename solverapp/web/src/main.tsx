import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import { createBrowserRouter, RouterProvider } from "react-router-dom";

import "./monaco-setup";
import ProblemList from "./pages/ProblemList";
import Solve from "./pages/Solve";
import "./styles.css";

const router = createBrowserRouter([
  { path: "/", element: <ProblemList /> },
  { path: "/p/:problemId", element: <Solve /> },
  { path: "*", element: <ProblemList /> },
]);

createRoot(document.getElementById("root")!).render(
  <StrictMode>
    <RouterProvider router={router} />
  </StrictMode>,
);
