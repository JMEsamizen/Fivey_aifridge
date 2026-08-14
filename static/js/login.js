/* ==========================================================================
   Fivey Auth - Frost Interactive FX
   ========================================================================== */

document.addEventListener("DOMContentLoaded", () => {

    /* =========================================================
       FROST PARTICLES
    ========================================================= */

    function createFrostParticles() {

        if (document.querySelector(".frost-particles-container")) {
            return;
        }

        const container = document.createElement("div");
        container.className = "frost-particles-container";

        document.body.appendChild(container);

        const particleCount = 20;

        for (let i = 0; i < particleCount; i++) {

            const particle = document.createElement("div");
            particle.className = "frost-particle";

            const size = Math.random() * 5 + 2;

            particle.style.width = `${size}px`;
            particle.style.height = `${size}px`;

            particle.style.left = `${Math.random() * 100}%`;
            particle.style.top = `${Math.random() * 100}%`;

            particle.style.animationDuration =
                `${Math.random() * 8 + 7}s`;

            particle.style.animationDelay =
                `${Math.random() * 5}s`;

            container.appendChild(particle);
        }
    }

    createFrostParticles();


    /* =========================================================
       AUTH CARD 3D EFFECT
    ========================================================= */

    const card = document.querySelector(".auth-card");

    if (card && window.innerWidth > 768) {

        card.addEventListener("mousemove", (event) => {

            const rect = card.getBoundingClientRect();

            const x = event.clientX - rect.left;
            const y = event.clientY - rect.top;

            const centerX = rect.width / 2;
            const centerY = rect.height / 2;

            const rotateY = (x - centerX) / centerX * 6;
            const rotateX = (centerY - y) / centerY * 6;

            card.style.transform =
                `perspective(1000px)
                 rotateX(${rotateX}deg)
                 rotateY(${rotateY}deg)
                 translateY(-3px)`;
        });

        card.addEventListener("mouseleave", () => {

            card.style.transform =
                "perspective(1000px) rotateX(0deg) rotateY(0deg) translateY(0)";

        });
    }


    /* =========================================================
       INPUT INTERACTION
    ========================================================= */

    const inputs = document.querySelectorAll(
        ".input-group input, input"
    );

    inputs.forEach((input) => {

        input.addEventListener("focus", () => {

            const group = input.closest(".input-group");

            if (group) {
                group.classList.add("scanning-active");
            }
        });


        input.addEventListener("blur", () => {

            const group = input.closest(".input-group");

            if (group) {
                group.classList.remove("scanning-active");
            }
        });

    });


    /* =========================================================
       BUTTON LIGHT FOLLOWING CURSOR
    ========================================================= */

    const buttons = document.querySelectorAll(
        ".primary-button, button"
    );

    buttons.forEach((button) => {

        button.addEventListener("mousemove", (event) => {

            const rect = button.getBoundingClientRect();

            const x = event.clientX - rect.left;
            const y = event.clientY - rect.top;

            button.style.setProperty("--mouse-x", `${x}px`);
            button.style.setProperty("--mouse-y", `${y}px`);

        });

    });


    /* =========================================================
       FORM SUBMIT ANIMATION
    ========================================================= */

    const form = document.querySelector("form");

    if (form) {

        form.addEventListener("submit", () => {

            const submitButton =
                form.querySelector(
                    ".primary-button, button[type='submit'], button"
                );

            if (!submitButton) {
                return;
            }

            submitButton.classList.add("authenticating");

            submitButton.disabled = true;

            const text =
                submitButton.querySelector("span");

            if (text) {

                text.dataset.originalText = text.textContent;

                text.textContent = "AUTHENTICATING...";
            }

            /* создаём простой loader */

            const loader =
                document.createElement("span");

            loader.className = "auth-loader";

            submitButton.prepend(loader);
        });

    }


    /* =========================================================
       PAGE FADE-IN
    ========================================================= */

    document.body.classList.add("page-loaded");


    /* =========================================================
       REDUCE MOTION
    ========================================================= */

    const prefersReducedMotion =
        window.matchMedia(
            "(prefers-reduced-motion: reduce)"
        ).matches;

    if (prefersReducedMotion) {

        document
            .querySelectorAll("*")
            .forEach((element) => {

                element.style.animationDuration = "0.01ms";
                element.style.animationIterationCount = "1";
                element.style.transitionDuration = "0.01ms";

            });
    }

});