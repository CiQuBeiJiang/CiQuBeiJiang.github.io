// 胶片主题首页的小动效：胶卷随滚动前进、帧号像计数器一样跳到当前帧
(function () {
    var root = document.documentElement;
    if (!root.classList.contains("film-motion")) return;
    if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) return;

    var home = document.querySelector(".layout-archive");
    if (!home) return;

    var strip = home.querySelector(".home-strip");
    if (strip) {
        var advance = function (y) {
            strip.style.backgroundPosition = (-y * 0.6).toFixed(1) + "px center, 0 0";
        };
        if (window.siteLenis) {
            window.siteLenis.on("scroll", function (e) { advance(e.scroll); });
        } else {
            window.addEventListener("scroll", function () { advance(window.scrollY); }, { passive: true });
        }
    }

    var list = home.querySelector(".home-latest");
    if (!list || !("IntersectionObserver" in window)) return;

    var codes = Array.prototype.map.call(list.querySelectorAll(".home-latest-code > span:first-child"), function (el) {
        var m = el.textContent.match(/^(\D*)(\d+)\s*$/);
        return m ? { el: el, prefix: m[1], target: parseInt(m[2], 10), width: m[2].length } : null;
    }).filter(Boolean);

    function pad(n, w) {
        n = String(n);
        while (n.length < w) n = "0" + n;
        return n;
    }

    codes.forEach(function (c) { c.el.textContent = c.prefix + pad(0, c.width); });

    var io = new IntersectionObserver(function (entries) {
        if (!entries[0].isIntersecting) return;
        io.disconnect();
        codes.forEach(function (c, i) {
            var n = 0;
            setTimeout(function tick() {
                c.el.textContent = c.prefix + pad(n, c.width);
                if (n++ < c.target) setTimeout(tick, 70);
            }, 200 + i * 140);
        });
    }, { rootMargin: "0px 0px -15% 0px" });
    io.observe(list);
})();
