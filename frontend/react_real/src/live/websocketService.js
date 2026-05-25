import { getJson } from "../api/apiClient";

export async function websocketStats() {
    return await getJson("/socketio/stats");
}

export async function websocketPush() {
    return await getJson("/socketio/push-dashboard");
}

export async function websocketPushOCR(filename = "facture_live.pdf") {
    return await getJson(`/socketio/push-ocr?filename=${encodeURIComponent(filename)}`);
}
