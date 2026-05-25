import { API } from "../api/apiClient";

export async function loginApi(email, password) {
    const response = await API.post("/auth/login", {
        email,
        password
    });

    if (response.data.success) {
        localStorage.setItem("comptapilot_token", response.data.token);
        localStorage.setItem("comptapilot_user", response.data.user.email);
        localStorage.setItem("comptapilot_role", response.data.user.role);
    }

    return response.data;
}

export function logout() {
    localStorage.removeItem("comptapilot_token");
    localStorage.removeItem("comptapilot_user");
    localStorage.removeItem("comptapilot_role");
}

export function isAuthenticated() {
    return Boolean(localStorage.getItem("comptapilot_token"));
}

export function currentUser() {
    return {
        email: localStorage.getItem("comptapilot_user") || "admin@comptapilot.local",
        role: localStorage.getItem("comptapilot_role") || "SUPER_ADMIN"
    };
}
