const GAME_STATE = {

    score: 0,

    lives: 3,

    time: 90,

    completed: false,

    gameOver: false,

    started: false,

    level: 1
};


function resetGameState() {

    GAME_STATE.score = 0;

    GAME_STATE.lives =
        GAME_SETTINGS.startingLives;

    GAME_STATE.time =
        GAME_SETTINGS.startingTime;

    GAME_STATE.completed = false;

    GAME_STATE.gameOver = false;

    GAME_STATE.started = false;
}
