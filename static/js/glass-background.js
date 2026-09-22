document.addEventListener("DOMContentLoaded", () => {

    const layer = document.getElementById("backgroundLayer");

    if (!layer) return;

    const saved = localStorage.getItem("lunashidBackground");

    if (saved) {
        layer.style.backgroundImage = `url("${saved}")`;
        layer.style.opacity = "1";
    }

});
