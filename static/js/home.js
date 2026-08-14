(function () {
    'use strict';

    var prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

    /* ---------------------------------------------------------
       Navbar: blur/glass on scroll
    --------------------------------------------------------- */
    var navbar = document.getElementById('navbar');

    function onScroll() {
        if (!navbar) return;
        if (window.scrollY > 12) {
            navbar.classList.add('scrolled');
        } else {
            navbar.classList.remove('scrolled');
        }
    }

    window.addEventListener('scroll', onScroll, { passive: true });
    onScroll();

    /* ---------------------------------------------------------
       Mobile nav toggle
    --------------------------------------------------------- */
    var navToggle = document.getElementById('navToggle');
    var navMobile = document.getElementById('navMobile');

    if (navToggle && navMobile) {
        navToggle.addEventListener('click', function () {
            var isOpen = navMobile.classList.toggle('open');
            navToggle.setAttribute('aria-expanded', isOpen ? 'true' : 'false');
        });

        navMobile.querySelectorAll('a').forEach(function (link) {
            link.addEventListener('click', function () {
                navMobile.classList.remove('open');
                navToggle.setAttribute('aria-expanded', 'false');
            });
        });
    }

    /* ---------------------------------------------------------
       Scroll reveal via IntersectionObserver
    --------------------------------------------------------- */
    var revealTargets = document.querySelectorAll('.reveal-on-scroll');

    if ('IntersectionObserver' in window && revealTargets.length) {
        var revealObserver = new IntersectionObserver(function (entries) {
            entries.forEach(function (entry) {
                if (entry.isIntersecting) {
                    entry.target.classList.add('in-view');
                    revealObserver.unobserve(entry.target);
                }
            });
        }, { threshold: 0.15, rootMargin: '0px 0px -40px 0px' });

        revealTargets.forEach(function (el) {
            revealObserver.observe(el);
        });
    } else {
        revealTargets.forEach(function (el) {
            el.classList.add('in-view');
        });
    }

    /* ---------------------------------------------------------
       Readout number count-up (items detected)
    --------------------------------------------------------- */
    var readouts = document.querySelectorAll('.readout-num[data-target]');

    if ('IntersectionObserver' in window && readouts.length) {
        var countObserver = new IntersectionObserver(function (entries) {
            entries.forEach(function (entry) {
                if (!entry.isIntersecting) return;
                var el = entry.target;
                var target = parseInt(el.getAttribute('data-target'), 10) || 0;

                if (prefersReducedMotion) {
                    el.textContent = target;
                    countObserver.unobserve(el);
                    return;
                }

                var start = null;
                var duration = 900;

                function step(ts) {
                    if (start === null) start = ts;
                    var progress = Math.min((ts - start) / duration, 1);
                    var eased = 1 - Math.pow(1 - progress, 3);
                    el.textContent = Math.round(eased * target);
                    if (progress < 1) {
                        requestAnimationFrame(step);
                    }
                }

                requestAnimationFrame(step);
                countObserver.unobserve(el);
            });
        }, { threshold: 0.4 });

        readouts.forEach(function (el) {
            countObserver.observe(el);
        });
    } else {
        readouts.forEach(function (el) {
            el.textContent = el.getAttribute('data-target');
        });
    }

    /* ---------------------------------------------------------
       Subtle mouse parallax on the hero fridge visual
    --------------------------------------------------------- */
    var heroVisual = document.getElementById('heroVisual');
    var fridgeParallax = document.getElementById('fridgeParallax');

    if (heroVisual && fridgeParallax && !prefersReducedMotion && window.matchMedia('(min-width: 981px)').matches) {
        var rafId = null;
        var targetX = 0, targetY = 0, currentX = 0, currentY = 0;

        heroVisual.addEventListener('mousemove', function (e) {
            var rect = heroVisual.getBoundingClientRect();
            var relX = (e.clientX - rect.left) / rect.width - 0.5;
            var relY = (e.clientY - rect.top) / rect.height - 0.5;
            targetX = relX * 10;
            targetY = relY * 10;

            if (!rafId) {
                rafId = requestAnimationFrame(animateParallax);
            }
        });

        heroVisual.addEventListener('mouseleave', function () {
            targetX = 0;
            targetY = 0;
            if (!rafId) {
                rafId = requestAnimationFrame(animateParallax);
            }
        });

        function animateParallax() {
            currentX += (targetX - currentX) * 0.08;
            currentY += (targetY - currentY) * 0.08;

            fridgeParallax.style.transform =
                'rotateY(' + currentX + 'deg) rotateX(' + (-currentY) + 'deg)';

            if (Math.abs(targetX - currentX) > 0.05 || Math.abs(targetY - currentY) > 0.05) {
                rafId = requestAnimationFrame(animateParallax);
            } else {
                rafId = null;
            }
        }
    }

})();
