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

<div class="page-cover-archive">
  <div class="film-border film-border-top" aria-hidden="true"></div>

  <section class="cover-stage">
    <div class="cover-left">
      <button class="cover-flip" type="button" aria-label="翻转档案卡片">
        <span class="cover-flip-face cover-flip-front">
          <span class="cover-mark cover-mark-top">私人档案 / 2026</span>
          <span class="cover-title">CiQuBeiJiang</span>
          <span class="cover-title-cn">此去北疆</span>
          <span class="cover-line">光从笔记、底片和未完成的模型之间慢慢渗出来。</span>
          <span class="cover-mark cover-mark-bottom">点击翻转这一帧</span>
        </span>

        <span class="cover-flip-face cover-flip-back">
          <span class="cover-photo-frame" data-photo-orientation="landscape">
            <span class="cover-photo-image">
              <img class="cover-photo-asset" src="./assets/1-004_13.jpeg" alt="封面档案照片">
            </span>
            <span class="cover-photo-note">人群 / 音乐台 / 02:17</span>
          </span>
        </span>
      </button>
    </div>

    <aside class="cover-right" aria-label="Archive metadata">
      <p>ROLL_07</p>
      <p>FRAME_18</p>
      <p><span id="cover-live-time">NANJING / --:-- --</span></p>
      <p>VISION3 5207 拍摄</p>
      <p>归档笔记、图像与模型</p>
    </aside>
  </section>

  <a class="cover-enter" href="./archive/">进入</a>

  <div class="film-border film-border-bottom" aria-hidden="true"></div>
</div>

<script>
document.addEventListener("DOMContentLoaded", function () {
  const root = document.querySelector(".page-cover-archive");
  const flip = root?.querySelector(".cover-flip");
  const enter = root?.querySelector(".cover-enter");

  if (flip) {
    flip.addEventListener("click", function () {
      flip.classList.toggle("is-flipped");
    });
  }

  function updateCoverTime() {
    const timeNode = document.getElementById("cover-live-time");
    if (!timeNode) return;
    const now = new Date();
    const formatted = new Intl.DateTimeFormat("en-US", {
      hour: "2-digit",
      minute: "2-digit",
      hour12: true
    }).format(now);
    timeNode.textContent = "NANJING / " + formatted;
  }

  updateCoverTime();
  setInterval(updateCoverTime, 30000);

  document.addEventListener("keydown", function (event) {
    if (event.key === "Enter" && enter) {
      window.location.href = enter.href;
    }
  });
});
</script>
