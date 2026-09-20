const GAME_SESSION = {

    startedAt: 0,

    elapsed: 0,

    attacks: 0,

    enemiesDefeated: 0,

    coinsCollected: 0
};

function startGameSession() {

    GAME_SESSION.startedAt =
        Date.now();

    GAME_SESSION.elapsed = 0;

    GAME_SESSION.attacks = 0;

    GAME_SESSION.enemiesDefeated = 0;

    GAME_SESSION.coinsCollected = 0;
}

function updateGameSession() {

    if (!GAME_SESSION.startedAt) {
        return;
    }

    GAME_SESSION.elapsed =
        Math.floor(
            (Date.now() -
            GAME_SESSION.startedAt) /
            1000
        );
}
