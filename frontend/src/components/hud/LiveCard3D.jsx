import React from "react";
import "./HologramFrame.css";

export default function LiveCard3D({ t }) {
    return (
        <div className="holo-card live">
            <div className="holo-border" />
            <div className="holo-inner">
                <div className="holo-title">{t.team1} – {t.team2}</div>
                <div className="holo-odds">Odds: {t.current_odds}</div>
                <div className="holo-strength">Live score: {t.live_strength}</div>
            </div>
        </div>
    );
}
