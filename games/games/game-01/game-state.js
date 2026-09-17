const GAME_STATE = {
    score: 0,
    lives: 3,
    time: 60,
    completed: false,
    gameOver: false
};

function resetGameState() {
    GAME_STATE.score = 0;
    GAME_STATE.lives = 3;
    GAME_STATE.time = 60;
    GAME_STATE.completed = false;
    GAME_STATE.gameOver = false;
}
