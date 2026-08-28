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
            button.setAttribute("aria-label", theme === "dark" ? "Switch to light mode" : "Switch to dark mode");
            const label = button.querySelector(".theme-label");
            if (label) label.textContent = theme === "dark" ? "Light mode" : "Dark mode";
            const icon = button.querySelector(".theme-icon");
            if (icon) { icon.textContent = theme === "dark" ? "☀" : "☾"; icon.classList.remove("is-switching"); void icon.offsetWidth; icon.classList.add("is-switching"); }
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
