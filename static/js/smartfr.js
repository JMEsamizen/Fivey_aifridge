function showProduct(product) {
    const name = product.dataset.name;
    const quantity = product.dataset.quantity;
    const expireDate = product.dataset.expire;

    document.getElementById("modalProductName").textContent = name;

    document.getElementById("modalQuantity").textContent =
        "×" + quantity;

    document.getElementById("modalExpireDate").textContent =
        expireDate || "Not available";

    document.getElementById("productModal").classList.add("active");
}


function closeProduct() {
    document.getElementById("productModal").classList.remove("active");
}


document.addEventListener("click", function (event) {
    const modal = document.getElementById("productModal");

    if (event.target === modal) {
        closeProduct();
    }
});