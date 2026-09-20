const LEVEL_OBJECTIVES = {

    1: {
        requiredCoins: 7,
        requiredEnemies: 0,
        objectiveText: "Collect every energy core."
    },

    2: {
        requiredCoins: 8,
        requiredEnemies: 2,
        objectiveText: "Reach the exit."
    },

    3: {
        requiredCoins: 10,
        requiredEnemies: 4,
        objectiveText: "Survive the shadow zone."
    }
};

function getLevelObjective(level) {

    return (
        LEVEL_OBJECTIVES[level] ||
        LEVEL_OBJECTIVES[1]
    );
}
