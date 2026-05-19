
document.addEventListener("DOMContentLoaded", () => {
    // LOAD CHARACTER
    document.querySelectorAll(".load-btn").forEach(btn => {
        btn.addEventListener("click", (e) => {
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

            const res = await fetch(`/delete_character/${characterId}`, {
                method: "DELETE"
            });

            if (res.ok) {
                row.remove();
            }
        });
    });
});
