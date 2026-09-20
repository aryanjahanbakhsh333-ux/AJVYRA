const ACHIEVEMENTS = {

    FIRST_CORE: {
        id: "first-core",
        title: "First Signal",
        description: "Collect your first energy core.",
        unlocked: false
    },

    FIRST_KILL: {
        id: "first-kill",
        title: "First Shadow",
        description: "Defeat your first enemy.",
        unlocked: false
    },

    PERFECT_LEVEL: {
        id: "perfect-level",
        title: "Untouched",
        description: "Complete a level without losing a life.",
        unlocked: false
    },

    MASTER_RUN: {
        id: "master-run",
        title: "Black Runner",
        description: "Complete the first level.",
        unlocked: false
    }
};


function unlockAchievement(id) {

    const achievement =
        Object.values(ACHIEVEMENTS)
            .find(item => item.id === id);

    if (!achievement) {
        return false;
    }

    if (achievement.unlocked) {
        return false;
    }

    achievement.unlocked = true;

    saveAchievements();

    return true;
}


function saveAchievements() {

    const data = {};

    Object.values(ACHIEVEMENTS).forEach(
        achievement => {

            data[achievement.id] =
                achievement.unlocked;
        }
    );

    localStorage.setItem(
        "AJVYRA_BLACK_RUN_ACHIEVEMENTS",
        JSON.stringify(data)
    );
}


function loadAchievements() {

    const saved =
        localStorage.getItem(
            "AJVYRA_BLACK_RUN_ACHIEVEMENTS"
        );

    if (!saved) {
        return;
    }

    try {

        const data =
            JSON.parse(saved);

        Object.values(ACHIEVEMENTS)
            .forEach(achievement => {

                achievement.unlocked =
                    Boolean(
                        data[achievement.id]
                    );
            });

    } catch {

        return;
    }
}
