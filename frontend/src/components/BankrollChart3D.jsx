import React from "react";
import { LineChart, Line, CartesianGrid, XAxis, YAxis, Tooltip } from "recharts";

const data = [
  { day: "H", value: 300000 },
  { day: "K", value: 302000 },
  { day: "Sze", value: 306500 },
  { day: "Cs", value: 308000 },
  { day: "P", value: 312500 },
];

export default function BankrollChart3D() {
  return (
    <div className="bankroll-chart">
      <h2>📈 Bankroll alakulása</h2>
      <LineChart width={400} height={220} data={data}>
        <Line type="monotone" dataKey="value" stroke="#00ff99" strokeWidth={3} />
        <CartesianGrid stroke="#333" />
        <XAxis dataKey="day" />
        <YAxis />
        <Tooltip />
      </LineChart>
    </div>
  );
}
