const API_URL = "http://localhost:8000/api";

function getToken() {
    return localStorage.getItem("access_token");
}

function setToken(token) {
    localStorage.setItem("access_token", token);
}

function logout() {
    localStorage.removeItem("access_token");
    window.location.href = "/login";
}

async function apiCall(endpoint, method = "GET", body = null, isFormData = false) {
    const headers = {};
    const token = getToken();
    if (token) {
        headers["Authorization"] = `Bearer ${token}`;
    }
    if (!isFormData) {
        headers["Content-Type"] = "application/json";
    }

    const options = {
        method,
        headers,
    };

    if (body) {
        options.body = isFormData ? body : JSON.stringify(body);
    }

    const response = await fetch(`${API_URL}${endpoint}`, options);
    if (response.status === 401) {
        logout();
        return null;
    }
    return response;
}

function showLoader(id) {
    document.getElementById(id).style.display = "block";
}

function hideLoader(id) {
    document.getElementById(id).style.display = "none";
}

document.addEventListener("DOMContentLoaded", () => {
    // Check auth for protected routes
    const path = window.location.pathname;
    const token = getToken();
    const protectedRoutes = ["/dashboard", "/chat", "/image-generator", "/video-editor"];
    
    if (protectedRoutes.includes(path) && !token) {
        window.location.href = "/login";
    }
    
    if ((path === "/login" || path === "/signup") && token) {
        window.location.href = "/dashboard";
    }
});
