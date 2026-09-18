// Header scroll shadow
(function () {
  const header = document.querySelector(".site-header");
  if (!header) return;
  const onScroll = () => header.classList.toggle("is-scrolled", window.scrollY > 8);
  onScroll();
  window.addEventListener("scroll", onScroll, { passive: true });
})();

// Mobile menu
(function () {
  const openBtn = document.querySelector("[data-open-mobile-menu]");
  const closeBtn = document.querySelector("[data-close-mobile-menu]");
  const menu = document.querySelector("[data-mobile-menu]");
  if (!menu) return;
  openBtn?.addEventListener("click", () => menu.classList.add("is-open"));
  closeBtn?.addEventListener("click", () => menu.classList.remove("is-open"));
  menu.querySelectorAll("a").forEach((a) => a.addEventListener("click", () => menu.classList.remove("is-open")));
})();

// Reveal-on-scroll
(function () {
  const items = document.querySelectorAll(".reveal");
  if (!items.length) return;
  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add("is-visible");
          observer.unobserve(entry.target);
        }
      });
    },
    { threshold: 0.15 }
  );
  items.forEach((el) => observer.observe(el));
})();

// Product gallery thumbnails
(function () {
  const main = document.querySelector("[data-gallery-main]");
  const thumbs = document.querySelectorAll(".gallery__thumb");
  if (!main || !thumbs.length) return;
  thumbs.forEach((thumb) => {
    thumb.addEventListener("click", () => {
      thumbs.forEach((t) => t.classList.remove("active"));
      thumb.classList.add("active");
      const sourcePhoto = thumb.querySelector(".placeholder-photo");
      const targetPhoto = main.querySelector(".placeholder-photo");
      if (sourcePhoto && targetPhoto) {
        targetPhoto.className = sourcePhoto.className;
      }
    });
  });
})();

// Accordion (product info)
(function () {
  document.querySelectorAll(".accordion__trigger").forEach((trigger) => {
    trigger.addEventListener("click", () => {
      const item = trigger.closest(".accordion__item");
      const wasOpen = item.classList.contains("open");
      item.parentElement.querySelectorAll(".accordion__item").forEach((i) => i.classList.remove("open"));
      if (!wasOpen) item.classList.add("open");
    });
  });
})();

// Shop mobile filter drawer
(function () {
  const openBtn = document.querySelector("[data-open-filters]");
  const closeBtn = document.querySelector("[data-close-filters]");
  const drawer = document.querySelector("[data-filter-drawer]");
  if (!drawer) return;
  openBtn?.addEventListener("click", () => drawer.classList.add("is-open"));
  closeBtn?.addEventListener("click", () => drawer.classList.remove("is-open"));
  drawer.querySelector(".filter-drawer__overlay")?.addEventListener("click", () => drawer.classList.remove("is-open"));
})();

// Sort select navigates with query param preserved
(function () {
  document.querySelectorAll("[data-sort-select]").forEach((select) => {
    select.addEventListener("change", () => {
      const url = new URL(window.location.href);
      if (select.value) url.searchParams.set("sort", select.value);
      else url.searchParams.delete("sort");
      window.location.href = url.toString();
    });
  });
})();

// Length filter chip toggle (shop sidebar / drawer)
(function () {
  document.querySelectorAll("[data-length-chip]").forEach((chip) => {
    chip.addEventListener("click", () => {
      const url = new URL(window.location.href);
      const value = chip.getAttribute("data-length-chip");
      if (url.searchParams.get("length") === value) url.searchParams.delete("length");
      else url.searchParams.set("length", value);
      window.location.href = url.toString();
    });
  });
})();

// Availability checkbox
(function () {
  document.querySelectorAll("[data-availability-toggle]").forEach((box) => {
    box.addEventListener("change", () => {
      const url = new URL(window.location.href);
      if (box.checked) url.searchParams.set("availability", "in-stock");
      else url.searchParams.delete("availability");
      window.location.href = url.toString();
    });
  });
})();
