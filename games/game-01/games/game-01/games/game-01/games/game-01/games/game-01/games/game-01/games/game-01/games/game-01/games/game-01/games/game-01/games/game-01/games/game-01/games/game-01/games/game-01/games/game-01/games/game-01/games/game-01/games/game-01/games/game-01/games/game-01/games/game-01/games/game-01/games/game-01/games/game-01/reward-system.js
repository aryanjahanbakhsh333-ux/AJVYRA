const REWARD_STATE = {

    xp: 0,

    level: 1,

    totalCoins: 0,

    totalKills: 0
};


function addXP(amount) {

    if (
        !Number.isFinite(amount) ||
        amount <= 0
    ) {
        return;
    }

    REWARD_STATE.xp += amount;

    checkPlayerLevel();
}


function checkPlayerLevel() {

    const requiredXP =
        REWARD_STATE.level * 100;

    if (
        REWARD_STATE.xp >=
        requiredXP
    ) {

        REWARD_STATE.xp -=
            requiredXP;

        REWARD_STATE.level++;

        showRewardNotification(
            "LEVEL UP!"
        );
    }
}


function registerReward(
    type,
    amount
) {

    if (type === "coin") {

        REWARD_STATE.totalCoins +=
            amount;

        addXP(10);
    }

    if (type === "kill") {

        REWARD_STATE.totalKills +=
            amount;

        addXP(25);
    }
}


function showRewardNotification(
    message
) {

    if (
        typeof showWorldMessage ===
        "function" &&
        window.AJVYRA_SCENE
    ) {

        showWorldMessage(
            window.AJVYRA_SCENE,
            message
        );
    }
}
