document.addEventListener("DOMContentLoaded", () => {

    // DOM references
    const raceSelect = document.getElementById("race-select");
    const raceInfoBox = document.getElementById("race-info");
    
    const classSelect = document.getElementById("class-select");
    const classInfoBox = document.getElementById("class-info");

    const backgroundSelect = document.getElementById("background-select");
    const backgroundInfoBox = document.getElementById("background-info");

    const skillCheckboxes = document.querySelectorAll(".skill-checkbox");

    // State
    let maxClassSkills = 0;
    let backgroundSkills = [];

    
    // RACE SELECTION
    let racialModifiers = {};  // ability → value

    raceSelect.addEventListener("change", () => {
        const key = raceSelect.value;

        if (!key) {
            raceInfoBox.innerHTML = "";
            racialModifiers = {};
            updateFinalScores();
            return;
        }

        fetch(`/api/race/${key}`)
            .then(res => res.json())
            .then(data => {
                if (data.error) {
                    raceInfoBox.innerHTML = "<em>Race not found.</em>";
                    return;
                }

                // Store modifiers
                racialModifiers = {};
                data.modifiers.forEach(m => {
                    racialModifiers[m.ability.toLowerCase()] = m.value;
                });

                // Render race info (unchanged)
                let html = `
                    <strong>${data.name}</strong><br>
                    <p>${data.description}</p>

                    <h4>Traits</h4>
                    <ul>${data.traits.map(t => `<li>${t}</li>`).join("")}</ul>

                    <h4>Ability Modifiers</h4>
                    <ul>${data.modifiers.map(m => `<li>${m.ability}: +${m.value}</li>`).join("")}</ul>
                `;

                raceInfoBox.innerHTML = html;

                updateFinalScores();
            });
    });



    // CLASS SELECTION
    classSelect.addEventListener("change", () => {
        const key = classSelect.value;

        // Reset everything when class changes
        resetAllSkillSelections();

        // Reset background too
        backgroundSelect.value = "";
        backgroundInfoBox.innerHTML = "";
        backgroundSkills = [];

        maxClassSkills = 0;
        classInfoBox.innerHTML = "";

        if (!key) return;

        fetch(`/api/class/${key}`)
            .then(res => res.json())
            .then(data => {
                if (data.error) {
                    classInfoBox.innerHTML = "<em>Class not found.</em>";
                    return;
                }

                maxClassSkills = data.skill_choices;

                let html = `
                    <strong>${data.name}</strong><br>
                    <p>${data.description}</p>

                    <h4>Hit Die</h4>
                    <p>${data.hit_die}</p>

                    <h4>Saving Throws</h4>
                    <ul>${data.saves.map(s => `<li>${s}</li>`).join("")}</ul>

                    <h4>Primary Abilities</h4>
                    <ul>${data.abilities.map(a => `<li>${a}</li>`).join("")}</ul>

                    <h4>Class Features</h4>
                    <ul>
                        ${data.features.map(f => `<li><strong>${f.name}</strong>: ${f.description}</li>`).join("")}
                    </ul>

                    <h4>Available Skills</h4>
                    <ul>
                        ${data.class_skills.map(s => `<li>${s}</li>`).join("")}
                    </ul>

                    <p><strong>You may choose ${data.skill_choices} class skills.</strong></p>
                `;

                classInfoBox.innerHTML = html;

                enableSkillSelectionIfReady();
            });
    });




    // BACKGROUND SELECTION
    backgroundSelect.addEventListener("change", () => {
        const key = backgroundSelect.value;

        resetAllSkillSelections();

        if (!key) {
            backgroundInfoBox.innerHTML = "";
            backgroundSkills = [];
            return;
        }

        fetch(`/api/background/${key}`)
            .then(res => res.json())
            .then(data => {
                if (data.error) {
                    backgroundInfoBox.innerHTML = "<em>Background not found.</em>";
                    return;
                }

                backgroundSkills = data.proficiencies;

                let html = `
                    <strong>${data.name}</strong><br>
                    <p>${data.description}</p>

                    <h4>Background Proficiencies</h4>
                    <ul>
                        ${data.proficiencies.map(p => `<li>${p}</li>`).join("")}
                    </ul>
                `;

                backgroundInfoBox.innerHTML = html;

                applyBackgroundSkills();
                enableSkillSelectionIfReady();
            });
    });


    
    // RESET SKILLS
    function resetAllSkillSelections() {
        skillCheckboxes.forEach(cb => {
            cb.checked = false;
            cb.disabled = true;
            cb.classList.remove("skill-background");
            cb.classList.remove("skill-disabled");
        });
    }


    
    // APPLY BACKGROUND SKILLS
    function applyBackgroundSkills() {
        skillCheckboxes.forEach(cb => {
            const skillName = cb.dataset.skillName;

            if (backgroundSkills.includes(skillName)) {
                cb.checked = true;
                cb.disabled = true;
                cb.classList.add("skill-background");
                cb.classList.add("skill-disabled");
            }
        });
    }



    // ENABLE SKILLS ONLY IF BOTH SELECTED
    function enableSkillSelectionIfReady() {
        if (classSelect.value && backgroundSelect.value) {
            skillCheckboxes.forEach(cb => {
                if (!cb.classList.contains("skill-background")) {
                    cb.disabled = false;
                }
            });
        }
    }


    // CLASS SKILL LIMIT ENFORCEMENT
    function enforceSkillLimit() {
        // Count selected class skills (NOT background skills)
        const selected = [...skillCheckboxes].filter(cb =>
            cb.checked && !cb.classList.contains("skill-background")
        );

        if (selected.length >= maxClassSkills) {
            // Disable all unchecked class skills
            skillCheckboxes.forEach(cb => {
                if (!cb.checked && !cb.classList.contains("skill-background")) {
                    cb.disabled = true;
                    cb.classList.add("skill-disabled");
                }
            });
        } else {
            // Re-enable all class skills (unless background)
            skillCheckboxes.forEach(cb => {
                if (!cb.classList.contains("skill-background")) {
                    cb.disabled = false;
                    cb.classList.remove("skill-disabled");
                }
            });
        }
    }

    // Listen for changes
    skillCheckboxes.forEach(cb => {
        cb.addEventListener("change", () => {
            enforceSkillLimit();
        });
    });
    


    // ABILITY SCORE SELECT
    const abilitySelects = document.querySelectorAll(".ability-select");

    // Track which scores are still available
    let availableScores = ["15", "14", "13", "12", "10", "8"];

    // Track assigned scores
    let assignedScores = {
        strength: null,
        dexterity: null,
        constitution: null,
        intelligence: null,
        wisdom: null,
        charisma: null
    };

    abilitySelects.forEach(select => {
        select.addEventListener("change", () => {
            const ability = select.dataset.ability;
            const newValue = select.value;
            const oldValue = assignedScores[ability];

            // 1. Free the old value back into the pool
            if (oldValue) {
                availableScores.push(oldValue);
            }

            // 2. Assign the new value
            assignedScores[ability] = newValue || null;

            // 3. Remove the new value from the pool
            if (newValue) {
                availableScores = availableScores.filter(v => v !== newValue);
            }

            // 4. Update all dropdowns to reflect available scores
            refreshAbilityDropdowns();
            updateFinalScores();
        });
    });

    function refreshAbilityDropdowns() {
        abilitySelects.forEach(select => {
            const ability = select.dataset.ability;
            const currentValue = assignedScores[ability];

            // Rebuild dropdown options
            select.innerHTML = `<option value="">--</option>`;

            // Add available scores
            availableScores.forEach(score => {
                select.innerHTML += `<option value="${score}">${score}</option>`;
            });

            // Re-add the currently selected value (if any)
            if (currentValue) {
                select.innerHTML += `<option value="${currentValue}" selected>${currentValue}</option>`;
            }
        });
    }

    function updateFinalScores() {
        abilitySelects.forEach(select => {
            const ability = select.dataset.ability;
            const base = Number(select.value) || 0;
            const mod = racialModifiers[ability] || 0;
            const finalValue = base + mod;

            const finalSpan = document.getElementById(`final-${ability}`);

            if (base === 0) {
                finalSpan.textContent = "—";
            } else {
                finalSpan.textContent = finalValue;
            }
        });
    }



    // FINAL VALIDATION + CREATE CHARACTER
    const createBtn = document.getElementById("create-character-btn");
    const nameInput = document.getElementById("char-name");

    // Re-run validation whenever anything changes
    nameInput.addEventListener("input", validateReadyState);
    raceSelect.addEventListener("change", validateReadyState);
    classSelect.addEventListener("change", validateReadyState);
    backgroundSelect.addEventListener("change", validateReadyState);
    abilitySelects.forEach(sel => sel.addEventListener("change", validateReadyState));
    skillCheckboxes.forEach(cb => cb.addEventListener("change", validateReadyState));

    function validateReadyState() {
        const nameOK = nameInput.value.trim().length > 0;
        const raceOK = raceSelect.value !== "";
        const classOK = classSelect.value !== "";
        const backgroundOK = backgroundSelect.value !== "";

        // All abilities assigned?
        const abilitiesOK = Object.values(assignedScores).every(v => v !== null);

        // Count class skills (not background)
        const selectedClassSkills = [...skillCheckboxes].filter(cb =>
            cb.checked && !cb.classList.contains("skill-background")
        ).length;

        const skillsOK = selectedClassSkills === maxClassSkills;

        const allOK = nameOK && raceOK && classOK && backgroundOK && abilitiesOK && skillsOK;

        if (allOK) {
            createBtn.disabled = false;
            createBtn.classList.remove("next-disabled");
        } else {
            createBtn.disabled = true;
            createBtn.classList.add("next-disabled");
        }
    }

    createBtn.addEventListener("click", () => {
        if (createBtn.disabled) return;

        const payload = {
            name: nameInput.value.trim(),
            race: raceSelect.value,
            class: classSelect.value,
            background: backgroundSelect.value,
            abilities: assignedScores,
            skills: [...skillCheckboxes]
                .filter(cb => cb.checked)
                .map(cb => Number(cb.dataset.skill))
        };

        fetch("/api/create_character", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payload)
        })
        .then(res => res.json())
        .then(data => {
            if (data.error) {
                alert("Error: " + data.error);
                return;
            }

            // Redirect to character sheet
            window.location.href = `/character/${data.character_id}`;
        });
    });


});
