import axios from "axios";

export const API = axios.create({
    baseURL: "http://localhost:5001/api/v3"
});

API.interceptors.request.use((config) => {
    const token = localStorage.getItem("comptapilot_token");

    if (token) {
        config.headers.Authorization = `Bearer ${token}`;
    }

    return config;
});

export async function getJson(endpoint) {
    const response = await API.get(endpoint);
    return response.data;
}

export async function postForm(endpoint, formData) {
    const response = await API.post(endpoint, formData, {
        headers: {
            "Content-Type": "multipart/form-data"
        }
    });

    return response.data;
}
