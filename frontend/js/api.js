const API = "https://wastewatar.onrender.com/";

function token() {
    return localStorage.getItem("token") || "";
}

async function api(path, options = {}) {

    options.headers = {
        "Content-Type": "application/json",
        ...(options.headers || {})
    };

    const t = token();

    if (t) {
        options.headers["Authorization"] = `Bearer ${t}`;
    }

    const response = await fetch(API + path, options);

    const data = await response.json().catch(() => ({}));

    if (!response.ok) {
        throw new Error(data.detail || "Request failed");
    }

    return data;
}

function requireLogin() {
    if (!token()) {
        window.location.href = "index.html";
    }
}

function logout() {
    localStorage.removeItem("token");
    localStorage.removeItem("user");

    window.location.href = "index.html";
}
