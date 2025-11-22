import { useEffect, useState } from "react";
import { fetchDailyTips } from "../api/api";

export function useDailyTips() {
    const [tips, setTips] = useState(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        async function load() {
            const data = await fetchDailyTips();
            setTips(data);
            setLoading(false);
        }
        load();
    }, []);

    return { tips, loading };
}
