// Preload audio files
const diceRoll = new Audio("/static/audio/diceroll.mp3");
const pageFlip = new Audio("/static/audio/pageflip.mp3");
const scribble = new Audio("/static/audio/scribble.mp3");
const tear = new Audio("/static/audio/papertear.mp3");

// Ensure they load immediately
diceRoll.preload = "auto";
pageFlip.preload = "auto";
scribble.preload = "auto";
tear.preload = "auto";

// Utility: play from start, once
function playSound(audio) {
    audio.currentTime = 0; // rewind to start
    audio.play();
}

// Public functions
function playDiceRoll() {
    playSound(diceRoll);
}

function playPageFlip() {
    playSound(pageFlip);
}

function playScribble() {
    playSound(scribble);
}

function playTear() {
    playSound(tear);
}