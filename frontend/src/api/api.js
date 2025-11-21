const API_BASE = "http://localhost:8000"; 
// majd cseréled a szerver URL-re, ha deploy lesz

export async function fetchDailyTips() {
    const res = await fetch(`${API_BASE}/tips/daily`);
    return res.json();
}

export async function fetchLiveTips() {
    const res = await fetch(`${API_BASE}/tips/live`);
    return res.json();
}

export async function fetchEvents() {
    const res = await fetch(`${API_BASE}/scraper/events`);
    return res.json();
}

export async function fetchStatus() {
    const res = await fetch(`${API_BASE}/system/status`);
    return res.json();
}
