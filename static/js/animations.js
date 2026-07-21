// static/js/animations.js
// Konvexity — premium interaction layer. Restrained by design: one
// orchestrated hero moment, quiet scroll reveals, and a magnetic touch
// on primary actions. Nothing fights for attention.

(function () {
  'use strict';

  const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* =========================================
     SCROLL REVEAL
     Targets both legacy class names used across templates
     (.reveal, .lens-reveal, .fade-in, .fade-up) and the newer
     data-reveal attribute API.
  ========================================= */
  const revealSelector = '.fade-up, .fade-in, .reveal, .lens-reveal, [data-reveal], .card, .glass-card, .about-card, .lens-card, .program-card, .solution-card, .phase-item';
  const revealElements = document.querySelectorAll(revealSelector);

  if (!prefersReducedMotion && revealElements.length) {
    const revealObserver = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          const delay = entry.target.dataset.delay ? parseInt(entry.target.dataset.delay, 10) : 0;
          setTimeout(() => {
            entry.target.classList.add('revealed');
            entry.target.classList.add('visible');
          }, delay);
          revealObserver.unobserve(entry.target);
        }
      });
    }, { threshold: 0.12, rootMargin: '0px 0px -60px 0px' });

    revealElements.forEach((el, index) => {
      if (!el.dataset.delay) {
        el.style.transitionDelay = `${Math.min(index % 6, 5) * 0.06}s`;
      }
      revealObserver.observe(el);
    });
  } else {
    revealElements.forEach((el) => { el.classList.add('revealed'); el.classList.add('visible'); });
  }

  /* =========================================
     MOBILE NAVIGATION TOGGLE
  ========================================= */
  const navToggle = document.getElementById('navToggle');
  const navLinks = document.getElementById('navLinks');

  if (navToggle && navLinks) {
    navToggle.addEventListener('click', () => {
      const expanded = navToggle.getAttribute('aria-expanded') === 'true';
      navLinks.classList.toggle('active');
      navToggle.setAttribute('aria-expanded', String(!expanded));

      const lines = navToggle.querySelectorAll('.hamburger-line');
      if (!expanded) {
        lines[0].style.transform = 'rotate(45deg) translate(4px, 5px)';
        lines[1].style.opacity = '0';
        lines[2].style.transform = 'rotate(-45deg) translate(4px, -5px)';
      } else {
        lines[0].style.transform = 'none';
        lines[1].style.opacity = '1';
        lines[2].style.transform = 'none';
      }
    });

    document.querySelectorAll('.nav-link').forEach((link) => {
      link.addEventListener('click', () => {
        navLinks.classList.remove('active');
        navToggle.setAttribute('aria-expanded', 'false');
        const lines = navToggle.querySelectorAll('.hamburger-line');
        lines[0].style.transform = 'none';
        lines[1].style.opacity = '1';
        lines[2].style.transform = 'none';
      });
    });
  }

  /* =========================================
     STICKY NAVBAR SCROLL STATE
  ========================================= */
  const navbar = document.querySelector('.navbar');
  if (navbar) {
    let ticking = false;
    window.addEventListener('scroll', () => {
      if (!ticking) {
        requestAnimationFrame(() => {
          navbar.classList.toggle('scrolled', window.scrollY > 40);
          ticking = false;
        });
        ticking = true;
      }
    });
  }

  /* =========================================
     ACTIVE NAV LINK (fallback for non-Jinja contexts)
  ========================================= */
  const currentPath = window.location.pathname;
  document.querySelectorAll('.nav-link').forEach((link) => {
    if (link.getAttribute('href') === currentPath) link.classList.add('active');
  });

  /* =========================================
     MAGNETIC PRIMARY ACTIONS — subtle, capped range
  ========================================= */
  if (!prefersReducedMotion) {
    document.querySelectorAll('.btn-primary, .nav-cta, .magnetic').forEach((button) => {
      button.addEventListener('mousemove', (e) => {
        const rect = button.getBoundingClientRect();
        const x = e.clientX - rect.left - rect.width / 2;
        const y = e.clientY - rect.top - rect.height / 2;
        button.style.transform = `translate(${Math.max(-6, Math.min(6, x * 0.12))}px, ${Math.max(-4, Math.min(4, y * 0.12))}px)`;
      });
      button.addEventListener('mouseleave', () => { button.style.transform = ''; });
    });
  }

  /* =========================================
     HERO — the convexity curve draws on load
  ========================================= */
  const curvePath = document.querySelector('.hero-curve path');
  if (curvePath && !prefersReducedMotion) {
    const length = curvePath.getTotalLength();
    curvePath.style.strokeDasharray = `${length}`;
    curvePath.style.strokeDashoffset = `${length}`;
    requestAnimationFrame(() => {
      curvePath.style.transition = 'stroke-dashoffset 1.8s cubic-bezier(0.22,1,0.36,1) 0.3s';
      curvePath.style.strokeDashoffset = '0';
    });
  }

  /* =========================================
     AMBIENT HERO PARALLAX — desktop only, very subtle
  ========================================= */
  const heroAurora = document.querySelector('.hero__aurora, .hero-curve');
  if (heroAurora && !prefersReducedMotion && window.innerWidth > 900) {
    document.addEventListener('mousemove', (e) => {
      const x = (e.clientX / window.innerWidth - 0.5) * 14;
      const y = (e.clientY / window.innerHeight - 0.5) * 14;
      heroAurora.style.transform = `translate3d(${x * 0.4}px, ${y * 0.4}px, 0)`;
    });
  }

  /* =========================================
     SMOOTH ANCHOR SCROLL
  ========================================= */
  document.querySelectorAll('a[href^="#"]').forEach((anchor) => {
    anchor.addEventListener('click', function (e) {
      const targetId = this.getAttribute('href');
      if (targetId.length < 2) return;
      const target = document.querySelector(targetId);
      if (target) {
        e.preventDefault();
        target.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }
    });
  });

})();
