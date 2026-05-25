import axios from "axios";

const API = axios.create({
    baseURL: "http://localhost:5001/api/v3"
});

export async function chargerDashboard() {

    const endpoints = [
        "/dashboard",
        "/cloud",
        "/commercialisation",
        "/experience-finale",
        "/plateforme-reelle"
    ];

    const results = {};

    for (const endpoint of endpoints) {

        try {

            const response = await API.get(endpoint);

            results[endpoint] = response.data;

        } catch (error) {

            results[endpoint] = {
                success: false,
                error: error.message
            };
        }
    }

    return results;
}
