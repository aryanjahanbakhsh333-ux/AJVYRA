const SAVE_KEY = "AJVYRA_BLACK_RUN";


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


function saveGame(score) {

    const oldData =
        loadGame();

    const oldHighScore =
        Number(oldData.highScore) || 0;

    const newHighScore =
        Math.max(
            oldHighScore,
            score
        );

    const data = {

        highScore: newHighScore,

        completed:
            oldData.completed || GAME_STATE.completed
    };

    localStorage.setItem(
        SAVE_KEY,
        JSON.stringify(data)
    );

    return newHighScore;
}
