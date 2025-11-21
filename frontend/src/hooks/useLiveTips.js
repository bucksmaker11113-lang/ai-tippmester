import { useEffect, useState } from "react";
import { fetchLiveTips } from "../api/api";

export function useLiveTips() {
    const [liveTips, setLiveTips] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        async function load() {
            const data = await fetchLiveTips();
            setLiveTips(data.live_tips || data);
            setLoading(false);
        }
        load();
    }, []);

    return { liveTips, loading };
}
