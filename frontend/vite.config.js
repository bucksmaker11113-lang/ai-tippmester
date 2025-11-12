import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

// Railway / Render kompatibilis beállítás
export default defineConfig({
  plugins: [react()],
  server: {
    host: "0.0.0.0",
    port: 5173,
  },
  build: {
    outDir: "dist",
  },
});
