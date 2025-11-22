import React from "react";
import "./HologramFrame.css";

export default function KombiCard3D({ t }) {
    return (
        <div className="holo-card kombi">
            <div className="holo-border" />
            <div className="holo-inner">
                <div className="holo-title">{t.team1} – {t.team2}</div>
                <div className="holo-odds">Odds: {t.tippmix_odds}</div>
                <div className="holo-strength">Erősség: {t.strength}</div>
            </div>
        </div>
    );
}
