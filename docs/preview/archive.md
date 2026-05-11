---
title: 档案页提案
statistics: false
hide:
  - navigation
  - toc
  - footer
  - feedback
  - title
---

<div class="page-home-archive" data-lang="zh">
  <div class="archive-lang-switch" role="group" aria-label="Language switch">
    <button class="archive-lang-button is-active" type="button" data-lang-choice="zh">中文</button>
    <button class="archive-lang-button" type="button" data-lang-choice="en">EN</button>
  </div>

  <header class="archive-intro">
    <figure class="archive-profile">
      <img src="../../assets/camera.png" alt="Analog profile mark">
    </figure>

    <div class="archive-identity">
      <p class="archive-kicker" data-i18n data-zh="机器学习 / 摄影 / 写作" data-en="MACHINE LEARNING / PHOTOGRAPHY / WRITING">机器学习 / 摄影 / 写作</p>
      <p class="archive-name">CiQuBeiJiang</p>
      <p class="archive-note" data-i18n data-zh="留在模型训练、联系表、以及南京深夜阅读之间的一些笔记。" data-en="Notes left between model training, contact sheets, and late-night reading in Nanjing.">
        留在模型训练、联系表、以及南京深夜阅读之间的一些笔记。
      </p>
      <p class="archive-meta" data-i18n data-zh="南京 / 阅读室 / 安静更新" data-en="NANJING / READING ROOM / UPDATED QUIETLY">南京 / 阅读室 / 安静更新</p>
    </div>
  </header>

  <main class="archive-index" aria-label="Archive index">
    <a class="archive-row" href="../../literary/">
      <span class="archive-row-code">ARCHIVE_01</span>
      <span class="archive-row-title" data-i18n data-zh="阅读" data-en="Reading">阅读</span>
      <span class="archive-row-text" data-i18n data-zh="文学、哲学、阅读笔记与页边残留的批注。" data-en="Literature, philosophy, reading notes, and marginal traces left in books.">文学、哲学、阅读笔记与页边残留的批注。</span>
    </a>

    <a class="archive-row" href="../../essays/">
      <span class="archive-row-code">ARCHIVE_02</span>
      <span class="archive-row-title" data-i18n data-zh="随笔" data-en="Essays">随笔</span>
      <span class="archive-row-text" data-i18n data-zh="个人文章、观察、碎片与尚未完成的想法。" data-en="Personal essays, observations, fragments, and unfinished thoughts.">个人文章、观察、碎片与尚未完成的想法。</span>
    </a>

    <a class="archive-row" href="../../research/">
      <span class="archive-row-code">ARCHIVE_03</span>
      <span class="archive-row-title" data-i18n data-zh="研究" data-en="Research">研究</span>
      <span class="archive-row-text" data-i18n data-zh="机器学习、数据分析、优化与深夜技术札记。" data-en="Machine learning, data analysis, optimization, and late-night technical notes.">机器学习、数据分析、优化与深夜技术札记。</span>
    </a>
  </main>

  <nav class="archive-footer-nav" aria-label="Secondary navigation">
    <a href="../" data-i18n data-zh="返回封面" data-en="Return to Cover">返回封面</a>
    <a href="../../reading/" data-i18n data-zh="阅读档案" data-en="Reading Archive">阅读档案</a>
    <a href="../../essays/" data-i18n data-zh="随笔档案" data-en="Essays Archive">随笔档案</a>
    <a href="../../research/" data-i18n data-zh="研究档案" data-en="Research Archive">研究档案</a>
  </nav>
</div>

<script>
document.addEventListener("DOMContentLoaded", function () {
  const root = document.querySelector(".page-home-archive");
  const langButtons = root?.querySelectorAll(".archive-lang-button");
  const i18nNodes = root?.querySelectorAll("[data-i18n]");

  function applyLanguage(lang) {
    if (!root) return;
    root.dataset.lang = lang;
    localStorage.setItem("privateArchiveLang", lang);
    i18nNodes?.forEach(function (node) {
      const nextText = node.dataset[lang];
      if (nextText) node.textContent = nextText;
    });
    langButtons?.forEach(function (button) {
      button.classList.toggle("is-active", button.dataset.langChoice === lang);
    });
  }

  const savedLang = localStorage.getItem("privateArchiveLang") || "zh";
  applyLanguage(savedLang);

  langButtons?.forEach(function (button) {
    button.addEventListener("click", function () {
      applyLanguage(button.dataset.langChoice || "zh");
    });
  });
});
</script>
