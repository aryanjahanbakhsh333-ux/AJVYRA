const SAVE_KEY = "AJVYRA_BLACK_RUN";

function saveGame() {

    const data = {
        highScore: GAME_STATE.score,
        completed: GAME_STATE.completed
    };

    localStorage.setItem(
        SAVE_KEY,
        JSON.stringify(data)
    );
}

function loadGame() {

    const saved =
        localStorage.getItem(SAVE_KEY);

    if (!saved) {
        return {
            highScore: 0,
            completed: false
        };
    }

    try {

        return JSON.parse(saved);

    } catch {

        return {
            highScore: 0,
            completed: false
        };
    }
}

function getHighScore() {

    const data = loadGame();

    return Number(data.highScore) || 0;
}
