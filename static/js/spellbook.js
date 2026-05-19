document.addEventListener("DOMContentLoaded", () => {
    const pages = Array.from(document.querySelectorAll(".spell-page"));
    let index = 0;

    function showPage(i) {
        pages.forEach((p, idx) => {
            p.style.display = idx === i ? "block" : "none";
        });
    }

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