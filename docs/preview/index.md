---
title: 封面页提案
statistics: false
hide:
  - navigation
  - toc
  - footer
  - feedback
  - title
---

<div class="page-cover-archive" data-lang="zh">
  <div class="archive-lang-switch" role="group" aria-label="Language switch">
    <button class="archive-lang-button is-active" type="button" data-lang-choice="zh">中文</button>
    <button class="archive-lang-button" type="button" data-lang-choice="en">EN</button>
  </div>

  <div class="film-border film-border-top" aria-hidden="true"></div>

  <section class="cover-stage">
    <div class="cover-left">
      <button class="cover-flip" type="button" aria-label="Flip archive card">
        <span class="cover-flip-face cover-flip-front">
          <span class="cover-mark cover-mark-top" data-i18n data-zh="私人档案 / 2026" data-en="PRIVATE ARCHIVE / 2026">私人档案 / 2026</span>
          <span class="cover-title">CiQuBeiJiang</span>
          <span class="cover-title-cn">此去北疆</span>
          <span class="cover-line" data-i18n data-zh="光从笔记、底片和未完成的模型之间慢慢渗出来。" data-en="light leaks through notebooks, negatives, and unfinished models">光从笔记、底片和未完成的模型之间慢慢渗出来。</span>
          <span class="cover-mark cover-mark-bottom" data-i18n data-zh="点击翻转这一帧" data-en="tap to turn the frame">点击翻转这一帧</span>
        </span>

        <span class="cover-flip-face cover-flip-back">
          <span class="cover-photo-frame" data-photo-orientation="landscape" data-photo-src="">
            <span class="cover-photo-image" aria-hidden="true"></span>
            <span class="cover-photo-note" data-i18n data-zh="人群 / 音悦台 / 02:17" data-en="latent image / corridor light / 02:17">人群 / 音乐台 / 02:17</span>
          </span>
        </span>
      </button>
    </div>

    <aside class="cover-right" aria-label="Archive metadata">
      <p>ROLL_07</p>
      <p>FRAME_18</p>
      <p>NANJING / 02:17 AM</p>
      <p data-i18n data-zh="VISION3 5207 拍摄" data-en="SHOT ON VISION3 5207">VISION3 5207 拍摄</p>
      <p data-i18n data-zh="归档笔记、图像与模型" data-en="INDEXING NOTES, IMAGES, MODELS">归档笔记、图像与模型</p>
    </aside>
  </section>

  <a class="cover-enter" href="./archive/" data-i18n data-zh="进入" data-en="ENTER">进入</a>

  <div class="film-border film-border-bottom" aria-hidden="true"></div>
</div>

<script>
document.addEventListener("DOMContentLoaded", function () {
  const root = document.querySelector(".page-cover-archive");
  const flip = root?.querySelector(".cover-flip");
  const enter = root?.querySelector(".cover-enter");
  const langButtons = root?.querySelectorAll(".archive-lang-button");
  const i18nNodes = root?.querySelectorAll("[data-i18n]");
  const photoFrame = root?.querySelector(".cover-photo-frame");
  const photoImage = root?.querySelector(".cover-photo-image");

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

  if (flip) {
    flip.addEventListener("click", function () {
      flip.classList.toggle("is-flipped");
    });
  }

  if (photoFrame && photoImage) {
    const photoSrc = (photoFrame.dataset.photoSrc || "").trim();
    if (photoSrc) {
      photoImage.style.setProperty("--cover-photo-src", 'url("' + photoSrc + '")');
      photoImage.classList.add("has-photo");
    }
  }

  document.addEventListener("keydown", function (event) {
    if (event.key === "Enter" && enter) {
      window.location.href = enter.href;
    }
  });
});
</script>
