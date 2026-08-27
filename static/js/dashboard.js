(function () {
    const charts = [];
    const reducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

    function colors() {
        const dark = document.documentElement.dataset.theme === "dark";
        return { text: dark ? "#cbd5e1" : "#334155", grid: dark ? "#1e3a5f" : "#e2e8f0", blue: dark ? "#60a5fa" : "#2563eb", cyan: dark ? "#22d3ee" : "#0f766e" };
    }

    function drawCharts() {
        if (typeof Chart === "undefined" || !Array.isArray(window.dashboardData)) return;
        charts.forEach((chart) => chart.destroy());
        charts.length = 0;
        const palette = colors();
        const labels = window.dashboardData.map((item) => item.name);
        const hours = window.dashboardData.map((item) => item.optimized_hours);
        const performance = window.dashboardData.map((item) => item.predicted_performance);
        const base = { responsive: true, maintainAspectRatio: false, animation: reducedMotion ? false : { duration: 900, easing: "easeOutQuart" }, plugins: { legend: { display: false }, tooltip: { backgroundColor: "#0f172a", padding: 12, cornerRadius: 8 } }, scales: { x: { ticks: { color: palette.text }, grid: { display: false } }, y: { beginAtZero: true, ticks: { color: palette.text }, grid: { color: palette.grid } } } };
        const hoursCanvas = document.getElementById("hoursChart");
        if (hoursCanvas) charts.push(new Chart(hoursCanvas, { type: "bar", data: { labels, datasets: [{ data: hours, backgroundColor: palette.blue, hoverBackgroundColor: palette.cyan, borderRadius: 8, borderSkipped: false }] }, options: { ...base, scales: { ...base.scales, y: { ...base.scales.y, title: { display: true, text: "Hours per day", color: palette.text } } } } }));
        const performanceCanvas = document.getElementById("performanceChart");
        if (performanceCanvas) charts.push(new Chart(performanceCanvas, { type: "bar", data: { labels, datasets: [{ data: performance, backgroundColor: palette.cyan, hoverBackgroundColor: palette.blue, borderRadius: 8, borderSkipped: false }] }, options: { ...base, scales: { ...base.scales, y: { ...base.scales.y, max: 100, title: { display: true, text: "Score (0–100)", color: palette.text } } } } }));
    }

    function countUp() {
        document.querySelectorAll("[data-count-value]").forEach((element) => {
            const target = Number(element.dataset.countValue);
            const decimals = Number(element.dataset.countDecimals || 0);
            if (reducedMotion || !Number.isFinite(target)) { element.textContent = target.toFixed(decimals); return; }
            const start = performance.now();
            const tick = (now) => { const progress = Math.min((now - start) / 850, 1); const eased = 1 - Math.pow(1 - progress, 3); element.textContent = (target * eased).toFixed(decimals); if (progress < 1) requestAnimationFrame(tick); };
            requestAnimationFrame(tick);
        });
    }

    function reveal() { document.querySelectorAll(".reveal").forEach((element) => element.classList.add("is-revealed")); }
    document.addEventListener("DOMContentLoaded", () => { countUp(); reveal(); drawCharts(); });
    document.addEventListener("themechange", drawCharts);
}());
