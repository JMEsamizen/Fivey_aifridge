const products = document.querySelectorAll(".fridge-product");

products.forEach((product) => {
    product.addEventListener("click", (event) => {
        if (event.target.closest(".product-action")) {
            event.stopPropagation();
            return;
        }

        event.stopPropagation();
        const wasOpen = product.classList.contains("active");

        products.forEach((item) => item.classList.remove("active"));
        if (!wasOpen) product.classList.add("active");
    });

    product.addEventListener("keydown", (event) => {
        if (event.key === "Enter" || event.key === " ") {
            event.preventDefault();
            product.click();
        }
    });
});

document.addEventListener("click", () => {
    products.forEach((product) => product.classList.remove("active"));
});
