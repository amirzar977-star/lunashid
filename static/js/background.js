const backgroundLayer = document.getElementById("backgroundLayer");
const backgroundInput = document.getElementById("backgroundInput");
const heroBackgroundInput = document.getElementById("heroBackgroundInput");

function applyBackground(file) {

    if (!file || !file.type.startsWith("image/")) return;

    const reader = new FileReader();

    reader.onload = function (event) {

        const image = event.target.result;

        backgroundLayer.style.backgroundImage =
            `url("${image}")`;

        backgroundLayer.style.opacity = "1";

        try {
            localStorage.setItem(
                "lunashidBackground",
                image
            );
        } catch (error) {
            console.warn("تصویر برای localStorage بزرگ است.");
        }
    };

    reader.readAsDataURL(file);
}


if (backgroundInput) {
    backgroundInput.addEventListener(
        "change",
        function () {
            applyBackground(this.files[0]);
        }
    );
}


if (heroBackgroundInput) {
    heroBackgroundInput.addEventListener(
        "change",
        function () {
            applyBackground(this.files[0]);
        }
    );
}


/* بازیابی تصویر قبلی */

const savedBackground =
    localStorage.getItem("lunashidBackground");

if (savedBackground && backgroundLayer) {

    backgroundLayer.style.backgroundImage =
        `url("${savedBackground}")`;

    backgroundLayer.style.opacity = "1";
}


/* شمارنده سبد */

const cartCount =
    document.getElementById("cartCount");

if (cartCount) {

    try {

        const cart =
            JSON.parse(
                localStorage.getItem("cart") || "[]"
            );

        cartCount.textContent = cart.length;

    } catch {

        cartCount.textContent = "0";
    }
}
