const LOCAL_SAVE_VERSION = 1;

const LOCAL_SAVE_KEY =
    "AJVYRA_BLACK_RUN_PROFILE";


function createSaveSnapshot() {

    return {

        version:
            LOCAL_SAVE_VERSION,

        timestamp:
            Date.now(),

        level:
            LEVEL_MANAGER.currentLevel,

        unlockedLevels:
            [...LEVEL_MANAGER.unlockedLevels],

        score:
            GAME_STATE.score,

        rewards:
            {
                ...REWARD_STATE
            },

        achievements:
            Object.values(
                ACHIEVEMENTS
            ).map(item => ({
                id: item.id,
                unlocked:
                    item.unlocked
            }))
    };
}


function saveFullProfile() {

    const snapshot =
        createSaveSnapshot();

    localStorage.setItem(
        LOCAL_SAVE_KEY,
        JSON.stringify(snapshot)
    );
}


function loadFullProfile() {

    const saved =
        localStorage.getItem(
            LOCAL_SAVE_KEY
        );

    if (!saved) {
        return null;
    }

    try {

        return JSON.parse(saved);

    } catch {

        return null;
    }
}
