(function () {
    const storageKey = "study-optimizer-theme";
    const root = document.documentElement;
    const saved = localStorage.getItem(storageKey);
    const initial = saved || (window.matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light");
    root.dataset.theme = initial;

    function updateCharts() {
        document.dispatchEvent(new CustomEvent("themechange", { detail: { theme: root.dataset.theme } }));
    }

    function setTheme(theme) {
        root.dataset.theme = theme;
        localStorage.setItem(storageKey, theme);
        document.querySelectorAll("[data-theme-toggle]").forEach((button) => {
            button.setAttribute("aria-pressed", theme === "dark");
            const label = button.querySelector(".theme-label");
            if (label) label.textContent = theme === "dark" ? "Light mode" : "Dark mode";
        });
        updateCharts();
    }

    document.addEventListener("DOMContentLoaded", () => {
        setTheme(root.dataset.theme);
        document.querySelectorAll("[data-theme-toggle]").forEach((button) => {
            button.addEventListener("click", () => setTheme(root.dataset.theme === "dark" ? "light" : "dark"));
        });
    });
}());
