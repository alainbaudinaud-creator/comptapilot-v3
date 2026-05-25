import { useEffect, useState } from "react";
import { loadCockpitLiveData } from "../services/cockpitLiveService";

export default function useCockpitLive(refreshMs = 10000) {

    const [data, setData] = useState({});
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState("");

    async function refresh() {

        try {
            setError("");

            const result = await loadCockpitLiveData();

            setData(result);

        } catch (e) {
            setError(e.message || "Erreur chargement cockpit");
        }

        setLoading(false);
    }

    useEffect(() => {

        refresh();

        const timer = setInterval(refresh, refreshMs);

        return () => clearInterval(timer);

    }, [refreshMs]);

    return {
        data,
        loading,
        error,
        refresh
    };
}
