import React, { useEffect, useState } from "react";
import "./KombiPanel.css";
import { useParallax } from "../hooks/useParallax";

export default function KombiPanel() {

    const [kombi, setKombi] = useState(null);
    const { style, move, reset } = useParallax(9);

    useEffect(() => {
        async function load() {
            const res = await fetch("http://localhost:8000/kombi_tip", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ events: [] })
            });
            const data = await res.json();
            setKombi(data.kombi_tip);
        }
        load();
    }, []);

    if (!kombi) return <div className="kombi-empty">Nincs kombi ajánlat...</div>;

    return (
        <div className="kombi-card tip3d" style={style} onMouseMove={move} onMouseLeave={reset}>
            <h2 className="kombi-title">Kombi tipp</h2>

            {kombi.tips.map((t, i) => (
                <div className="kombi-item" key={i}>
                    <div className="kombi-match">{t.match}</div>
                    <div className="kombi-odds">Odds: {t.odds}</div>
                </div>
            ))}

            <div className="kombi-sum">Össz-odds: {kombi.combined_odds.toFixed(2)}</div>
            <div className="kombi-stake">Javasolt tét: {kombi.stake} Ft</div>
        </div>
    );
}
