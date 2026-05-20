// Initialize Trackers UI on page load
document.addEventListener("DOMContentLoaded", () => {
    
    // Hit Dice Initialize
    const hitdiceTracker = document.getElementById("hitdice-tracker");
    if (hitdiceTracker) {
        const remaining = parseInt(hitdiceTracker.dataset.used, 10);
        updateHitDiceUI(remaining);
    }

    // Death Saves Initialize
    const successContainer = document.getElementById("deathroll-success");
    const failContainer = document.getElementById("deathroll-fail");

    if (successContainer && failContainer) {
        const successes = parseInt(successContainer.dataset.used, 10);
        const failures = parseInt(failContainer.dataset.used, 10);

        updateDeathSavesUI(successes, failures);
    }

    // Exaustion Initialize
    const exhaustionTracker = document.getElementById("exhaustion-tracker");
    if (exhaustionTracker) {
        const level = parseInt(exhaustionTracker.dataset.used, 10);
        updateExhaustionUI(level);
    }

    // Spell Slots Initialize
    const spellSection = document.getElementById("spellslots-section");
    if (spellSection) {
        const used = parseInt(spellSection.dataset.used, 10);
        updateSpellSlotsUI(remaining);
    }
});



// Open dice button
function openDice() {
    window.open(
        "/dice", 
        "diceWindow",
        "width=400,height=600,resizable=yes"
    );
}

// Open spellbook button
function openSpellbook(characterId) {
    window.open(
        `/spellbook/${characterId}`,
        "spellbookWindow",
        "width=650,height=600,resizable=yes"
    );
}

// Adjust HP
function adjustHP(direction) {
    fetch(`/hp/${direction}`, { method: "POST" })
        .then(res => res.json())
        .then(data => {
            document.getElementById("current-hp-display").textContent = data.current_hp;
        })
        .catch(err => console.error("HP update failed:", err));
}

// Hit Dice Tracker
document.querySelectorAll(".hitdie-box").forEach(box => {
    box.addEventListener("click", () => {
        fetch(`/hitdice/toggle`, { method: "POST" })
            .then(res => res.json())
            .then(data => {
                updateHitDiceUI(data.hit_dice_remaining);
            })
            .catch(err => console.error("Hit Dice update failed:", err));
    });
});
function updateHitDiceUI(remaining) {
    const box = document.querySelector(".hitdie-box");
    if (!box) return;

    if (remaining === 0) {
        box.classList.add("active");
    } else {
        box.classList.remove("active");
    }
}

// Death Saves Tracker
document.querySelectorAll(".deathroll-box").forEach(box => {
    box.addEventListener("click", () => {
        const type = box.classList.contains("success") ? "success" : "fail";
        const index = parseInt(box.dataset.index, 10);

        fetch(`/deathsave/${type}/${index}`, { method: "POST" })
            .then(res => res.json())
            .then(data => {
                updateDeathSavesUI(data.successes, data.failures);
            })
            .catch(err => console.error("Death save update failed:", err));
    });
});
function updateDeathSavesUI(successes, failures) {
    // Success boxes
    document.querySelectorAll("#deathroll-success .deathroll-box").forEach(box => {
        const idx = parseInt(box.dataset.index, 10);
        box.classList.toggle("active", idx <= successes);
    });

    // Failure boxes
    document.querySelectorAll("#deathroll-fail .deathroll-box").forEach(box => {
        const idx = parseInt(box.dataset.index, 10);
        box.classList.toggle("active", idx <= failures);
    });
}

// Exaustion Tracker
document.querySelectorAll("#exhaustion-tracker .exhaustion-box").forEach(box => {
    box.addEventListener("click", () => {
        const index = parseInt(box.dataset.index, 10);

        fetch(`/exhaustion/${index}`, { method: "POST" })
            .then(res => res.json())
            .then(data => {
                updateExhaustionUI(data.exhaustion);
            })
            .catch(err => console.error("Exhaustion update failed:", err));
    });
});
function updateExhaustionUI(level) {
    document.querySelectorAll("#exhaustion-tracker .exhaustion-box").forEach(box => {
        const idx = parseInt(box.dataset.index, 10);
        box.classList.toggle("active", idx <= level);
    });
}

// Spellslots Tracker
document.querySelectorAll(".spellslot-box").forEach(box => {
    box.addEventListener("click", () => {
        const index = parseInt(box.dataset.index, 10);

        fetch(`/spellslot/${index}`, { method: "POST" })
            .then(res => res.json())
            .then(data => {
                updateSpellSlotsUI(data.current_spellslots);
            })
            .catch(err => console.error("Spell slot update failed:", err));
    });
});
function updateSpellSlotsUI(remaining) {
    const boxes = document.querySelectorAll(".spellslot-box");
    const total = boxes.length;
    const used = total - remaining; // how many have been spent

    boxes.forEach(box => {
        const idx = parseInt(box.dataset.index, 10);
        box.classList.toggle("active", idx <= used);
    });
}