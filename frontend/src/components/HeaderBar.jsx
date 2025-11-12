import React from "react";

export default function HeaderBar({ onToggleChat }) {
  return (
    <header className="header-bar">
      <h1 className="logo">💚 Tippmester 5.2</h1>
      <button className="chat-toggle" onClick={onToggleChat}>
        💬 Chat
      </button>
    </header>
  );
}
