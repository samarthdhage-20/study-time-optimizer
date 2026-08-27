(function () {
    const form = document.querySelector("[data-optimizer-form]");
    if (!form) return;
    const overlay = document.querySelector("[data-loading-overlay]");
    const submitButton = form.querySelector("button[type='submit']");
    const stages = Array.from(document.querySelectorAll("[data-loader-stage]"));

    form.addEventListener("submit", () => {
        if (form.dataset.submitting === "true") return;
        form.dataset.submitting = "true";
        if (submitButton) { submitButton.disabled = true; submitButton.classList.add("is-loading"); }
        if (overlay) overlay.classList.add("is-visible");
        stages.forEach((stage, index) => {
            window.setTimeout(() => stage.classList.add("is-active"), index * 500);
        });
    });
}());
