import React, { useEffect, useState } from "react";
import "./LivePanel.css";
import { useParallax } from "../hooks/useParallax";

export default function LivePanel() {

    const [live, setLive] = useState(null);
    const { style, move, reset } = useParallax(10);

    useEffect(() => {
        async function load() {
            const res = await fetch("http://localhost:8000/live_tip", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    match: "Live API Match",
                    odds: 2.10,
                    live_stats: { pressure: 0.8, attacks: 14 }
                })
            });
            const data = await res.json();
            setLive(data.live_tip);
        }
        load();
    }, []);

    if (!live) return <div className="live-empty">Nincs élő ajánlat…</div>;

    return (
        <div className="live-card tip3d" style={style} onMouseMove={move} onMouseLeave={reset}>
            <div className="live-title">{live.match}</div>
            <div className="live-odds">Odds: {live.odds}</div>
            <div className="live-stake">Tét: {live.stake} Ft</div>
            <div className="live-section">Goal chance: {Math.round(live.goal_chance * 100)}%</div>
            <div className="live-section">Confidence: {Math.round(live.confidence * 100)}%</div>
        </div>
    );
}
