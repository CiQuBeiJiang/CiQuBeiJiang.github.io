// 和梦途一样的惯性滚动（Lenis），首页再加一点视差和渐显
(function () {
    var reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    if (reduce || typeof Lenis === "undefined") return;

    var lenis = new Lenis({
        duration: 1.2,
        easing: function (t) { return Math.min(1, 1 - Math.pow(2, -10 * t)); },
        smoothWheel: true,
        anchors: true,
        allowNestedScroll: true
    });
    window.siteLenis = lenis;

    function raf(time) {
        lenis.raf(time);
        requestAnimationFrame(raf);
    }
    requestAnimationFrame(raf);

    // Material 的“回到顶部”按钮也走惯性滚动
    document.addEventListener("click", function (e) {
        var top = e.target.closest && e.target.closest(".md-top");
        if (!top) return;
        e.preventDefault();
        e.stopPropagation();
        lenis.scrollTo(0);
    }, true);

    // 以下只在首页
    var home = document.querySelector(".home-v2");
    if (!home) return;

    var text = home.querySelector(".home-hero-text");
    var photo = home.querySelector(".home-photo");
    lenis.on("scroll", function (e) {
        var y = Math.min(e.scroll, window.innerHeight);
        var fade = 1 - y / (window.innerHeight * 0.9);
        if (text) {
            text.style.translate = "0 " + (y * 0.18).toFixed(1) + "px";
            text.style.opacity = Math.max(fade, 0).toFixed(3);
        }
        if (photo) {
            photo.style.translate = "0 " + (y * 0.08).toFixed(1) + "px";
        }
    });

    var sections = home.querySelectorAll(".home-section");
    if (!("IntersectionObserver" in window) || !sections.length) return;
    document.documentElement.classList.add("home-reveal");
    var io = new IntersectionObserver(function (entries) {
        entries.forEach(function (entry) {
            if (entry.isIntersecting) {
                entry.target.classList.add("is-in");
                io.unobserve(entry.target);
            }
        });
    }, { rootMargin: "0px 0px -12% 0px" });
    sections.forEach(function (s) { io.observe(s); });
})();
