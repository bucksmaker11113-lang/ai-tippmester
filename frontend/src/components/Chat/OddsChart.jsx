import React from "react";
import { Line } from "react-chartjs-2";

export default function OddsChart({ history }) {

    const labels = history.map(h => h.timestamp);
    const odds = history.map(h => h.odds);

    const data = {
        labels,
        datasets: [
            {
                label: "Odds változás",
                data: odds,
                borderWidth: 3,
                tension: 0.3
            }
        ]
    };

    const options = {
        responsive: true,
        scales: {
            y: {
                beginAtZero: false
            }
        }
    };

    return (
        <div style={{ padding: "20px", background: "#020b18", borderRadius: "12px" }}>
            <Line data={data} options={options} />
        </div>
    );
}
