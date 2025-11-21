// frontend/src/components/HUD3D/Panels/TipPanel3D.jsx
import "./tippanel.css";

export default function TipPanel3D({ mode, onClose }) {
  if (!mode) return null;

  const title =
    mode === "single"
      ? "SINGLE TIPPEK"
      : mode === "kombi"
      ? "KOMBI TIPPEK"
      : "ÉLŐ TIPPEK";

  return (
    <div className="tippanel-wrapper">
      <div className="tippanel-glow"></div>

      <div className="tippanel">
        {/* HEADER */}
        <div className="tippanel-header">
          <h2>{title}</h2>
          <button className="tippanel-close" onClick={onClose}>X</button>
        </div>

        {/* ALL 3 SECTIONS */}
        <div className="tippanel-sections">

          {/* A) TIPP LISTA */}
          <div className="tippanel-block">
            <h3 className="panel-label">TIPP LISTA</h3>
            <div className="panel-content">
              <p className="loading">Betöltés...</p>
            </div>
          </div>

          {/* B) AI ELEMZÉS */}
          <div className="tippanel-block">
            <h3 className="panel-label">AI ELEMZÉS</h3>
            <div className="panel-content">
              <p className="loading">Elemzés folyamatban...</p>
            </div>
          </div>

          {/* D) BANKROLL ADATOK */}
          <div className="tippanel-block">
            <h3 className="panel-label">BANKROLL ADATOK</h3>
            <div className="panel-content">
              <p className="loading">Bankroll adatlekérés...</p>
            </div>
          </div>

        </div>
      </div>
    </div>
  );
}
