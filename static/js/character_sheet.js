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
        updateSpellSlotsUI(used);
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

// Open notebook button
function openNotebook(characterId) {
    window.open(
        `/notebook/${characterId}`,
        "notebookWindow",
        "width=900,height=700,resizable=yes"
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
let hpQueue = 0;
let hpTimer = null;

function adjustHP(direction) {
    // Convert direction to +1 or -1
    hpQueue += direction === "plus" ? 1 : -1;

    // Update UI instantly
    const display = document.getElementById("current-hp-display");
    const current = parseInt(display.textContent, 10);
    display.textContent = current + (direction === "plus" ? 1 : -1);

    // Reset timer
    clearTimeout(hpTimer);

    // Batch send after 150ms of no clicking
    hpTimer = setTimeout(() => {
        const amount = hpQueue;
        hpQueue = 0;

        fetch(`/hp/batch`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ delta: amount })
        })
        .then(res => res.json())
        .then(data => {
            display.textContent = data.current_hp;
        })
        .catch(err => console.error("HP batch update failed:", err));
    }, 150);
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
        box.classList.toggle("active");

        // Count how many are active
        const activeCount = document.querySelectorAll(".spellslot-box.active").length;

        // Send active count to backend
        fetch(`/spellslot/${activeCount}`, { method: "POST" })
            .then(res => res.json())
            .then(data => {
                updateSpellSlotsUI(data.current_spellslots);
            })
            .catch(err => console.error("Spell slot update failed:", err));
    });
});

function updateSpellSlotsUI(remaining) {
    const boxes = document.querySelectorAll(".spellslot-box");
    const max = boxes.length;

    const spent = max - remaining;

    boxes.forEach((box, i) => {
        box.classList.toggle("active", i < spent);
    });
}