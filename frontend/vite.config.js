import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

// Tippmester Quantum Engine - frontend Vite config
export default defineConfig({
  plugins: [react()],

  server: {
    host: "0.0.0.0",
    port: 5173,

    // Backend API & WebSocket proxy
    proxy: {
      "/api": {
        target: "http://127.0.0.1:8000",
        changeOrigin: true,
        secure: false,
      },
      "/ws": {
        target: "ws://127.0.0.1:8000",
        ws: true,
        secure: false,
      },
    },
  },

  build: {
    sourcemap: false,
    chunkSizeWarningLimit: 800,
    outDir: "dist",
  },

  resolve: {
    alias: {
      "@": "/src",
    },
  },
});
