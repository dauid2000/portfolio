/* ==========================================================================
   David Musumali — Portfolio
   script.js
   Navigation, scroll-spy, reveal animations, hero particles,
   project modal, contact form validation, toast notifications.
   ========================================================================== */

"use strict";

/* ---------- Small helpers ---------- */
const $ = (sel, ctx = document) => ctx.querySelector(sel);
const $$ = (sel, ctx = document) => Array.from(ctx.querySelectorAll(sel));

/* ==========================================================================
   1. NAVIGATION
   ========================================================================== */
const navbar = $("#navbar");
const navToggle = $("#nav-toggle");
const navLinks = $("#nav-links");
const navItems = $$(".nav-link");

/* Mobile hamburger menu */
navToggle.addEventListener("click", () => {
  const isOpen = navLinks.classList.toggle("open");
  navToggle.classList.toggle("open", isOpen);
  navToggle.setAttribute("aria-expanded", String(isOpen));
  navToggle.setAttribute("aria-label", isOpen ? "Close menu" : "Open menu");
});

/* Close the mobile menu when a link is clicked */
navItems.forEach((link) =>
  link.addEventListener("click", () => {
    navLinks.classList.remove("open");
    navToggle.classList.remove("open");
    navToggle.setAttribute("aria-expanded", "false");
  })
);

/* Navbar background on scroll */
const onScrollNav = () => {
  navbar.classList.toggle("scrolled", window.scrollY > 30);
};
window.addEventListener("scroll", onScrollNav, { passive: true });
onScrollNav();

/* ---------- Scroll-spy: highlight active nav item ---------- */
const sections = $$("main section[id]");
const setActiveLink = (id) => {
  navItems.forEach((link) => {
    const isActive = link.getAttribute("href") === `#${id}`;
    link.classList.toggle("active", isActive);
  });
};

const spyObserver = new IntersectionObserver(
  (entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) setActiveLink(entry.target.id);
    });
  },
  { rootMargin: "-45% 0px -50% 0px", threshold: 0 }
);
sections.forEach((section) => spyObserver.observe(section));

/* ==========================================================================
   2. SCROLL REVEAL ANIMATIONS
   ========================================================================== */
const revealObserver = new IntersectionObserver(
  (entries, observer) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        entry.target.classList.add("visible");
        observer.unobserve(entry.target);
      }
    });
  },
  { threshold: 0.12, rootMargin: "0px 0px -40px 0px" }
);

$$(".reveal").forEach((el) => revealObserver.observe(el));

/* ==========================================================================
   3. HERO PARTICLES — subtle "digital mining" drift
   Amber particles rising slowly, like data/dust in a shaft.
   ========================================================================== */
const canvas = $("#hero-particles");

if (canvas && !window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
  const ctx2d = canvas.getContext("2d");
  let particles = [];
  let rafId = null;
  let width = 0;
  let height = 0;

  const createParticles = () => {
    const count = Math.min(70, Math.floor(width / 18));
    particles = Array.from({ length: count }, () => ({
      x: Math.random() * width,
      y: Math.random() * height,
      r: Math.random() * 1.8 + 0.6,
      speedY: Math.random() * 0.35 + 0.08,
      speedX: (Math.random() - 0.5) * 0.15,
      alpha: Math.random() * 0.45 + 0.1,
      amber: Math.random() > 0.55,
    }));
  };

  const resize = () => {
    const rect = canvas.parentElement.getBoundingClientRect();
    width = rect.width;
    height = rect.height;
    canvas.width = width;
    canvas.height = height;
    createParticles();
  };

  const draw = () => {
    ctx2d.clearRect(0, 0, width, height);

    particles.forEach((p) => {
      p.y -= p.speedY;
      p.x += p.speedX;

      /* wrap around edges */
      if (p.y < -10) {
        p.y = height + 10;
        p.x = Math.random() * width;
      }
      if (p.x < -10) p.x = width + 10;
      if (p.x > width + 10) p.x = -10;

      ctx2d.beginPath();
      ctx2d.arc(p.x, p.y, p.r, 0, Math.PI * 2);
      ctx2d.fillStyle = p.amber
        ? `rgba(245, 166, 35, ${p.alpha})`
        : `rgba(255, 255, 255, ${p.alpha * 0.55})`;
      ctx2d.fill();
    });

    rafId = requestAnimationFrame(draw);
  };

  resize();
  draw();
  window.addEventListener("resize", resize);

  /* Pause animation when hero is off-screen (saves battery) */
  new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting && rafId === null) {
        rafId = requestAnimationFrame(draw);
      } else if (!entry.isIntersecting && rafId !== null) {
        cancelAnimationFrame(rafId);
        rafId = null;
      }
    });
  }).observe(canvas.parentElement);
}

/* ==========================================================================
   4. PROJECT MODAL — "Technology Used" details
   --------------------------------------------------------------------------
   The entries below are the offline fallback. On load, loadProjects() fetches
   /api/projects and merges fresh data in (matched by project name), so the
   modal always shows what the API serves when it is reachable.
   ========================================================================== */
const PROJECT_DATA = {
  banakulu: {
    title: "Bana Kulu Finances",
    desc:
      "A loan business management system designed to manage customers, loans, " +
      "repayments, interest, outstanding balances and business reporting.",
    tech: [
      "Python",
      "SQLite",
      "Streamlit",
      "React",
      "FastAPI",
      "Database Systems",
    ],
    note: "Live link coming soon — deployment in progress.",
  },
  dispatch: {
    title: "Bus Station Transport Management & Automated Dispatch System",
    desc:
      "A transport management and automated dispatch system designed to improve " +
      "bus allocation, loading sequences, fleet management and station operations.",
    tech: [
      "Python",
      "SQLite",
      "Automation",
      "Database Systems",
      "SMS Integration",
    ],
    note: "Live link coming soon — deployment in progress.",
  },
};

/* Merge API project objects into the modal cache. Keys stay stable
   ("banakulu", "dispatch") so the existing buttons keep working. */
const applyProjectsToModalData = (projects) => {
  for (const [key, data] of Object.entries(PROJECT_DATA)) {
    const match = projects.find((p) => p.name === data.title);
    if (!match) continue;
    data.desc = match.description;
    if (match.tagline) data.note = match.tagline;
    if (Array.isArray(match.technologies) && match.technologies.length > 0) {
      data.tech = match.technologies;
    }
    data.projectUrl = match.project_url || null;
  }
};

/* Fetch projects from the API. Runs at the end of this file, after all
   UI helpers exist. Silent fallback: the static data above stays in use. */
const loadProjects = async () => {
  if (!window.PortfolioAPI) return;
  try {
    const projects = await window.PortfolioAPI.getProjects();
    applyProjectsToModalData(projects);
  } catch (err) {
    console.warn("Projects could not be loaded from the API:", err.message);
  }
};

const modal = $("#project-modal");
const modalTitle = $("#modal-title");
const modalDesc = $("#modal-desc");
const modalList = $("#modal-list");
const modalNote = $("#modal-note");
const modalClose = $("#modal-close");
let lastFocused = null;

const openModal = (key) => {
  const data = PROJECT_DATA[key];
  if (!data) return;

  modalTitle.textContent = data.title;
  modalDesc.textContent = data.desc;
  modalNote.textContent = data.note;
  modalList.innerHTML = data.tech
    .map((t) => `<li>${t}</li>`)
    .join("");

  lastFocused = document.activeElement;
  modal.hidden = false;
  requestAnimationFrame(() => modal.classList.add("visible"));
  document.body.style.overflow = "hidden";
  modalClose.focus();
};

const closeModal = () => {
  modal.classList.remove("visible");
  document.body.style.overflow = "";
  setTimeout(() => {
    modal.hidden = true;
  }, 280);
  if (lastFocused) lastFocused.focus();
};

$$("[data-open-modal]").forEach((btn) =>
  btn.addEventListener("click", () => openModal(btn.dataset.project))
);

modalClose.addEventListener("click", closeModal);

modal.addEventListener("click", (e) => {
  if (e.target === modal) closeModal();
});

document.addEventListener("keydown", (e) => {
  if (e.key === "Escape" && !modal.hidden) closeModal();
});

/* "View Project" links — live links will replace this later */
$$(".project-link").forEach((link) =>
  link.addEventListener("click", (e) => {
    e.preventDefault();
    const pData = PROJECT_DATA[link.dataset.project];
    if (pData && pData.projectUrl) {
      window.open(pData.projectUrl, "_blank", "noopener");
      return;
    }
    showToast("Live project link coming soon. Use “Technology Used” for details.");
  })
);

/* Placeholder blog links */
$$("[data-placeholder-article]").forEach((link) =>
  link.addEventListener("click", (e) => {
    e.preventDefault();
    showToast("This article is being written — check back soon.");
  })
);

/* ==========================================================================
   5. TOAST NOTIFICATIONS
   ========================================================================== */
const toast = $("#toast");
let toastTimer = null;

function showToast(message, isError = false) {
  toast.textContent = message;
  toast.classList.toggle("error", isError);
  toast.classList.add("show");

  clearTimeout(toastTimer);
  toastTimer = setTimeout(() => toast.classList.remove("show"), 3600);
}

/* ==========================================================================
   6. CONTACT FORM VALIDATION
   ========================================================================== */
const form = $("#contact-form");
const fields = {
  name: {
    input: $("#cf-name"),
    validate: (v) =>
      v.trim().length >= 2 || "Please enter your name (at least 2 characters).",
  },
  email: {
    input: $("#cf-email"),
    validate: (v) =>
      /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(v.trim()) ||
      "Please enter a valid email address.",
  },
  subject: {
    input: $("#cf-subject"),
    validate: (v) =>
      v.trim().length >= 3 || "Please enter a subject (at least 3 characters).",
  },
  message: {
    input: $("#cf-message"),
    validate: (v) =>
      v.trim().length >= 10 ||
      "Please write a message of at least 10 characters.",
  },
};

const setError = (input, message) => {
  const errorEl = $(`[data-error-for="${input.id}"]`);
  input.classList.toggle("invalid", Boolean(message));
  if (errorEl) errorEl.textContent = message || "";
};

const validateField = (field) => {
  const result = field.validate(field.input.value);
  const ok = result === true;
  setError(field.input, ok ? "" : result);
  return ok;
};

/* Live validation once a field has been touched */
Object.values(fields).forEach((field) => {
  field.input.addEventListener("blur", () => validateField(field));
  field.input.addEventListener("input", () => {
    if (field.input.classList.contains("invalid")) validateField(field);
  });
});

form.addEventListener("submit", async (e) => {
  e.preventDefault();

  const results = Object.values(fields).map(validateField);
  const allValid = results.every(Boolean);

  if (!allValid) {
    showToast("Please fix the highlighted fields before sending.", true);
    const firstInvalid = $(".form-group input.invalid, .form-group textarea.invalid");
    if (firstInvalid) firstInvalid.focus();
    return;
  }

  /* Send to the Personal API (js/api.js). Validation already passed above;
     server-side errors are mapped back onto the individual fields. */
  const submitBtn = $("#cf-submit");
  const label = submitBtn.querySelector(".btn-label");
  const original = label.textContent;

  if (!window.PortfolioAPI) {
    showToast("Messaging is temporarily unavailable. Please email me directly.", true);
    return;
  }

  submitBtn.disabled = true;
  label.textContent = "Sending...";

  const payload = {
    name: fields.name.input.value.trim(),
    email: fields.email.input.value.trim(),
    subject: fields.subject.input.value.trim(),
    message: fields.message.input.value.trim(),
  };

  try {
    const result = await window.PortfolioAPI.sendContact(payload);
    if (result.ok) {
      form.reset();
      Object.values(fields).forEach((f) => setError(f.input, ""));
      showToast("Message sent successfully. David will get back to you soon.");
    } else {
      let matchedField = false;
      for (const [fieldName, message] of Object.entries(result.errors || {})) {
        if (fields[fieldName]) {
          setError(fields[fieldName].input, message);
          matchedField = true;
        }
      }
      showToast(
        matchedField
          ? "Please fix the highlighted fields and try again."
          : result.message || "The message could not be sent. Please try again.",
        true
      );
    }
  } catch (err) {
    showToast(err.message || "Network error — please try again.", true);
  } finally {
    label.textContent = original;
    submitBtn.disabled = false;
  }
});

/* ==========================================================================
   7. MISC
   ========================================================================== */

/* Smooth scrolling is handled by CSS (scroll-behavior + scroll-padding-top),
   but respect reduced-motion users who got it disabled there. */

/* Pull live project data from the API (falls back silently to the
   static PROJECT_DATA above when the API is unreachable). */
loadProjects();

/* Current year in footer (keeps © year fresh) */
const yearEl = $(".footer-bottom p");
if (yearEl) {
  yearEl.textContent = yearEl.textContent.replace(/\d{4}/, new Date().getFullYear());
}
