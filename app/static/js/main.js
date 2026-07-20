// app/static/js/main.js

(function () {
    'use strict';

    function initBackToTop() {
        const btn = document.getElementById('back-to-top');
        if (!btn) return;

        let ticking = false;
        function update() {
            if (window.scrollY > 600) {
                btn.classList.remove('opacity-0', 'invisible', 'translate-y-4', 'pointer-events-none');
                btn.classList.add('opacity-100', 'visible', 'translate-y-0', 'pointer-events-auto');
            } else {
                btn.classList.add('opacity-0', 'invisible', 'translate-y-4', 'pointer-events-none');
                btn.classList.remove('opacity-100', 'visible', 'translate-y-0', 'pointer-events-auto');
            }
        }

        window.addEventListener('scroll', () => {
            if (!ticking) {
                requestAnimationFrame(() => { update(); ticking = false; });
                ticking = true;
            }
        }, { passive: true });

        btn.addEventListener('click', () => window.scrollTo({ top: 0, behavior: 'smooth' }));
    }

    function initSmoothScroll() {
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {
            anchor.addEventListener('click', function (e) {
                const id = this.getAttribute('href');(function () {
    'use strict';

    function initBackToTop() {
        var button = document.getElementById('back-to-top');
        if (!button) return;

        var scrollTimeout;
        function handleScroll() {
            if (window.scrollY > 800) {
                button.classList.remove('opacity-0', 'invisible', 'translate-y-4', 'pointer-events-none');
                button.classList.add('opacity-100', 'visible', 'translate-y-0', 'pointer-events-auto');
            } else {
                button.classList.add('opacity-0', 'invisible', 'translate-y-4', 'pointer-events-none');
                button.classList.remove('opacity-100', 'visible', 'translate-y-0', 'pointer-events-auto');
            }
        }

        window.addEventListener('scroll', function () {
            if (scrollTimeout) window.cancelAnimationFrame(scrollTimeout);
            scrollTimeout = window.requestAnimationFrame(handleScroll);
        }, { passive: true });

        button.addEventListener('click', function () {
            window.scrollTo({ top: 0, behavior: 'smooth' });
        });
    }

    document.addEventListener('DOMContentLoaded', initBackToTop);
})();
                if (id === '#') return;
                const target = document.querySelector(id);
                if (target) {
                    e.preventDefault();
                    target.scrollIntoView({ behavior: 'smooth', block: 'start' });
                }
            });
        });
    }

    document.addEventListener('DOMContentLoaded', () => {
        initBackToTop();
        initSmoothScroll();
    });
})();