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
    raceSelect.addEventListener("change", () => {
        const key = raceSelect.value;

        if (!key) {
            raceInfoBox.innerHTML = "";
            return;
        }

        fetch(`/api/race/${key}`)
            .then(res => res.json())
            .then(data => {
                if (data.error) {
                    raceInfoBox.innerHTML = "<em>Race not found.</em>";
                    return;
                }

                let html = `
                    <strong>${data.name}</strong><br>
                    <p>${data.description}</p>

                    <h4>Traits</h4>
                    <ul>
                        ${data.traits.map(t => `<li>${t}</li>`).join("")}
                    </ul>

                    <h4>Ability Modifiers</h4>
                    <ul>
                        ${data.modifiers.map(m => `<li>${m.ability}: +${m.value}</li>`).join("")}
                    </ul>
                `;

                raceInfoBox.innerHTML = html;
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
    

});
