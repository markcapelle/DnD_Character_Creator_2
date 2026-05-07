// Abilities.html Next/Back Buttons
const abilitiesNext = document.getElementById("abilities-next-button");
if (abilitiesNext) {
    abilitiesNext.addEventListener("click", () => {
        fetch("/commit_character", { method: "POST" })
            .then(r => r.json())
            .then(data => {
                if (data.success) {
                    window.location.href = "/skills";
                }
            });
    });
}

// Skills.html Next/Back Buttons
const skillsBack = document.getElementById("skills-back-button");
if (skillsBack) {
    skillsBack.addEventListener("click", () => {
        window.location.href = "/";
    });
}

const skillsNext = document.getElementById("skills-next-button");
if (skillsNext) {
    skillsNext.addEventListener("click", () => {

        // 1. Collect selected skills
        const selectedSkills = [...document.querySelectorAll(".skill-checkbox")]
            .filter(cb => cb.checked)
            .map(cb => cb.value);

        // 2. Send selected skills to backend
        fetch("/set_skills", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ skills: selectedSkills })
        })
        .then(r => r.json())
        .then(data => {
            if (!data.success) return;

            // 3. Commit full character sheet
            return fetch("/commit_character", { method: "POST" });
        })
        .then(r => r.json())
        .then(data => {
            if (data.success) {
                // 4. Move on to background
                window.location.href = "/background";
            }
        });
    });
}

// Background.html Next/Back Buttons
const backgroundBack = document.getElementById("background-back-button");
if (backgroundBack) {
    backgroundBack.addEventListener("click", () => {
        window.location.href = "/skills";
    });
}

const backgroundNext = document.getElementById("background-next-button");
if (backgroundNext) {

    const select = document.getElementById("backgroundSelect");

    function checkBackgroundReady() {
        fetch("/background_ready")
            .then(r => r.json())
            .then(data => {
                backgroundNext.disabled = !data.ready;
                backgroundNext.classList.toggle("next-disabled", !data.ready);
            });
    }

    if (select) {
        select.addEventListener("change", () => {
            const chosen = select.value;

            if (chosen) {
                fetch("/set_background", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ background: chosen })
                }).then(() => checkBackgroundReady());
            } else {
                checkBackgroundReady();
            }
        });
    }

    // Initial check
    checkBackgroundReady();

    // Next button → finalize page
    backgroundNext.addEventListener("click", () => {
        window.location.href = "/index";
    });
}





// Open dice button
function openDice() {
    window.open(
        "/dice", 
        "diceWindow",
        "width=400,height=600,resizable=yes"
    );
}




// Reset button
document.addEventListener("DOMContentLoaded", () => {
    const resetBtn = document.getElementById("reset-character");
    if (!resetBtn) return;

    resetBtn.addEventListener("click", () => {
        fetch("/reset", {
            method: "POST"
        })
        .then(res => res.json())
        .then(data => {
            if (data.success) {
                window.location.href = "/";  // send user back to start
            }
        });
    });
});




// If the class is a spellcaster, reveal spellbook button.
document.addEventListener("DOMContentLoaded", () => {
    const spellData = document.getElementById("spellcasting-data");
    if (!spellData) return;  // <-- prevents errors on pages without spellcasting data

    const isSpellcaster = spellData.dataset.spellcaster.toLowerCase() === "true";
    const spellbookName = spellData.dataset.spellbook;
    const primaryAbility = spellData.dataset.primary;

    const btn = document.getElementById("open-spellbook");
    const windowEl = document.getElementById("spellbook-window");
    const contentEl = document.getElementById("spellbook-content");

    if (isSpellcaster) {
        btn.style.display = "inline-block";
    }

    btn.addEventListener("click", () => {
        window.open(
            "/spellbook",
            "SpellbookWindow",
            "width=650,height=600,resizable=yes"
        );
    });
});



