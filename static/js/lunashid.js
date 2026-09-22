function getCart() {
    try {
        return JSON.parse(localStorage.getItem("lunashidCart") || "[]");
    } catch {
        return [];
    }
}

function saveCart(cart) {
    localStorage.setItem("lunashidCart", JSON.stringify(cart));
    updateCartCount();
}

function updateCartCount() {
    const count = document.getElementById("cartCount");

    if (!count) return;

    const cart = getCart();

    count.textContent = cart.reduce(
        (sum, item) => sum + (item.quantity || 1),
        0
    );
}

function addToCart(button) {

    const id = Number(button.dataset.id);

    const product = {
        id: id,
        name: button.dataset.name,
        price: Number(button.dataset.price),
        image: button.dataset.image || "",
        quantity: 1
    };

    const cart = getCart();

    const existing = cart.find(item => item.id === id);

    if (existing) {
        existing.quantity++;
    } else {
        cart.push(product);
    }

    saveCart(cart);

    button.textContent = "اضافه شد ✓";

    setTimeout(() => {
        button.textContent = "افزودن";
    }, 1000);
}

document.addEventListener("click", function(event) {

    const button = event.target.closest(".add-cart");

    if (button) {
        addToCart(button);
    }

});


function renderCart() {

    const container = document.getElementById("cartItems");

    if (!container) return;

    const cart = getCart();

    if (!cart.length) {

        container.innerHTML = `
            <div class="empty-state">
                سبد خرید هنوز خالی است.
                <br><br>
                <a class="text-link" href="/products">
                    رفتن به محصولات
                </a>
            </div>
        `;

        updateTotal();

        return;
    }

    container.innerHTML = cart.map((item, index) => {

        const image = item.image
            ? `<img src="${item.image}">`
            : `<div class="image-placeholder">Lunashid</div>`;

        return `
            <div class="cart-item">

                ${image}

                <div class="cart-item-info">

                    <h3>
                        ${item.name}
                    </h3>

                    <p>
                        ${Number(item.price).toLocaleString("fa-IR")}
                        تومان
                    </p>

                </div>

                <strong>
                    × ${item.quantity}
                </strong>

                <button
                    class="cart-remove"
                    onclick="removeCartItem(${index})">
                    حذف
                </button>

            </div>
        `;

    }).join("");

    updateTotal();
}


function removeCartItem(index) {

    const cart = getCart();

    cart.splice(index, 1);

    saveCart(cart);

    renderCart();
}


function updateTotal() {

    const totalElement = document.getElementById("cartTotal");

    if (!totalElement) return;

    const cart = getCart();

    const total = cart.reduce(
        (sum, item) =>
            sum + (Number(item.price) * Number(item.quantity || 1)),
        0
    );

    totalElement.textContent =
        total.toLocaleString("fa-IR") + " تومان";
}


function changeProductImage(src) {

    const image = document.getElementById("mainProductImage");

    if (image) {
        image.src = src;
    }
}


function closeCheckout() {

    const modal = document.getElementById("checkoutModal");

    if (modal) {
        modal.classList.remove("show");
    }
}


function openCheckout() {

    const modal = document.getElementById("checkoutModal");

    if (modal) {
        modal.classList.add("show");
    }
}


async function submitOrder() {

    const name = document.getElementById("customerName")?.value.trim();
    const phone = document.getElementById("customerPhone")?.value.trim();

    if (!name || !phone) {
        alert("لطفاً نام و شماره تماس را وارد کنید.");
        return;
    }

    const cart = getCart();

    const total = cart.reduce(
        (sum, item) =>
            sum + Number(item.price) * Number(item.quantity || 1),
        0
    );

    const response = await fetch("/api/order", {

        method: "POST",

        headers: {
            "Content-Type": "application/json"
        },

        body: JSON.stringify({
            name: name,
            phone: phone,
            total: total,
            items: JSON.stringify(cart)
        })

    });

    const data = await response.json();

    if (data.ok) {

        localStorage.removeItem("lunashidCart");

        alert(data.message);

        location.reload();

    } else {

        alert(data.message || "خطایی رخ داد.");

    }
}


document.addEventListener("DOMContentLoaded", function() {

    updateCartCount();

    renderCart();

    const checkout = document.getElementById("checkoutButton");

    if (checkout) {

        checkout.addEventListener("click", function() {

            const cart = getCart();

            if (!cart.length) {

                alert("سبد خرید خالی است.");

                return;
            }

            openCheckout();

        });

    }

});
