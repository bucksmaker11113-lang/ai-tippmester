import React, { useState } from "react";
import Navbar from "./components/Navbar";
import TipPanel from "./components/TipPanel";
import KombiPanel from "./components/KombiPanel";
import LivePanel from "./components/LivePanel";
import ChatPanel from "./components/ChatPanel";

import "./styles/hud-background.css";

export default function App() {

    const [currentPanel, setCurrentPanel] = useState("single");

    return (
        <div className="app-container">

            {/* HUD background */}
            <div className="hud-bg-wrapper">
                <div className="hud-grid"></div>
            </div>

            {/* NAVBAR */}
            <Navbar onSelectPanel={setCurrentPanel} />

            {/* MAIN CONTENT */}
            <div className="main-content">
                {currentPanel === "single" && <TipPanel />}
                {currentPanel === "kombi" && <KombiPanel />}
                {currentPanel === "live" && <LivePanel />}
                {currentPanel === "chat" && <ChatPanel />}
            </div>

        </div>
    );
}
