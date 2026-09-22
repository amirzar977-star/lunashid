document.addEventListener("DOMContentLoaded", () => {

    const cartCount = document.getElementById("cartCount");
    const cartItems = document.getElementById("cartItems");

    function getCart() {
        try {
            return JSON.parse(localStorage.getItem("cart") || "[]");
        } catch {
            return [];
        }
    }

    function saveCart(cart) {
        localStorage.setItem("cart", JSON.stringify(cart));
    }

    function updateCartCount() {
        if (!cartCount) return;

        const cart = getCart();
        cartCount.textContent = cart.length;
    }

    document.querySelectorAll(".add-to-cart").forEach(button => {

        button.addEventListener("click", () => {

            const product = {
                id: Number(button.dataset.id),
                name: button.dataset.name,
                price: Number(button.dataset.price),
                image: button.dataset.image
            };

            const cart = getCart();

            const exists = cart.find(item => item.id === product.id);

            if (!exists) {
                cart.push(product);
                saveCart(cart);
            }

            updateCartCount();

            const original = button.innerHTML;

            button.innerHTML = "به سبد اضافه شد ✓";

            setTimeout(() => {
                button.innerHTML = original;
            }, 1300);

        });

    });


    function renderCart() {

        if (!cartItems) return;

        const cart = getCart();

        if (!cart.length) {

            cartItems.innerHTML = `
                <div style="
                    min-height:180px;
                    display:flex;
                    align-items:center;
                    justify-content:center;
                    flex-direction:column;
                    gap:15px;
                    text-align:center;
                ">
                    <strong style="color:#57715f;font-size:18px">
                        سبد خرید خالی است
                    </strong>

                    <span style="color:#89958d;font-size:12px">
                        هنوز قطعه‌ای انتخاب نکرده‌اید.
                    </span>

                    <a
                        href="/products"
                        class="primary-button"
                        style="margin-top:8px"
                    >
                        مشاهده محصولات
                    </a>
                </div>
            `;

            return;
        }

        cartItems.innerHTML = `
            <div style="
                display:flex;
                flex-direction:column;
                gap:12px;
            ">

                ${cart.map((item, index) => `

                    <div style="
                        display:flex;
                        align-items:center;
                        justify-content:space-between;
                        gap:15px;
                        padding:15px;
                        border-radius:20px;
                        background:rgba(255,255,255,.25);
                        border:1px solid rgba(255,255,255,.55);
                    ">

                        <div style="
                            display:flex;
                            align-items:center;
                            gap:14px;
                        ">

                            <img
                                src="/static/images/${item.image}"
                                style="
                                    width:65px;
                                    height:65px;
                                    border-radius:16px;
                                    object-fit:cover;
                                "
                            >

                            <div>
                                <strong style="
                                    display:block;
                                    color:#506b5a;
                                    font-size:13px;
                                ">
                                    ${item.name}
                                </strong>

                                <span style="
                                    display:block;
                                    margin-top:5px;
                                    color:#789080;
                                    font-size:11px;
                                ">
                                    ${item.price.toLocaleString("fa-IR")} تومان
                                </span>
                            </div>

                        </div>

                        <button
                            data-index="${index}"
                            class="remove-cart"
                            style="
                                border:1px solid rgba(255,255,255,.65);
                                background:rgba(255,255,255,.3);
                                color:#70907d;
                                border-radius:12px;
                                padding:9px 13px;
                                cursor:pointer;
                                font-family:inherit;
                                font-size:10px;
                            "
                        >
                            حذف
                        </button>

                    </div>

                `).join("")}

            </div>
        `;

        document.querySelectorAll(".remove-cart").forEach(button => {

            button.addEventListener("click", () => {

                const cart = getCart();

                cart.splice(Number(button.dataset.index), 1);

                saveCart(cart);

                updateCartCount();
                renderCart();

            });

        });

    }

    updateCartCount();
    renderCart();

});
