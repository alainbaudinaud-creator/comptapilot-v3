export function loginDemo(email, password) {

    const token = btoa(`${email}:${password}:${Date.now()}`);

    localStorage.setItem("comptapilot_token", token);
    localStorage.setItem("comptapilot_user", email);

    return {
        success: true,
        token,
        user: {
            email,
            role: "SUPER_ADMIN"
        }
    };
}

export function logout() {
    localStorage.removeItem("comptapilot_token");
    localStorage.removeItem("comptapilot_user");
}

export function isAuthenticated() {
    return Boolean(localStorage.getItem("comptapilot_token"));
}

export function currentUser() {
    return localStorage.getItem("comptapilot_user") || "admin@comptapilot.local";
}
