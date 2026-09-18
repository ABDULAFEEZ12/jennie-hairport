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

// Product gallery: swipeable main track + thumbnails + dots + lightbox
(function () {
  const swipe = document.querySelector("[data-gallery-swipe]");
  if (!swipe) return;

  const slides = Array.from(swipe.querySelectorAll("[data-slide-index]"));
  const thumbs = Array.from(document.querySelectorAll("[data-thumb-index]"));
  const dots = Array.from(document.querySelectorAll("[data-dot-index]"));

  function setActive(index) {
    thumbs.forEach((t, i) => t.classList.toggle("active", i === index));
    dots.forEach((d, i) => d.classList.toggle("active", i === index));
  }

  function goTo(index, behavior) {
    const slide = slides[index];
    if (!slide) return;
    swipe.scrollTo({ left: slide.offsetLeft, behavior: behavior || "smooth" });
    setActive(index);
  }

  thumbs.forEach((thumb, i) => thumb.addEventListener("click", () => goTo(i)));

  let scrollTimer;
  swipe.addEventListener(
    "scroll",
    () => {
      clearTimeout(scrollTimer);
      scrollTimer = setTimeout(() => {
        const index = Math.round(swipe.scrollLeft / swipe.clientWidth);
        setActive(index);
      }, 80);
    },
    { passive: true }
  );

  // Lightbox
  const lightbox = document.querySelector("[data-lightbox]");
  if (!lightbox || slides.length === 0) return;
  const stage = lightbox.querySelector("[data-lightbox-stage]");
  const prevBtn = lightbox.querySelector("[data-lightbox-prev]");
  const nextBtn = lightbox.querySelector("[data-lightbox-next]");
  let current = 0;

  if (slides.length < 2) {
    if (prevBtn) prevBtn.style.display = "none";
    if (nextBtn) nextBtn.style.display = "none";
  }

  function renderStage() {
    const media = slides[current].querySelector("img, .product-photo");
    stage.innerHTML = "";
    if (!media) return;
    if (media.tagName === "IMG") {
      const img = document.createElement("img");
      img.src = media.src;
      img.alt = media.alt;
      stage.appendChild(img);
    } else {
      stage.appendChild(media.cloneNode(true));
    }
  }

  function open(index) {
    current = index;
    renderStage();
    lightbox.classList.add("is-open");
    document.body.style.overflow = "hidden";
  }
  function close() {
    lightbox.classList.remove("is-open");
    document.body.style.overflow = "";
  }
  function step(delta) {
    current = (current + delta + slides.length) % slides.length;
    renderStage();
  }

  slides.forEach((slide, i) => slide.addEventListener("click", () => open(i)));
  lightbox.querySelectorAll("[data-lightbox-close]").forEach((el) => el.addEventListener("click", close));
  prevBtn?.addEventListener("click", () => step(-1));
  nextBtn?.addEventListener("click", () => step(1));
  document.addEventListener("keydown", (e) => {
    if (!lightbox.classList.contains("is-open")) return;
    if (e.key === "Escape") close();
    if (e.key === "ArrowLeft") step(-1);
    if (e.key === "ArrowRight") step(1);
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
