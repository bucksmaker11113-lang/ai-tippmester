import "./chatpanel.css";

export default function ChatPanelHUD() {
  return (
    <div className="chatpanel-wrapper">
      <div className="chat-header">CHAT</div>

      <div className="chat-body">
        <p style={{ color: "#11cfff" }}>Csatlakozás...</p>
      </div>

      <input
        className="chat-input"
        placeholder="Írd ide az üzenetet..."
      />
    </div>
  );
}
