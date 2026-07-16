/* Frontend Interactivity for Industry Theme Engine */
document.addEventListener("DOMContentLoaded", function () {
    // 1. Hide Page Loader
    const loader = document.querySelector(".industry-theme-loader");
    if (loader) {
        setTimeout(function () {
            loader.classList.add("loaded");
        }, 500); // Small delay to guarantee smoothness
    }

    // 2. Back to Top Button
    const backToTopBtn = document.querySelector(".industry-theme-back-to-top");
    if (backToTopBtn) {
        window.addEventListener("scroll", function () {
            if (window.scrollY > 300) {
                backToTopBtn.classList.add("visible");
            } else {
                backToTopBtn.classList.remove("visible");
            }
        });

        backToTopBtn.addEventListener("click", function (e) {
            e.preventDefault();
            window.scrollTo({
                top: 0,
                behavior: "smooth"
            });
        });
    }
});
