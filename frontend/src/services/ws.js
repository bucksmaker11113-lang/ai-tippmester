const WS_BASE = "ws://127.0.0.1:8000";

// -----------------------------
// LIVE TIP STREAM
// -----------------------------
export function connectLiveTips(onMessage) {
    const ws = new WebSocket(WS_BASE + "/ws/live");

    ws.onopen = () => console.log("WS LIVE CONNECTED");
    ws.onmessage = (event) => onMessage(event.data);
    ws.onerror = (e) => console.log("WS ERROR", e);
    ws.onclose = () => console.log("WS CLOSED");

    return ws;
}

// -----------------------------
// PUSH NOTIFICATIONS
// -----------------------------
export function connectPush(onMessage) {
    const ws = new WebSocket(WS_BASE + "/ws/push");

    ws.onopen = () => console.log("WS PUSH CONNECTED");
    ws.onmessage = (event) => onMessage(event.data);

    return ws;
}
