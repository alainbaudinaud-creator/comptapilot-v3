import { io } from "socket.io-client";

const SOCKET_URL = "http://localhost:5001";

export const socket = io(SOCKET_URL, {
    transports: ["websocket", "polling"]
});

export function startRealtimeDashboard(callbacks = {}) {

    socket.on("connect", () => {

        console.log("Socket.IO connecté");
    });

    socket.on("server_message", (payload) => {

        console.log("SERVER MESSAGE", payload);

        if (callbacks.onServerMessage) {
            callbacks.onServerMessage(payload);
        }
    });

    socket.on("dashboard_update", (payload) => {

        console.log("DASHBOARD UPDATE", payload);

        if (callbacks.onDashboardUpdate) {
            callbacks.onDashboardUpdate(payload);
        }
    });

    socket.on("ocr_update", (payload) => {

        console.log("OCR UPDATE", payload);

        if (callbacks.onOCRUpdate) {
            callbacks.onOCRUpdate(payload);
        }
    });
}

export function emitDashboardRefresh(data = {}) {

    socket.emit("dashboard_refresh", data);
}

export function emitOCRAnalysis(filename) {

    socket.emit("ocr_analysis", {
        filename
    });
}
