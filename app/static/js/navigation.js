(function () {
    'use strict';

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
            if (isOpen) {
                closeMenu();
            } else {
                openMenu();
            }
        });

        for (var i = 0; i < links.length; i++) {
            links[i].addEventListener('click', closeMenu);
        }

        menu.addEventListener('click', function (e) {
            if (e.target === menu) {
                closeMenu();
            }
        });
    }

    function initHeaderScroll() {
        var header = document.getElementById('site-header');
        if (!header) return;

        var scrollTimeout;
        function handleScroll() {
            if (window.scrollY > 50) {
                header.classList.add('glass-strong', 'py-4');
                header.classList.remove('py-6');
            } else {
                header.classList.remove('glass-strong', 'py-4');
                header.classList.add('py-6');
            }
        }

        window.addEventListener('scroll', function () {
            if (scrollTimeout) {
                window.cancelAnimationFrame(scrollTimeout);
            }
            scrollTimeout = window.requestAnimationFrame(handleScroll);
        }, { passive: true });

        handleScroll();
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
        initMobileMenu();
        initHeaderScroll();
        initFocusTrap();
    });
})();