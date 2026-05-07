function updateUI(data) {   // Update stats on the page without refreshing
        document.getElementById("points").textContent = data.points_pool;

        for (const [key, val] of Object.entries(data.abilities)) {
            document.getElementById(key).textContent = val;
        }
    }

function change(ability, action) {
    playScribble();
    fetch("/" + action, {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({ ability })
    })
    .then(r => r.json())
    .then(data => {
        updateUI(data);
        checkReady();
    });
}

function selectRace(race) {
    fetch("/select_race", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({ race })
    })
    .then(r => r.json())
    .then(data => {
        const mods = data.modifiers;

        // Clear all modifiers
        const abilities = ["strength","dexterity","constitution","intelligence","wisdom","charisma"];
        abilities.forEach(a => {
            document.getElementById(a + "-mod").textContent = "";
        });

        // Apply new modifiers
        for (const [ability, bonus] of Object.entries(mods)) {
            const el = document.getElementById(ability + "-mod");
            if (el) {
                el.textContent = ` (${data.race} + ${bonus})`;
            }
        }

        // Update race info
        const raceInfo = document.getElementById("race-info");

        if (!data.race) {
            raceInfo.innerHTML = "";
            checkReady();
            return;
        }

        let traitsHTML = "";
        if (data.traits && data.traits.length > 0) {
            traitsHTML = `
                <strong>Traits:</strong>
                <ul>${data.traits.map(t => `<li>${t}</li>`).join("")}</ul>
            `;
        }

        raceInfo.innerHTML = `
            <strong>${data.race.toUpperCase()}</strong><br>
            ${data.description}<br><br>
            ${traitsHTML}
        `;

        checkReady();   // Run check AFTER backend update
    });
}

   
function selectClass(className) {
    fetch("/select_class", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({ class: className })
    })
    .then(r => r.json())
    .then(data => {
        const classInfo = document.getElementById("class-info");

        // If no class selected, clear everything and stop
        if (!data.class) {
            classInfo.innerHTML = "";
            checkReady();
            return;
        }

        // Build primary abilities list
        const primaryList = data.primary_abilities
            .map(a => a.charAt(0).toUpperCase() + a.slice(1))
            .join(", ");

        // Build class features block
        let featuresHTML = "";
        if (data.class_features) {
            if (Array.isArray(data.class_features)) {
                featuresHTML = `
                    <strong>Class Features:</strong>
                    <ul>${data.class_features.map(f => `<li>${f}</li>`).join("")}</ul>
                `;
            } else {
                featuresHTML = `
                    <strong>Class Features:</strong>
                    <p>${data.class_features}</p>
                `;
            }
        }

        // Final HTML block
        classInfo.innerHTML = `
            <strong>${data.class.toUpperCase()}</strong><br>
            ${data.description}<br><br>

            <strong>Primary Abilities:</strong> ${primaryList}<br><br>

            ${featuresHTML}
        `;

        checkReady();
    });
}

function checkReady() {
    fetch("/is_ready")
        .then(r => r.json())
        .then(data => {
            console.log("READY CHECK:", data);

            const btn = document.getElementById("abilities-next-button");

            if (data.ready) {
                btn.disabled = false;
                btn.classList.remove("next-disabled");
                btn.classList.add("next-enabled");
            } else {
                btn.disabled = true;
                btn.classList.remove("next-enabled");
                btn.classList.add("next-disabled");
            }
        });
}






