import "./tipselector.css";

export default function TipSelector({ onSelect }) {
  return (
    <div className="tipselector-wrapper">
      <button className="tip-btn" onClick={() => onSelect("single")}>
        SINGLE TIPPEK
      </button>

      <button className="tip-btn" onClick={() => onSelect("kombi")}>
        KOMBI TIPPEK
      </button>

      <button className="tip-btn" onClick={() => onSelect("live")}>
        ÉLŐ TIPPEK
      </button>
    </div>
  );
}
