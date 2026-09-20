const DIFFICULTY_LEVELS = {

    easy: {
        enemySpeedMultiplier: 0.75,
        enemyHealthMultiplier: 0.75,
        playerDamageMultiplier: 1.25,
        timeMultiplier: 1.3
    },

    normal: {
        enemySpeedMultiplier: 1,
        enemyHealthMultiplier: 1,
        playerDamageMultiplier: 1,
        timeMultiplier: 1
    },

    hard: {
        enemySpeedMultiplier: 1.3,
        enemyHealthMultiplier: 1.4,
        playerDamageMultiplier: 0.85,
        timeMultiplier: 0.8
    }
};


let CURRENT_DIFFICULTY = "normal";


function setDifficulty(level) {

    if (!DIFFICULTY_LEVELS[level]) {
        return false;
    }

    CURRENT_DIFFICULTY = level;

    localStorage.setItem(
        "AJVYRA_BLACK_RUN_DIFFICULTY",
        level
    );

    return true;
}


function getDifficulty() {

    return DIFFICULTY_LEVELS[
        CURRENT_DIFFICULTY
    ];
}


function loadDifficulty() {

    const saved =
        localStorage.getItem(
            "AJVYRA_BLACK_RUN_DIFFICULTY"
        );

    if (
        saved &&
        DIFFICULTY_LEVELS[saved]
    ) {

        CURRENT_DIFFICULTY = saved;
    }
}
