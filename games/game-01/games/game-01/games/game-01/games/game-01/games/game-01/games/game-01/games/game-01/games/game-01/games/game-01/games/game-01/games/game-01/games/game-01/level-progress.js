const LEVEL_PROGRESS = {
    coins: 0,
    enemies: 0,
    objectivesComplete: false
};

function resetLevelProgress() {

    LEVEL_PROGRESS.coins = 0;

    LEVEL_PROGRESS.enemies = 0;

    LEVEL_PROGRESS.objectivesComplete = false;
}

function registerCoinCollected() {

    LEVEL_PROGRESS.coins++;
}

function registerEnemyDefeated() {

    LEVEL_PROGRESS.enemies++;
}

function checkLevelObjectives() {

    const objective =
        getLevelObjective(
            LEVEL_MANAGER.currentLevel
        );

    const coinsReady =
        LEVEL_PROGRESS.coins >=
        objective.requiredCoins;

    const enemiesReady =
        LEVEL_PROGRESS.enemies >=
        objective.requiredEnemies;

    LEVEL_PROGRESS.objectivesComplete =
        coinsReady &&
        enemiesReady;

    return LEVEL_PROGRESS.objectivesComplete;
}
