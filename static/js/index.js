
document.addEventListener("DOMContentLoaded", () => {
    // LOAD CHARACTER
    document.querySelectorAll(".load-btn").forEach(btn => {
        btn.addEventListener("click", (e) => {
            playPageFlip();
            const row = e.target.closest("tr");
            const characterId = row.dataset.characterId;
            window.location.href = `/character/${characterId}`;
        });
    });

    // DELETE CHARACTER
    document.querySelectorAll(".delete-btn").forEach(btn => {
        btn.addEventListener("click", async (e) => {
            const row = e.target.closest("tr");
            const characterId = row.dataset.characterId;

            const confirmed = confirm("Are you sure you want to delete this character?");
            if (!confirmed) return;

            playTear();
            
            const res = await fetch(`/delete_character/${characterId}`, {
                method: "DELETE"
            });

            if (res.ok) {
                row.remove();
            }
        });
    });

    // CREATE CHARACTER
    document.getElementById("new-character-btn").addEventListener("click", () => {
        playPageFlip();

        setTimeout(() => {
            window.location.href = "/create_character";
        }, 500); // half‑second delay
    });

});
