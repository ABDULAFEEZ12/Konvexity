// static/js/animations.js

(function () {
    'use strict';

    const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

    /* =========================================
       PREMIUM SCROLL REVEAL
    ========================================= */
    const revealElements = document.querySelectorAll(
        '.fade-up, .glass-card, .glass-panel, .hero-content, .section > *'
    );

    if (!prefersReducedMotion) {
        const revealObserver = new IntersectionObserver((entries) => {
            entries.forEach((entry) => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('revealed');
                    revealObserver.unobserve(entry.target);
                }
            });
        }, {
            threshold: 0.12,
            rootMargin: '0px 0px -40px 0px'
        });

        revealElements.forEach((el, index) => {
            el.style.opacity = '0';
            el.style.transform = 'translateY(32px)';
            el.style.transition = `opacity 0.9s cubic-bezier(0.22, 1, 0.36, 1) ${index * 0.05}s,
                                   transform 0.9s cubic-bezier(0.22, 1, 0.36, 1) ${index * 0.05}s`;

            revealObserver.observe(el);
        });

        document.addEventListener('scroll', () => {
            document.querySelectorAll('.revealed').forEach((el) => {
                el.style.opacity = '1';
                el.style.transform = 'translateY(0)';
            });
        });
    } else {
        revealElements.forEach((el) => {
            el.style.opacity = '1';
            el.style.transform = 'none';
            el.style.transition = 'none';
        });
    }

    /* =========================================
       MOBILE NAVIGATION TOGGLE
    ========================================= */
    const navToggle = document.getElementById('navToggle');
    const navLinks = document.getElementById('navLinks');

    if (navToggle && navLinks) {
        navToggle.addEventListener('click', () => {
            navLinks.classList.toggle('active');

            const expanded = navToggle.getAttribute('aria-expanded') === 'true';
            navToggle.setAttribute('aria-expanded', !expanded);

            const lines = navToggle.querySelectorAll('.hamburger-line');

            if (!expanded) {
                lines[0].style.transform = 'rotate(45deg) translate(5px, 5px)';
                lines[1].style.opacity = '0';
                lines[2].style.transform = 'rotate(-45deg) translate(5px, -5px)';
            } else {
                lines[0].style.transform = 'none';
                lines[1].style.opacity = '1';
                lines[2].style.transform = 'none';
            }
        });

        // Close menu when a link is clicked
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
       STICKY NAVBAR SCROLL EFFECT
    ========================================= */
    const navbar = document.querySelector('.navbar');

    if (navbar) {
        window.addEventListener('scroll', () => {
            if (window.scrollY > 40) {
                navbar.classList.add('scrolled');
            } else {
                navbar.classList.remove('scrolled');
            }
        });
    }

    /* =========================================
       ACTIVE NAVIGATION LINK
    ========================================= */
    const currentPath = window.location.pathname;

    document.querySelectorAll('.nav-link').forEach((link) => {
        const href = link.getAttribute('href');

        if (href === currentPath) {
            link.classList.add('active');
        }
    });

    /* =========================================
       PREMIUM MAGNETIC BUTTON EFFECT
    ========================================= */
    if (!prefersReducedMotion) {
        document.querySelectorAll('.btn, .nav-cta').forEach((button) => {
            button.addEventListener('mousemove', (e) => {
                const rect = button.getBoundingClientRect();
                const x = e.clientX - rect.left - rect.width / 2;
                const y = e.clientY - rect.top - rect.height / 2;

                button.style.transform = `translate(${x * 0.08}px, ${y * 0.08}px)`;
            });

            button.addEventListener('mouseleave', () => {
                button.style.transform = 'translate(0, 0)';
            });
        });
    }

    /* =========================================
       SUBTLE PARALLAX AMBIENT EFFECT
    ========================================= */
    const hero = document.querySelector('.hero');

    if (hero && !prefersReducedMotion && window.innerWidth > 768) {
        document.addEventListener('mousemove', (e) => {
            const x = (e.clientX / window.innerWidth - 0.5) * 10;
            const y = (e.clientY / window.innerHeight - 0.5) * 10;

            hero.style.transform = `translate3d(${x * 0.5}px, ${y * 0.5}px, 0)`;
        });
    }

    /* =========================================
       GLASS CARD HOVER LIFT
    ========================================= */
    if (!prefersReducedMotion) {
        document.querySelectorAll('.glass-card, .glass-panel').forEach((card) => {
            card.addEventListener('mousemove', (e) => {
                const rect = card.getBoundingClientRect();
                const x = e.clientX - rect.left;
                const y = e.clientY - rect.top;

                const rotateY = ((x / rect.width) - 0.5) * 6;
                const rotateX = ((y / rect.height) - 0.5) * -6;

                card.style.transform = `perspective(1000px)
                                        rotateX(${rotateX}deg)
                                        rotateY(${rotateY}deg)
                                        translateY(-6px)`;
            });

            card.addEventListener('mouseleave', () => {
                card.style.transform = 'perspective(1000px) rotateX(0) rotateY(0) translateY(0)';
            });
        });
    }

    /* =========================================
       SMOOTH ANCHOR SCROLL
    ========================================= */
    document.querySelectorAll('a[href^="#"]').forEach((anchor) => {
        anchor.addEventListener('click', function (e) {
            const target = document.querySelector(this.getAttribute('href'));

            if (target) {
                e.preventDefault();

                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });

})();
