(function () {
  const STORAGE_KEY = "jh_cart_v1";

  function getCart() {
    try {
      return JSON.parse(localStorage.getItem(STORAGE_KEY)) || [];
    } catch (e) {
      return [];
    }
  }

  function saveCart(cart) {
    try {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(cart));
    } catch (e) {
      /* storage unavailable */
    }
    renderAll();
  }

  function lineKey(id, length) {
    return `${id}::${length || "std"}`;
  }

  function addItem(item, quantity) {
    quantity = quantity || 1;
    const cart = getCart();
    const key = lineKey(item.id, item.length);
    const existing = cart.find((i) => lineKey(i.id, i.length) === key);
    if (existing) existing.quantity += quantity;
    else cart.push(Object.assign({ quantity }, item));
    saveCart(cart);
    openDrawer();
  }

  function removeItem(id, length) {
    const cart = getCart().filter((i) => lineKey(i.id, i.length) !== lineKey(id, length));
    saveCart(cart);
  }

  function updateQuantity(id, length, quantity) {
    const cart = getCart()
      .map((i) => (lineKey(i.id, i.length) === lineKey(id, length) ? Object.assign({}, i, { quantity: Math.max(1, quantity) }) : i))
      .filter((i) => i.quantity > 0);
    saveCart(cart);
  }

  function clearCart() {
    saveCart([]);
  }

  function subtotal(cart) {
    return cart.reduce((sum, i) => sum + i.price * i.quantity, 0);
  }

  function itemCount(cart) {
    return cart.reduce((sum, i) => sum + i.quantity, 0);
  }

  function formatNaira(amount) {
    return "₦" + Math.round(amount).toLocaleString("en-NG");
  }

  function escapeHtml(value) {
    return String(value || "").replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
  }

  function mediaHtml(image, seed, alt) {
    const safeAlt = escapeHtml(alt);
    if (image && image !== "placeholder") {
      return `<div class="product-photo"><img src="${image}" alt="${safeAlt}" loading="lazy"></div>`;
    }
    return `<div class="product-photo product-photo--empty" role="img" aria-label="${safeAlt}"></div>`;
  }

  // ---- Drawer ----
  function openDrawer() {
    document.querySelector("[data-cart-drawer]")?.classList.add("is-open");
    document.querySelector("[data-cart-overlay]")?.classList.add("is-open");
  }
  function closeDrawer() {
    document.querySelector("[data-cart-drawer]")?.classList.remove("is-open");
    document.querySelector("[data-cart-overlay]")?.classList.remove("is-open");
  }

  function renderBadge() {
    const count = itemCount(getCart());
    document.querySelectorAll("[data-cart-count]").forEach((el) => {
      el.textContent = String(count);
      el.style.display = count > 0 ? "flex" : "none";
    });
  }

  function renderDrawer() {
    const container = document.querySelector("[data-cart-drawer-items]");
    const emptyEl = document.querySelector("[data-cart-drawer-empty]");
    const footerEl = document.querySelector("[data-cart-drawer-footer]");
    if (!container) return;

    const cart = getCart();
    if (cart.length === 0) {
      container.innerHTML = "";
      container.style.display = "none";
      if (emptyEl) emptyEl.style.display = "flex";
      if (footerEl) footerEl.style.display = "none";
      return;
    }
    container.style.display = "block";
    if (emptyEl) emptyEl.style.display = "none";
    if (footerEl) footerEl.style.display = "block";

    container.innerHTML = cart
      .map(
        (item, idx) => `
      <li class="cart-line" style="border-top:none;padding-top:${idx === 0 ? "0" : "1.25rem"};">
        <div class="cart-line__media">${mediaHtml(item.image, item.id, item.name)}</div>
        <div class="cart-line__body">
          <div class="cart-line__top">
            <div>
              <a href="/product/${item.slug}" style="font-size:0.9rem;font-weight:600;">${item.name}</a>
              ${item.length ? `<p class="text-muted" style="font-size:0.75rem;margin-top:2px;">${item.length}&quot; length</p>` : ""}
            </div>
            <button class="remove-btn" data-remove="${item.id}" data-length="${item.length || ""}" aria-label="Remove">&times;</button>
          </div>
          <div class="cart-line__bottom">
            <div class="qty-control" style="transform:scale(0.85);transform-origin:left;">
              <button data-qty-down="${item.id}" data-length="${item.length || ""}">&minus;</button>
              <span>${item.quantity}</span>
              <button data-qty-up="${item.id}" data-length="${item.length || ""}">+</button>
            </div>
            <span class="price">${formatNaira(item.price * item.quantity)}</span>
          </div>
        </div>
      </li>`
      )
      .join("");

    const subEl = document.querySelector("[data-cart-drawer-subtotal]");
    if (subEl) subEl.textContent = formatNaira(subtotal(cart));

    bindLineActions(container);
  }

  function renderCartPage() {
    const container = document.querySelector("[data-cart-page-items]");
    if (!container) return;
    const cart = getCart();
    const emptyEl = document.querySelector("[data-cart-page-empty]");
    const bodyEl = document.querySelector("[data-cart-page-body]");

    if (cart.length === 0) {
      if (bodyEl) bodyEl.style.display = "none";
      if (emptyEl) emptyEl.style.display = "flex";
      return;
    }
    if (bodyEl) bodyEl.style.display = "grid";
    if (emptyEl) emptyEl.style.display = "none";

    container.innerHTML = cart
      .map(
        (item) => `
      <li class="cart-line">
        <div class="cart-line__media">${mediaHtml(item.image, item.id, item.name)}</div>
        <div class="cart-line__body">
          <div class="cart-line__top">
            <div>
              <a href="/product/${item.slug}" style="font-family:var(--font-display);font-size:1rem;">${item.name}</a>
              ${item.length ? `<p class="text-muted" style="font-size:0.78rem;margin-top:2px;">${item.length}&quot; length</p>` : ""}
            </div>
            <button class="remove-btn" data-remove="${item.id}" data-length="${item.length || ""}" aria-label="Remove"><svg class="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6"><path d="M4 7h16M9 7V5a1 1 0 011-1h4a1 1 0 011 1v2m-9 0l1 12a1 1 0 001 1h8a1 1 0 001-1l1-12" stroke-linecap="round" stroke-linejoin="round"/></svg></button>
          </div>
          <div class="cart-line__bottom">
            <div class="qty-control">
              <button data-qty-down="${item.id}" data-length="${item.length || ""}">&minus;</button>
              <span>${item.quantity}</span>
              <button data-qty-up="${item.id}" data-length="${item.length || ""}">+</button>
            </div>
            <span class="price">${formatNaira(item.price * item.quantity)}</span>
          </div>
        </div>
      </li>`
      )
      .join("");

    document.querySelectorAll("[data-cart-subtotal]").forEach((el) => (el.textContent = formatNaira(subtotal(cart))));
    document.querySelectorAll("[data-cart-total]").forEach((el) => (el.textContent = formatNaira(subtotal(cart))));

    bindLineActions(container);
  }

  function bindLineActions(scope) {
    scope.querySelectorAll("[data-remove]").forEach((btn) => {
      btn.addEventListener("click", () => removeItem(btn.dataset.remove, btn.dataset.length || null));
    });
    scope.querySelectorAll("[data-qty-up]").forEach((btn) => {
      btn.addEventListener("click", () => {
        const cart = getCart();
        const item = cart.find((i) => lineKey(i.id, i.length) === lineKey(btn.dataset.qtyUp, btn.dataset.length || null));
        if (item) updateQuantity(btn.dataset.qtyUp, btn.dataset.length || null, item.quantity + 1);
      });
    });
    scope.querySelectorAll("[data-qty-down]").forEach((btn) => {
      btn.addEventListener("click", () => {
        const cart = getCart();
        const item = cart.find((i) => lineKey(i.id, i.length) === lineKey(btn.dataset.qtyDown, btn.dataset.length || null));
        if (item) updateQuantity(btn.dataset.qtyDown, btn.dataset.length || null, item.quantity - 1);
      });
    });
  }

  function renderAll() {
    renderBadge();
    renderDrawer();
    renderCartPage();
  }

  // ---- Add-to-cart buttons (product page + quick view) ----
  function bindAddToCartButtons() {
    document.querySelectorAll("[data-add-to-cart]").forEach((btn) => {
      btn.addEventListener("click", (e) => {
        // Card-level add buttons sit inside an <a> (the product link) — stop it from navigating.
        e.preventDefault();
        e.stopPropagation();
        const card = btn.closest("[data-product-payload]");
        if (!card) return;
        const product = JSON.parse(card.dataset.productPayload);
        const lengthEl = card.querySelector("[data-selected-length]");
        const qtyEl = card.querySelector("[data-selected-qty]");
        const length = lengthEl ? Number(lengthEl.dataset.selectedLength) || null : null;
        const quantity = qtyEl ? Number(qtyEl.textContent) || 1 : 1;
        addItem(
          { id: product.id, slug: product.slug, name: product.name, price: product.price, image: product.image, length },
          quantity
        );
      });
    });
  }

  // Length selector buttons (product page + quick view)
  function bindLengthSelectors() {
    document.querySelectorAll("[data-length-selector]").forEach((wrap) => {
      wrap.querySelectorAll(".length-btn").forEach((btn) => {
        btn.addEventListener("click", () => {
          wrap.querySelectorAll(".length-btn").forEach((b) => b.classList.remove("active"));
          btn.classList.add("active");
          const scope = wrap.closest("[data-product-payload]");
          const target = scope?.querySelector("[data-selected-length]");
          if (target) target.dataset.selectedLength = btn.dataset.length;
          if (scope) updateWhatsAppOrderLink(scope);
        });
      });
    });
  }

  // Quantity steppers (product page + quick view)
  function bindQuantitySteppers() {
    document.querySelectorAll("[data-qty-stepper]").forEach((wrap) => {
      const display = wrap.querySelector("[data-selected-qty]");
      const scope = wrap.closest("[data-product-payload]");
      wrap.querySelector("[data-qty-stepper-down]")?.addEventListener("click", () => {
        display.textContent = String(Math.max(1, Number(display.textContent) - 1));
        if (scope) updateWhatsAppOrderLink(scope);
      });
      wrap.querySelector("[data-qty-stepper-up]")?.addEventListener("click", () => {
        display.textContent = String(Number(display.textContent) + 1);
        if (scope) updateWhatsAppOrderLink(scope);
      });
    });
  }

  // Builds the "Order via WhatsApp" link with the live product name, selected
  // length, quantity and total amount baked into the message text.
  function updateWhatsAppOrderLink(scope) {
    const link = scope.querySelector("[data-whatsapp-order-link]");
    if (!link || !scope.dataset.productPayload) return;
    const product = JSON.parse(scope.dataset.productPayload);
    const lengthEl = scope.querySelector("[data-selected-length]");
    const qtyEl = scope.querySelector("[data-selected-qty]");
    const length = lengthEl?.dataset.selectedLength;
    const quantity = qtyEl ? Number(qtyEl.textContent) || 1 : 1;
    const amount = product.price * quantity;

    const lines = ["Hello Jennie_Hairport, I'd like to order:", "", `Product: ${product.name}`];
    if (length) lines.push(`Length: ${length} inches`);
    lines.push(`Quantity: ${quantity}`);
    lines.push(`Amount: ${formatNaira(amount)}`);
    lines.push("", "Please confirm availability and delivery details.");

    link.href = "https://wa.me/2349034160178?text=" + encodeURIComponent(lines.join("\n"));
  }

  // ---- Quick view modal ----
  function bindQuickView() {
    const overlay = document.querySelector("[data-quick-view-modal]");
    if (!overlay) return;

    document.querySelectorAll("[data-quick-view-trigger]").forEach((btn) => {
      btn.addEventListener("click", (e) => {
        e.preventDefault();
        const card = btn.closest("[data-product-payload]");
        if (!card) return;
        const product = JSON.parse(card.dataset.productPayload);
        populateQuickView(product);
        overlay.classList.add("is-open");
      });
    });

    overlay.querySelector("[data-quick-view-close]")?.addEventListener("click", () => overlay.classList.remove("is-open"));
    overlay.querySelector(".modal-overlay__bg")?.addEventListener("click", () => overlay.classList.remove("is-open"));
  }

  function populateQuickView(product) {
    const overlay = document.querySelector("[data-quick-view-modal]");
    overlay.querySelector("[data-qv-media]").innerHTML = mediaHtml(product.image, product.id, product.name);
    overlay.querySelector("[data-qv-category]").textContent = product.category;
    overlay.querySelector("[data-qv-name]").textContent = product.name;
    overlay.querySelector("[data-qv-price]").textContent = formatNaira(product.price);

    const oldPriceEl = overlay.querySelector("[data-qv-old-price]");
    if (product.oldPrice && product.oldPrice > product.price) {
      oldPriceEl.textContent = formatNaira(product.oldPrice);
      oldPriceEl.style.display = "inline";
    } else {
      oldPriceEl.style.display = "none";
    }

    overlay.querySelector("[data-qv-description]").textContent = product.description;

    const lengthWrap = overlay.querySelector("[data-length-selector]");
    lengthWrap.innerHTML = (product.lengths || [])
      .map((l, i) => `<button type="button" class="length-btn ${i === 0 ? "active" : ""}" data-length="${l}">${l}&quot;</button>`)
      .join("");

    const qtyDisplay = overlay.querySelector("[data-selected-qty]");
    if (qtyDisplay) qtyDisplay.textContent = "1";

    const payloadHost = overlay.querySelector("[data-product-payload]");
    payloadHost.dataset.productPayload = JSON.stringify(product);
    const selLen = payloadHost.querySelector("[data-selected-length]");
    if (selLen) selLen.dataset.selectedLength = (product.lengths && product.lengths[0]) || "";

    const viewLink = overlay.querySelector("[data-qv-view-link]");
    if (viewLink) viewLink.href = "/product/" + product.slug;

    bindLengthSelectors();
    bindQuantitySteppers();
    updateWhatsAppOrderLink(payloadHost);
  }

  // ---- Checkout ----
  function bindCheckout() {
    const form = document.querySelector("[data-checkout-form]");
    if (!form) return;
    const errorEl = document.querySelector("[data-checkout-error]");
    const submitBtn = form.querySelector("[data-checkout-submit]");

    function readCommonFields() {
      return {
        name: form.name.value.trim(),
        phone: form.phone.value.trim(),
        location: form.location.value.trim(),
        notes: form.notes.value.trim(),
      };
    }

    function cartItemsPayload() {
      const cart = getCart();
      return cart.map((i) => ({ id: i.id, name: i.name, price: i.price, quantity: i.quantity, length: i.length }));
    }

    // Pay Online with Squad — requires email for the receipt/payment record.
    form.addEventListener("submit", async (e) => {
      e.preventDefault();
      const cart = getCart();
      if (cart.length === 0) return;

      const payload = Object.assign(readCommonFields(), {
        email: form.email.value.trim(),
        items: cartItemsPayload(),
      });

      if (!payload.name || !payload.email || !payload.phone || !payload.location) {
        if (errorEl) errorEl.textContent = "Please fill in your name, email, phone and delivery location.";
        return;
      }

      if (errorEl) errorEl.textContent = "";
      submitBtn.disabled = true;
      submitBtn.textContent = "Redirecting to payment…";

      try {
        const res = await fetch("/api/checkout", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(payload),
        });
        const data = await res.json();
        if (!res.ok) throw new Error(data.message || "Something went wrong.");

        clearCart();
        window.location.href = data.checkout_url;
      } catch (err) {
        if (errorEl) errorEl.textContent = err.message || "Something went wrong. Please try again.";
        submitBtn.disabled = false;
        submitBtn.textContent = "Pay Online with Squad";
      }
    });
  }

  document.addEventListener("DOMContentLoaded", () => {
    renderAll();
    bindAddToCartButtons();
    bindLengthSelectors();
    bindQuantitySteppers();
    bindQuickView();
    bindCheckout();
    document.querySelectorAll("[data-product-payload]").forEach((scope) => updateWhatsAppOrderLink(scope));

    document.querySelector("[data-open-cart]")?.addEventListener("click", openDrawer);
    document.querySelector("[data-close-cart]")?.addEventListener("click", closeDrawer);
    document.querySelector("[data-cart-overlay]")?.addEventListener("click", closeDrawer);
  });

  window.JHCart = { getCart, addItem, clearCart };
})();
