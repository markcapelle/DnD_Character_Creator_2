
// HANDLE DELETE
document.addEventListener("DOMContentLoaded", () => {
    const table = document.getElementById("character-table");

    table.addEventListener("click", async (e) => {
        if (!e.target.classList.contains("delete-btn")) return;

        const row = e.target.closest("tr");
        const characterId = row.dataset.characterId;

        const confirmed = confirm("Are you sure you want to delete this character?");
        if (!confirmed) return;

        const res = await fetch(`/delete_character/${characterId}`, {
            method: "DELETE"
        });

        const data = await res.json();

        if (data.success) {
            row.remove();
        } else {
            alert("Error deleting character.");
        }
    });
});
