document.addEventListener("DOMContentLoaded", () => {
    const pages = Array.from(document.querySelectorAll(".spell-page"));
    const pipContainer = document.getElementById("spellbook-pips");
    let index = 0;

    // Create pips dynamically
    pages.forEach((_, i) => {
        const pip = document.createElement("div");
        pip.classList.add("pip");
        pip.dataset.index = i;

        pip.addEventListener("click", () => {
            index = i;
            showPage(index);
        });

        pipContainer.appendChild(pip);
    });

    function updatePips() {
        const pips = pipContainer.querySelectorAll(".pip");
        pips.forEach((pip, i) => {
            pip.classList.toggle("active", i === index);
        });
    }

    function showPage(i) {
        pages.forEach((p, idx) => {
            p.style.display = idx === i ? "block" : "none";
        });

        playPageFlip();
        updatePips();
    }

    // Button navigation
    document.getElementById("next-spell").addEventListener("click", () => {
        index = (index + 1) % pages.length;
        showPage(index);
    });

    document.getElementById("prev-spell").addEventListener("click", () => {
        index = (index - 1 + pages.length) % pages.length;
        showPage(index);
    });

    // Keyboard navigation
    document.addEventListener("keydown", (event) => {
        switch (event.key) {
            case "ArrowRight":
                index = (index + 1) % pages.length;
                showPage(index);
                break;

            case "ArrowLeft":
                index = (index - 1 + pages.length) % pages.length;
                showPage(index);
                break;

            case "Escape":
                window.close();
                break;
        }
    });

    // Show first page initially
    showPage(index);
});
