import { getJson } from "../api/apiClient";

export async function loadCockpitLiveData() {

    const endpoints = {
        financier: "/dashboard-financier",
        production: "/production-premium",
        orchestration: "/orchestration/dashboard",
        securite: "/securite-probatoire/dashboard",
        enterprise: "/enterprise/dashboard",
        reglementaire: "/reglementaire/dashboard",
        commercial: "/commercial/dashboard",
        goLive: "/go-live/dashboard"
    };

    const result = {};

    for (const [key, endpoint] of Object.entries(endpoints)) {

        try {
            result[key] = await getJson(endpoint);
        } catch (error) {
            result[key] = {
                success: false,
                error: error.message
            };
        }
    }

    return result;
}
