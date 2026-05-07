function rollDice(sides) {
    playDiceRoll();
    const count = Number(document.getElementById("dice-count").value);
    const results = [];

    for (let i = 0; i < count; i++) {
        const roll = Math.floor(Math.random() * sides) + 1;
        results.push(roll);
    }

    // Text output
    const output = document.getElementById("dice-output");
    let html = `<strong>Rolling ${count}d${sides}:</strong><br>Results: ${results.join(", ")}`;
    if (count > 1) {
        const total = results.reduce((a, b) => a + b, 0);
        html += `<br>Total: ${total}`;
    }
    output.innerHTML = html;

    // Visual dice
    const visuals = document.getElementById("dice-visuals");
    visuals.innerHTML = "";
    results.forEach(value => {
        const die = document.createElement("div");
        die.className = "die roll";
        die.textContent = value;
        visuals.appendChild(die);
        setTimeout(() => die.classList.remove("roll"), 400);
    });
}
