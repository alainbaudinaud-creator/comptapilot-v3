import axios from "axios";

const apiClient = axios.create({

    baseURL: "http://localhost:5001/api/v3",

    headers: {
        "Content-Type": "application/json"
    }
});

export async function getJson(url) {

    const response = await apiClient.get(url);

    return response.data;
}

export async function postJson(url, data) {

    const response = await apiClient.post(url, data);

    return response.data;
}

export default apiClient;
