/**
 * Main Frontend Application Logic
 * Handles API calls and UI interactions
 */

const API_BASE = "http://localhost:5000/api";

// ===========================
// UTILITY FUNCTIONS
// ===========================

/**
 * Show alert message
 */
function showAlert(message, type = "info") {
    const alertDiv = document.querySelector(".alert");
    if (!alertDiv) {
        const container = document.querySelector(".content");
        const newAlert = document.createElement("div");
        newAlert.className = `alert ${type}`;
        newAlert.textContent = message;
        container.insertBefore(newAlert, container.firstChild);
    } else {
        alertDiv.textContent = message;
        alertDiv.className = `alert ${type}`;
        alertDiv.style.display = "block";
    }
    
    setTimeout(() => {
        alertDiv.style.display = "none";
    }, 4000);
}

/**
 * Make API request
 */
async function apiCall(endpoint, method = "GET", data = null) {
    const options = {
        method: method,
        headers: {
            "Content-Type": "application/json"
        }
    };

    if (data) {
        options.body = JSON.stringify(data);
    }

    try {
        const response = await fetch(`${API_BASE}${endpoint}`, options);
        const result = await response.json();

        if (!response.ok) {
            throw new Error(result.error || "API Error");
        }

        return result;
    } catch (error) {
        showAlert(`Error: ${error.message}`, "error");
        console.error("API Error:", error);
        return null;
    }
}

// ===========================
// INITIALIZATION
// ===========================

document.addEventListener('DOMContentLoaded', function() {
    // Any global initialization can go here
    console.log('Application loaded');
});
