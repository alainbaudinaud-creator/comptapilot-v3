import { getJson } from "../api/apiClient";

export async function websocketStats() {
    return await getJson("/live/websocket/stats");
}

export async function websocketPush() {
    return await getJson("/live/websocket/push");
}
