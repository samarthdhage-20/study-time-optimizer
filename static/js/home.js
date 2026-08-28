(function () {
    const toggle = document.querySelector("[data-menu-toggle]");
    const links = document.querySelector("[data-nav-links]");
    if (toggle && links) toggle.addEventListener("click", () => { const open = links.classList.toggle("is-open"); toggle.setAttribute("aria-expanded", open); });
    const items = document.querySelectorAll(".home-section, .home-cta");
    const progress = document.querySelector("[data-scroll-progress]");
    const nav = document.querySelector(".home-nav");
    const visual = document.querySelector(".system-visual");
    const reducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    function updateScrollState() {
        const max = document.documentElement.scrollHeight - window.innerHeight;
        if (progress) progress.style.transform = `scaleX(${max > 0 ? window.scrollY / max : 0})`;
        if (nav) nav.classList.toggle("is-scrolled", window.scrollY > 18);
    }
    window.addEventListener("scroll", updateScrollState, { passive: true });
    updateScrollState();
    if (visual && !reducedMotion && window.matchMedia("(pointer: fine)").matches) {
        visual.addEventListener("pointermove", (event) => { const rect = visual.getBoundingClientRect(); visual.style.setProperty("--pointer-x", `${(event.clientX - rect.left) / rect.width - .5}`); visual.style.setProperty("--pointer-y", `${(event.clientY - rect.top) / rect.height - .5}`); });
        visual.addEventListener("pointerleave", () => { visual.style.setProperty("--pointer-x", "0"); visual.style.setProperty("--pointer-y", "0"); });
    }
    if (!window.matchMedia("(prefers-reduced-motion: reduce)").matches && "IntersectionObserver" in window) {
        const observer = new IntersectionObserver((entries) => entries.forEach((entry) => { if (entry.isIntersecting) { entry.target.classList.add("in-view"); entry.target.querySelectorAll(".feature-card, .home-timeline > div, .tech-grid > div, .method-step").forEach((child, index) => { child.style.setProperty("--stagger", `${index * 90}ms`); child.classList.add("item-in-view"); }); observer.unobserve(entry.target); } }), { threshold: 0.12 });
        items.forEach((item) => { item.classList.add("scroll-reveal"); observer.observe(item); });
    }
}());
