import React, { useState } from "react";
import "./ChatPanel.css";
import { useParallax } from "../hooks/useParallax";

export default function ChatPanel() {

    const [messages, setMessages] = useState([]);
    const [input, setInput] = useState("");

    const { style, move, reset } = useParallax(8);

    function sendMessage() {
        if (!input.trim()) return;
        setMessages([...messages, { text: input, self: true }]);
        setInput("");
    }

    return (
        <div className="chat-wrapper">
            <div className="chat-title">Tippmester AI – Élő Chat</div>

            <div className="chat-box" style={style} onMouseMove={move} onMouseLeave={reset}>
                {messages.map((msg, i) => (
                    <div key={i} className={`chat-msg ${msg.self ? "self" : "ai"}`}>
                        {msg.text}
                    </div>
                ))}
            </div>

            <div className="chat-input-area">
                <input
                    className="chat-input"
                    value={input}
                    onChange={(e) => setInput(e.target.value)}
                    placeholder="Írj valamit az AI-nak..."
                />
                <button className="chat-send" onClick={sendMessage}>Küldés</button>
            </div>
        </div>
    );
}
