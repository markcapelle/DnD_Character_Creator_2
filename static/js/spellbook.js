document.addEventListener("DOMContentLoaded", () => {
    const pages = Array.from(document.querySelectorAll(".spell-page"));
    let index = 0;

    function showPage(i) {
        pages.forEach((p, n) => {
            p.style.display = n === i ? "block" : "none";
        });
    }

    // Initial display
    showPage(index);

    // Button navigation
    document.getElementById("next-spell").addEventListener("click", () => {
        playPageFlip();
        index = (index + 1) % pages.length;
        showPage(index);
    });
    
    document.getElementById("prev-spell").addEventListener("click", () => {
        playPageFlip();
        index = (index - 1 + pages.length) % pages.length;
        showPage(index);
    });
    
    // Keyboard navigation
    document.addEventListener("keydown", (e) => {
        if (e.key === "ArrowRight") {
            playPageFlip();
            index = (index + 1) % pages.length;
            showPage(index);
        }
        if (e.key === "ArrowLeft") {
            playPageFlip();
            index = (index - 1 + pages.length) % pages.length;
            showPage(index);
        }
    });
});