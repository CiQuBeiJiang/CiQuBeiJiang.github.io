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

// 左侧文字：标题逐字显影
(function () {
    var root = document.documentElement;
    if (!root.classList.contains("film-motion")) return;
    if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) return;

    var start = 0;
    [".layout-archive .home-title", ".layout-archive .home-title-cn"].forEach(function (sel) {
        var el = document.querySelector(sel);
        if (!el) return;
        var chars = Array.from(el.textContent.trim());
        el.setAttribute("aria-label", el.textContent.trim());
        el.textContent = "";
        chars.forEach(function (ch) {
            var s = document.createElement("span");
            s.className = "film-char";
            s.setAttribute("aria-hidden", "true");
            s.textContent = ch;
            s.style.setProperty("--i", start++);
            el.appendChild(s);
        });
        start += 3;
        el.classList.add("is-split");
    });
})();

// 鼠标移到文字上时有景深：整块随鼠标微微倾斜，靠近的标题字母被吸起来
(function () {
    var root = document.documentElement;
    if (!root.classList.contains("film-motion")) return;
    if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) return;
    if (!window.matchMedia("(hover: hover) and (pointer: fine)").matches) return;

    var hero = document.querySelector(".layout-archive .home-hero");
    var text = hero && hero.querySelector(".home-hero-text");
    if (!text) return;

    var chars = Array.prototype.slice.call(text.querySelectorAll(".film-char"));
    var lifts = chars.map(function () { return 0; });
    var mx = 0, my = 0, tx = 0, ty = 0;
    var px = -9999, py = -9999;
    var active = false, raf = null;

    hero.addEventListener("pointermove", function (e) {
        var r = text.getBoundingClientRect();
        mx = Math.max(-1, Math.min(1, (e.clientX - (r.left + r.width / 2)) / r.width));
        my = Math.max(-1, Math.min(1, (e.clientY - (r.top + r.height / 2)) / r.height));
        px = e.clientX;
        py = e.clientY;
        active = true;
        kick();
    });

    hero.addEventListener("pointerleave", function () {
        mx = 0;
        my = 0;
        px = py = -9999;
        active = false;
        kick();
    });

    function frame() {
        tx += (mx - tx) * 0.1;
        ty += (my - ty) * 0.1;
        text.style.transform = "perspective(1000px) rotateY(" + (tx * 7).toFixed(2) + "deg) rotateX(" + (-ty * 7).toFixed(2) + "deg)";

        var moving = Math.abs(mx - tx) > 0.002 || Math.abs(my - ty) > 0.002;
        chars.forEach(function (c, i) {
            var b = c.getBoundingClientRect();
            var dx = px - (b.left + b.width / 2);
            var dy = py - (b.top + b.height / 2 + lifts[i]);
            var f = Math.max(0, 1 - Math.sqrt(dx * dx + dy * dy) / 150);
            var target = f * f * 12;
            lifts[i] += (target - lifts[i]) * 0.2;
            if (Math.abs(target - lifts[i]) > 0.05) moving = true;
            c.style.transform = lifts[i] > 0.05 ? "translateY(" + (-lifts[i]).toFixed(2) + "px)" : "";
            c.style.color = f > 0.05 ? "color-mix(in srgb, var(--site-accent) " + Math.round(f * 75) + "%, var(--archive-ink))" : "";
        });

        raf = moving || active ? requestAnimationFrame(frame) : null;
    }

    function kick() {
        if (!raf) raf = requestAnimationFrame(frame);
    }
})();
