/**
 * SmartLibrary ERP - Enterprise JavaScript Core
 */
document.addEventListener("DOMContentLoaded", () => {
    // Auto dismiss alert messages after 5 seconds
    const alerts = document.querySelectorAll(".alert");
    alerts.forEach((alert) => {
        setTimeout(() => {
            alert.style.transition = "opacity 0.5s ease";
            alert.style.opacity = "0";
            setTimeout(() => alert.remove(), 500);
        }, 5000);
    });

    // Mobile sidebar toggle if trigger present
    const toggleBtn = document.getElementById("sidebar-toggle");
    const sidebar = document.querySelector(".sidebar");
    if (toggleBtn && sidebar) {
        toggleBtn.addEventListener("click", () => {
            sidebar.classList.toggle("show");
        });
    }
});
