import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    proxy: {
      "/api": {
        target: "http://127.0.0.1:8000",
        changeOrigin: true,
        // The run endpoint streams NDJSON; buffering it would defeat the point.
        configure: (proxy) => {
          proxy.on("proxyRes", (proxyRes) => {
            proxyRes.headers["cache-control"] = "no-cache, no-transform";
          });
        },
      },
    },
  },
  build: {
    outDir: "dist",
    emptyOutDir: true,
    // Monaco is a few MB. That is irrelevant over localhost, and splitting it into
    // its own chunk keeps the app chunk small and cacheable across rebuilds.
    chunkSizeWarningLimit: 4000,
    rollupOptions: {
      output: {
        manualChunks(id) {
          if (id.includes("node_modules/monaco-editor")) return "monaco";
          return undefined;
        },
      },
    },
  },
});
