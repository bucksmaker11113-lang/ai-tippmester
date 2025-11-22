import React, { useEffect, useState } from "react";
import "./TipPanel.css";
import { useParallax } from "../hooks/useParallax";
import { Football3D, Basketball3D, Hockey3D, Tennis3D } from "./icons/SportIcons3D";

export default function TipPanel() {

    const [tips, setTips] = useState([]);
    const { style, move, reset } = useParallax(10);

    async function loadTips() {
        try {
            const res = await fetch("http://localhost:8000/single_tips", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ events: [] })
            });

            const data = await res.json();
            setTips(data.single_tips || []);
        } catch (err) {
            console.error("Error loading tips:", err);
        }
    }

    useEffect(() => { loadTips(); }, []);

    const getIcon = (sport) => {
        switch (sport) {
            case "foci": return <Football3D />;
            case "kosar": return <Basketball3D />;
            case "hok": return <Hockey3D />;
            case "tenisz": return <Tennis3D />;
            default: return null;
        }
    };

    return (
        <div className="tip-panel-wrapper">
            <h2 className="tip-title">Mai ajánlott tippek</h2>

            <div className="tip-list">
                {tips.map((t, i) => (
                    <div key={i}
                        className="tip-card tip3d"
                        style={style}
                        onMouseMove={move}
                        onMouseLeave={reset}
                    >
                        <div className="tip-icon">{getIcon(t.sport)}</div>
                        <div className="tip-info">
                            <div className="tip-match">{t.match}</div>
                            <div className="tip-odds">Odds: {t.odds}</div>
                            <div className="tip-stake">Tét: {t.stake} Ft</div>
                        </div>
                    </div>
                ))}
            </div>
        </div>
    );
}
