// Increase-Decrease HP.
function changeHP(direction) {
    playScribble();
    fetch(`/hp/${direction}`, { method: "POST" })
        .then(res => res.json())
        .then(data => {
            document.getElementById("hp-display").textContent = `${data.current_hp} / ${data.max_hp}`;
        });
}

// Track user's hit-dice
document.addEventListener("DOMContentLoaded", () => {
    const tracker = document.getElementById("hitdice-tracker");
    const used = Number(tracker.dataset.used);

    updateHitDiceUI(used);

    document.querySelectorAll(".hitdie-box").forEach(box => {
        box.addEventListener("click", () => {
            const index = Number(box.dataset.index);

            // If clicking an active box → untick down to index-1
            // If clicking an inactive box → tick up to index
            let newCount = index;

            if (box.classList.contains("active")) {
                newCount = index - 1;
            }

            fetch("/hitdice/update", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ count: newCount })
            })
            .then(res => res.json())
            .then(data => {
                updateHitDiceUI(data.hit_dice_used);
                tracker.dataset.used = data.hit_dice_used; // keep DOM in sync
            });
        });
    });
});

function updateHitDiceUI(count) {
    playScribble();
    document.querySelectorAll(".hitdie-box").forEach(box => {
        const index = Number(box.dataset.index);
        box.classList.toggle("active", index <= count);
    });
}

// Track user's death rolls
document.addEventListener("DOMContentLoaded", () => {

    // ----- SUCCESS TRACKER -----
    const successTracker = document.getElementById("deathroll-success");
    const successUsed = Number(successTracker.dataset.used);
    updateDeathUI("success", successUsed);

    document.querySelectorAll(".deathroll-box.success").forEach(box => {
        box.addEventListener("click", () => {
            const index = Number(box.dataset.index);

            // If this box is active, clicking it reduces count
            const current = Number(successTracker.dataset.used);
            let newCount = index;

            if (box.classList.contains("active")) {
                newCount = index - 1;
            }

            const delta = newCount - current;

            fetch("/deathroll/update", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ type: "success", delta })
            })
            .then(res => res.json())
            .then(data => {
                successTracker.dataset.used = data.success;
                updateDeathUI("success", data.success);
            });
        });
    });


    // ----- FAIL TRACKER -----
    const failTracker = document.getElementById("deathroll-fail");
    const failUsed = Number(failTracker.dataset.used);
    updateDeathUI("fail", failUsed);

    document.querySelectorAll(".deathroll-box.fail").forEach(box => {
        box.addEventListener("click", () => {
            const index = Number(box.dataset.index);

            const current = Number(failTracker.dataset.used);
            let newCount = index;

            if (box.classList.contains("active")) {
                newCount = index - 1;
            }

            const delta = newCount - current;

            fetch("/deathroll/update", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ type: "fail", delta })
            })
            .then(res => res.json())
            .then(data => {
                failTracker.dataset.used = data.fails;
                updateDeathUI("fail", data.fails);
            });
        });
    });


    // ----- UI UPDATE FUNCTION -----
    function updateDeathUI(type, count) {
        playScribble();
        document.querySelectorAll(`.deathroll-box.${type}`).forEach(box => {
            const index = Number(box.dataset.index);
            box.classList.toggle("active", index <= count);
        });
    }

});

// Track the player's spell slots if the class is a spellcaster.
document.addEventListener("DOMContentLoaded", () => {
    const spellSlotsSection = document.getElementById("spellslots-section");
    if (!spellSlotsSection) return;

    const boxes = spellSlotsSection.querySelectorAll(".spellslot-box");

    boxes.forEach(box => {
        box.addEventListener("click", () => {
            const index = Number(box.dataset.index);

            let newCount = index;
            if (box.classList.contains("active")) {
                newCount = index - 1;
            }

            fetch("/spellslots/update", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ count: newCount })
            })
            .then(res => res.json())
            .then(data => {
                updateSpellSlotUI(data.spell_slots_used);
            });
        });
    });
});

function updateSpellSlotUI(count) {
    playScribble();
    document.querySelectorAll(".spellslot-box").forEach(box => {
        const index = Number(box.dataset.index);
        box.classList.toggle("active", index <= count);
    });
}