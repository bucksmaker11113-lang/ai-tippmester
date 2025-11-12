import React, { useState } from "react";

export default function ChatPanel() {
  const [messages, setMessages] = useState([
    { from: "mesterke", text: "Szia! Én vagyok Mesterke 👋 Kérj tippet, vagy tölts fel egy képet!" }
  ]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);

  // Szöveges üzenetküldés
  const sendMessage = () => {
    if (!input.trim()) return;
    const userMsg = { from: "user", text: input };
    const botMsg = {
      from: "mesterke",
      text: getRandomResponse(input)
    };
    setMessages([...messages, userMsg, botMsg]);
    setInput("");
  };

  // Véletlen magyar válaszok
  const getRandomResponse = () => {
    const responses = [
      "Ez érdekes tipp! Nézzük meg közelebbről... 🤔",
      "Hmm, ebben látok fantáziát! 💚",
      "A statisztikák szerint nem rossz ötlet! 📈",
      "Kíváncsi vagyok, mit mond majd a Monte Carlo motor... 🎲",
      "Sosem lehet tudni, de érzem benne a value-t! ⚽"
    ];
    return responses[Math.floor(Math.random() * responses.length)];
  };

  // 📸 Képfeltöltés kezelése (Railway optimalizált)
  const handlePhotoUpload = async (e) => {
    const file = e.target.files[0];
    if (!file) return;

    setLoading(true);
    setMessages(prev => [...prev, { from: "user", text: "📷 Fotó feltöltve, feldolgozom..." }]);

    const formData = new FormData();
    formData.append("file", file);

    try {
      const res = await fetch("/vision/analyze_image", {
        method: "POST",
        body: formData,
      });

      if (!res.ok) throw new Error("Sikertelen feldolgozás");
      const data = await res.json();

      const msgText = data.comment
        ? `📸 ${data.match || "Ismeretlen meccs"} — ${data.comment}`
        : "Nem tudtam kiolvasni a képet. 😅";

      setMessages(prev => [...prev, { from: "mesterke", text: msgText }]);
    } catch (err) {
      console.error("Hiba a képfeldolgozásnál:", err);
      setMessages(prev => [
        ...prev,
        { from: "mesterke", text: "Valami gubanc történt a kép elemzésekor. Próbáld újra! 😔" },
      ]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="chat-panel">
      <h3 className="title">💬 Tippmester AI Chat</h3>

      <div className="chat-window">
        {messages.map((m, i) => (
          <div key={i} className={`msg ${m.from}`}>
            {m.text}
          </div>
        ))}
        {loading && <div className="msg mesterke">⏳ Feldolgozás folyamatban...</div>}
      </div>

      <div className="chat-input">
        <input
          type="text"
          placeholder="Írj valamit Mesterkének..."
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && sendMessage()}
        />
        <button onClick={sendMessage}>➡️</button>
      </div>

      <div className="photo-upload">
        <label htmlFor="photo" className="upload-btn">
          📸 Kép feltöltése
        </label>
        <input
          id="photo"
          type="file"
          accept="image/*"
          onChange={handlePhotoUpload}
          style={{ display: "none" }}
        />
      </div>
    </div>
  );
}
