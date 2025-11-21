import React from "react";
import Navbar from "./components/Navbar";
import TipPanel from "./components/TipPanel";
import "./styles/hud-background.css";

export default function App() {
    return (
        <div className="app-container">
            
            {/* HUD háttér */}
            <div className="hud-bg-wrapper">
                <div className="hud-grid"></div>
            </div>

            {/* NAVBAR */}
            <Navbar />

            {/* KÖZÉPSŐ PANEL */}
            <div className="main-content">
                <TipPanel />
            </div>
        </div>
    );
}
