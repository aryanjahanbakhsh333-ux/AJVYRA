const LEVEL_MANAGER = {
    currentLevel: 1,
    unlockedLevels: [1]
};

function loadLevel(level) {

    LEVEL_MANAGER.currentLevel = level;

    GAME_STATE.level = level;

    GAME_STATE.completed = false;
    GAME_STATE.gameOver = false;

    return level;
}

function unlockLevel(level) {

    if (
        !LEVEL_MANAGER.unlockedLevels.includes(level)
    ) {

        LEVEL_MANAGER.unlockedLevels.push(level);
    }
}

function isLevelUnlocked(level) {

    return LEVEL_MANAGER.unlockedLevels.includes(level);
}
