import React, { useEffect, useState } from "react";

export default function TipList() {
  const [tips, setTips] = useState([]);

  useEffect(() => {
    // Mock tippek – backendhez API fetch csatlakoztatható
    setTips([
      { match: "Liverpool – Arsenal", pick: "1", odds: 2.35, confidence: 0.78 },
      { match: "Real Madrid – Barcelona", pick: "X", odds: 3.25, confidence: 0.65 },
      { match: "Ferencváros – Újpest", pick: "1", odds: 1.85, confidence: 0.84 },
      { match: "Boston – LA Lakers", pick: "2", odds: 2.75, confidence: 0.71 }
    ]);
  }, []);

  return (
    <div className="tiplist">
      <h2>🎯 Napi Tippajánlatok</h2>
      {tips.map((t, i) => (
        <div key={i} className="tip-card">
          <h3>{t.match}</h3>
          <p><strong>Tipp:</strong> {t.pick} &nbsp;|&nbsp; <strong>Odds:</strong> {t.odds}</p>
          <div className="confidence-bar">
            <div className="fill" style={{ width: `${t.confidence * 100}%` }}></div>
          </div>
        </div>
      ))}
    </div>
  );
}
