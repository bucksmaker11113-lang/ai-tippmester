import React from "react";
import ChatPanel from "./components/ChatPanel";
import "./styles/global.css";

export default function App() {
  return (
    <div className="app-container">
      <header className="app-header">
        <h1>⚡ Tippmester AI 5.3 – Vision–Fusion Edition</h1>
        <p className="subtitle">A mesterséges intelligencia, ami lát, ért és számol 💚</p>
      </header>

      <main className="app-main">
        <ChatPanel />
      </main>

      <footer className="app-footer">
        <small>© {new Date().getFullYear()} Tippmester AI · Fusion Engine Connected</small>
      </footer>
    </div>
  );
}
