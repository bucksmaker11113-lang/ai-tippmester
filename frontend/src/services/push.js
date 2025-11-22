export function connectPush(onMessage) {
    const ws = new WebSocket("ws://127.0.0.1:8000/ws/push");

    ws.onopen = () => {
        console.log("PUSH WebSocket connected");
    };

    ws.onmessage = (event) => {
        try {
            const msg = JSON.parse(event.data);

            if (Notification.permission === "granted") {
                new Notification("Új Tippmester esemény!", {
                    body: msg.type + " | " + (msg.event || ""),
                });
            }

            onMessage(msg);
        } catch (err) {
            console.error("PUSH error:", err);
        }
    };

    ws.onerror = (e) => {
        console.log("WebSocket error:", e);
    };

    return ws;
}
