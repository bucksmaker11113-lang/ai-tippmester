// -----------------------------
// API BASE URL
// -----------------------------
const API_BASE = "http://127.0.0.1:8000";

async function apiGet(url) {
    try {
        const res = await fetch(API_BASE + url);
        return await res.json();
    } catch (err) {
        console.error("API ERROR:", url, err);
        return { error: true };
    }
}

// -----------------------------
// SINGLE TIPS
// -----------------------------
export async function getSingleTips() {
    return await apiGet("/api/single");
}

// -----------------------------
// KOMBI TIPS
// -----------------------------
export async function getKombiTips() {
    return await apiGet("/api/kombi");
}

// -----------------------------
// LIVE TIPS
// -----------------------------
export async function getLiveTips() {
    return await apiGet("/api/live");
}

// -----------------------------
// INTERNATIONAL ODDS
// -----------------------------
export async function getInternationalOdds() {
    return await apiGet("/api/international");
}

// -----------------------------
// INTERNATIONAL LIVE ODDS
// -----------------------------
export async function getInternationalLive() {
    return await apiGet("/api/international/live");
}

// -----------------------------
// TIPPMIXPRO ODDS
// -----------------------------
export async function getTippmixproOdds() {
    return await apiGet("/api/events");
}

// -----------------------------
// BANKROLLS
// -----------------------------
export async function getSingleBankroll() {
    return await apiGet("/api/bankroll/single");
}

export async function getKombiBankroll() {
    return await apiGet("/api/bankroll/kombi");
}

export async function getLiveBankroll() {
    return await apiGet("/api/bankroll/live");
}
