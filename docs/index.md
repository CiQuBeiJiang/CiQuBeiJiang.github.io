---
title: 首页
statistics: false
hide:
  - navigation
  - toc
  - footer
  - feedback
  - title
---

<div class="page-home-archive home-v2">
  <div class="home-strip" aria-hidden="true"></div>

  <header class="home-hero">
    <div class="home-hero-text">
      <p class="home-kicker">私人档案 / ROLL_07</p>
      <p class="home-title">CiQuBeiJiang</p>
      <p class="home-title-cn">此去北疆</p>
      <p class="home-line">光从笔记、底片和未完成的模型之间慢慢渗出来。</p>
      <p class="home-meta"><span id="home-live-time">NANJING / --:--</span><span>阅读 · 摄影 · 写作 · 机器学习</span></p>
    </div>

    <figure class="home-photo">
      <img src="./assets/1-004_13.jpeg" alt="音乐台前的人群与一只飞起的白鸽">
      <figcaption>人群 / 音乐台 / VISION3 5207</figcaption>
    </figure>
  </header>

  <section class="home-section" aria-labelledby="home-latest-title">
    <div class="home-section-head">
      <h2 id="home-latest-title">最近更新</h2>
      <span>LATEST FRAMES</span>
    </div>

    <ol class="home-latest">
      <li><a href="diary/碎/">
        <span class="home-latest-code"><span>FRAME 05</span><span>2026.05.29</span></span>
        <span class="home-latest-body"><span class="home-latest-title">碎</span><span class="home-latest-excerpt">眼睛突然被晃了一下。地上散落着一堆碎片，零碎地反射着窗外的阳光。</span></span>
        <span class="home-latest-cat">随笔</span>
      </a></li>
      <li><a href="diary/第一百次告别/">
        <span class="home-latest-code"><span>FRAME 04</span><span>2026.05.20</span></span>
        <span class="home-latest-body"><span class="home-latest-title">第一百次告别</span><span class="home-latest-excerpt">坐在公交车的最后一排，看着雨滴在车窗上赛跑。</span></span>
        <span class="home-latest-cat">随笔</span>
      </a></li>
      <li><a href="optimization/telecom_network_maintenance/">
        <span class="home-latest-code"><span>FRAME 03</span><span>2026.05.11</span></span>
        <span class="home-latest-body"><span class="home-latest-title">XGBoost 与 MIP 联合优化</span><span class="home-latest-excerpt">通信网络维护调度里，预测模型和混合整数规划如何接在一起。</span></span>
        <span class="home-latest-cat">研究</span>
      </a></li>
      <li><a href="diary/找/">
        <span class="home-latest-code"><span>FRAME 02</span><span>2026.05.10</span></span>
        <span class="home-latest-body"><span class="home-latest-title">找</span><span class="home-latest-excerpt">书桌一团糟，胶卷又找不见了。</span></span>
        <span class="home-latest-cat">随笔</span>
      </a></li>
      <li><a href="diary/伞/">
        <span class="home-latest-code"><span>FRAME 01</span><span>2026.05.05</span></span>
        <span class="home-latest-body"><span class="home-latest-title">伞</span><span class="home-latest-excerpt">很想有一把好用的伞。只是不用来挡雨。</span></span>
        <span class="home-latest-cat">随笔</span>
      </a></li>
    </ol>
  </section>

  <section class="home-section" aria-labelledby="home-index-title">
    <div class="home-section-head">
      <h2 id="home-index-title">档案</h2>
      <span>INDEX</span>
    </div>

    <div class="home-index">
      <a href="reading/">
        <span class="home-index-code">01 READING</span>
        <span class="home-index-title">阅读</span>
        <span class="home-index-note">文学、哲学、阅读笔记与收藏的诗。</span>
      </a>
      <a href="diary/">
        <span class="home-index-code">02 ESSAYS</span>
        <span class="home-index-title">随笔</span>
        <span class="home-index-note">个人文章、观察、片段与尚未完成的想法。</span>
      </a>
      <a href="research/">
        <span class="home-index-code">03 RESEARCH</span>
        <span class="home-index-title">研究</span>
        <span class="home-index-note">机器学习、数据分析、运筹优化与技术札记。</span>
      </a>
    </div>
  </section>

  <footer class="home-footer">
    <nav aria-label="Secondary navigation">
      <a href="about/">个人简介</a>
      <a href="site_info/">网站信息</a>
      <a href="https://github.com/ciqubeijiang">GitHub</a>
      <a href="mailto:1724961030@qq.com">Email</a>
    </nav>
    <p>© 2026 CiQuBeiJiang · 南京</p>
  </footer>
</div>

<script>
document.addEventListener("DOMContentLoaded", function () {
  function updateHomeTime() {
    const node = document.getElementById("home-live-time");
    if (!node) return;
    const formatted = new Intl.DateTimeFormat("en-US", {
      hour: "2-digit",
      minute: "2-digit",
      hour12: true,
      timeZone: "Asia/Shanghai"
    }).format(new Date());
    node.textContent = "NANJING / " + formatted;
  }

  updateHomeTime();
  setInterval(updateHomeTime, 30000);
});
</script>
