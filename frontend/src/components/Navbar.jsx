import React from "react";
import "./Navbar.css";

export default function Navbar({ onSelectPanel }) {
    return (
        <nav className="nav3d">

            <div className="nav-title">Tippmester Quantum Engine</div>

            <div className="nav-links">
                <button className="nav-btn" onClick={() => onSelectPanel("single")}>Single</button>
                <button className="nav-btn" onClick={() => onSelectPanel("kombi")}>Kombi</button>
                <button className="nav-btn" onClick={() => onSelectPanel("live")}>Élő</button>
                <button className="nav-btn" onClick={() => onSelectPanel("chat")}>Chat</button>
            </div>

        </nav>
    );
}
