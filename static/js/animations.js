(function () {
    'use strict';

    var prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

    function initRevealAnimations() {
        if (prefersReducedMotion) {
            var allReveals = document.querySelectorAll('.reveal');
            for (var i = 0; i < allReveals.length; i++) {
                allReveals[i].classList.add('visible');
            }
            return;
        }

        var observerOptions = {
            root: null,
            rootMargin: '0px 0px -80px 0px',
            threshold: 0.04,
        };

        var observer = new IntersectionObserver(function (entries) {
            entries.forEach(function (entry) {
                if (entry.isIntersecting) {
                    var delay = entry.target.getAttribute('data-delay');
                    if (delay) {
                        setTimeout(function () {
                            entry.target.classList.add('visible');
                        }, parseInt(delay, 10));
                    } else {
                        entry.target.classList.add('visible');
                    }
                    observer.unobserve(entry.target);
                }
            });
        }, observerOptions);

        var elements = document.querySelectorAll('.reveal');
        for (var i = 0; i < elements.length; i++) {
            observer.observe(elements[i]);
        }
    }

    function initParallaxOrbs() {
        if (prefersReducedMotion) return;

        var parallaxElements = document.querySelectorAll('[data-parallax]');

        function updateParallax() {
            var scrollY = window.scrollY;
            for (var i = 0; i < parallaxElements.length; i++) {
                var speed = parseFloat(parallaxElements[i].getAttribute('data-parallax')) || 0.04;
                var offset = scrollY * speed;
                parallaxElements[i].style.transform = 'translateY(' + offset + 'px)';
            }
        }

        var ticking = false;
        window.addEventListener('scroll', function () {
            if (!ticking) {
                requestAnimationFrame(function () {
                    updateParallax();
                    ticking = false;
                });
                ticking = true;
            }
        }, { passive: true });
    }

    function initMagneticButtons() {
        if (prefersReducedMotion) return;

        var buttons = document.querySelectorAll('.magnetic');

        for (var i = 0; i < buttons.length; i++) {
            (function (btn) {
                btn.addEventListener('mousemove', function (e) {
                    var rect = btn.getBoundingClientRect();
                    var x = e.clientX - rect.left - rect.width / 2;
                    var y = e.clientY - rect.top - rect.height / 2;
                    btn.style.transform = 'translate(' + (x * 0.1) + 'px, ' + (y * 0.1) + 'px)';
                });

                btn.addEventListener('mouseleave', function () {
                    btn.style.transform = 'translate(0px, 0px)';
                });
            })(buttons[i]);
        }
    }

    function initSmoothScroll() {
        var anchors = document.querySelectorAll('a[href^="#"]');
        for (var i = 0; i < anchors.length; i++) {
            anchors[i].addEventListener('click', function (e) {
                var targetId = this.getAttribute('href');
                if (targetId === '#') return;
                var target = document.querySelector(targetId);
                if (target) {
                    e.preventDefault();
                    target.scrollIntoView({ behavior: 'smooth', block: 'start' });
                }
            });
        }
    }

    function initMobileMenu() {
        var toggle = document.getElementById('mobile-menu-toggle');
        var menu = document.getElementById('mobile-menu');
        if (!toggle || !menu) return;

        var spans = toggle.querySelectorAll('span');
        var links = menu.querySelectorAll('a');
        var isOpen = false;

        function openMenu() {
            isOpen = true;
            menu.classList.remove('invisible', 'opacity-0', 'pointer-events-none');
            menu.classList.add('opacity-100', 'visible', 'pointer-events-auto');
            spans[0].style.transform = 'translateY(7px) rotate(45deg)';
            spans[1].style.opacity = '0';
            spans[2].style.transform = 'translateY(-7px) rotate(-45deg)';
            toggle.setAttribute('aria-expanded', 'true');
            document.body.style.overflow = 'hidden';
            if (links.length > 0) links[0].focus();
        }

        function closeMenu() {
            isOpen = false;
            menu.classList.add('invisible', 'opacity-0', 'pointer-events-none');
            menu.classList.remove('opacity-100', 'visible', 'pointer-events-auto');
            spans[0].style.transform = '';
            spans[1].style.opacity = '';
            spans[2].style.transform = '';
            toggle.setAttribute('aria-expanded', 'false');
            document.body.style.overflow = '';
            toggle.focus();
        }

        toggle.addEventListener('click', function () {
            if (isOpen) closeMenu();
            else openMenu();
        });

        for (var i = 0; i < links.length; i++) {
            links[i].addEventListener('click', closeMenu);
        }

        menu.addEventListener('click', function (e) {
            if (e.target === menu) closeMenu();
        });
    }

    function initFocusTrap() {
        document.addEventListener('keydown', function (e) {
            if (e.key === 'Escape') {
                var mobileMenu = document.getElementById('mobile-menu');
                var toggle = document.getElementById('mobile-menu-toggle');
                if (mobileMenu && !mobileMenu.classList.contains('invisible') && toggle) {
                    toggle.click();
                }
            }
        });
    }

    document.addEventListener('DOMContentLoaded', function () {
        initRevealAnimations();
        initParallaxOrbs();
        initMagneticButtons();
        initSmoothScroll();
        initMobileMenu();
        initFocusTrap();
    });
})();
