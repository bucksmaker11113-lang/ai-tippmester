import React, { useEffect, useState } from "react";
import { getSingleTips, getKombiTips, getLiveTips } from "../../services/api";
import { connectPush } from "../../services/push";

import SingleCard3D from "./SingleCard3D";
import KombiCard3D from "./KombiCard3D";
import LiveCard3D from "./LiveCard3D";

import "./HologramFrame.css";

export default function HUD3D() {

    const [single, setSingle] = useState([]);
    const [kombi, setKombi] = useState([]);
    const [live, setLive] = useState([]);

    const [flash, setFlash] = useState("");

    useEffect(() => {
        loadAll();

        const ws = connectPush((msg) => {
            console.log("PUSH:", msg);

            if (msg.type === "single") setFlash("single");
            if (msg.type === "kombi") setFlash("kombi");
            if (msg.type === "live") setFlash("live");

            setTimeout(() => setFlash(""), 2000);
            loadAll();
        });

        return () => ws.close();
    }, []);

    async function loadAll() {
        const s = await getSingleTips();
        const k = await getKombiTips();
        const l = await getLiveTips();

        setSingle(s?.tips || []);
        setKombi(k?.tips || []);
        setLive(l?.tips || []);
    }

    return (
        <div className={`hud-container ${flash}`}>
            <div className="hud-section">
                <h2 className="hud-title">Single tippek</h2>
                <div className="hud-row">
                    {single.map((t, i) => (
                        <SingleCard3D key={i} t={t} />
                    ))}
                </div>
            </div>

            <div className="hud-section">
                <h2 className="hud-title">Kombi tippek</h2>
                <div className="hud-row">
                    {kombi.map((t, i) => (
                        <KombiCard3D key={i} t={t} />
                    ))}
                </div>
            </div>

            <div className="hud-section">
                <h2 className="hud-title">Élő tippek</h2>
                <div className="hud-row">
                    {live.map((t, i) => (
                        <LiveCard3D key={i} t={t} />
                    ))}
                </div>
            </div>
        </div>
    );
}
