document.addEventListener("DOMContentLoaded", () => {
    const select = document.getElementById("backgroundSelect");
    const desc = document.getElementById("bgDescription");
    const profList = document.getElementById("bgProficiencies");

    function updateBackgroundInfo() {
        const key = select.value;
        const bg = BACKGROUNDS[key];

        if (!bg) {
            desc.innerText = "";
            profList.innerHTML = "";
            return;
        }

        desc.innerText = bg.description;

        profList.innerHTML = "";
        bg.proficiencies.forEach(p => {
            const li = document.createElement("li");
            li.innerText = p.replace(/_/g, " ");
            profList.appendChild(li);
        });
    }

    select.addEventListener("change", updateBackgroundInfo);
});
