import React, { useState, useEffect } from "react";
import OddsChart from "./OddsChart";

export default function OddsHistoryPanel({ eventName, onClose }) {
    const [history, setHistory] = useState([]);

    useEffect(() => {
        load();
        const id = setInterval(load, 5000);
        return () => clearInterval(id);
    }, []);

    async function load() {
        const res = await fetch(`/api/odds/history/${eventName}`);
        const data = await res.json();
        setHistory(data.history);
    }

    return (
        <div className="odds-overlay">
            <button onClick={onClose} className="close-btn">X</button>
            <h2 style={{ color: "#00eaff" }}>Odds History – {eventName}</h2>
            <OddsChart history={history} />
        </div>
    );
}
