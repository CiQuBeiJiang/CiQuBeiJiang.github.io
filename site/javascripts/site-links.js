document.addEventListener("DOMContentLoaded", function () {
  const homepage = "/";
  const siteLinks = document.querySelectorAll('a[title="此去北疆"]');

  siteLinks.forEach(function (link) {
    link.setAttribute("href", homepage);
  });
});
