const BOSS_STATE = {
    active: false,
    defeated: false,
    health: 500,
    maxHealth: 500
};


function createBoss(
    scene,
    x,
    y
) {

    const boss =
        scene.add.rectangle(
            x,
            y,
            90,
            110,
            0x555555
        );

    scene.physics.add.existing(
        boss
    );

    boss.body.setCollideWorldBounds(
        true
    );

    boss.body.setGravityY(900);

    boss.health =
        BOSS_STATE.maxHealth;

    boss.attackCooldown = false;

    BOSS_STATE.active = true;

    return boss;
}


function damageBoss(
    scene,
    boss,
    amount
) {

    if (
        !boss ||
        !boss.active
    ) {
        return;
    }

    boss.health -= amount;

    if (boss.health <= 0) {

        boss.health = 0;

        defeatBoss(
            scene,
            boss
        );
    }
}


function defeatBoss(
    scene,
    boss
) {

    BOSS_STATE.active = false;

    BOSS_STATE.defeated = true;

    GAME_STATE.score += 500;

    registerReward(
        "kill",
        10
    );

    emitGameEvent(
        scene,
        GAME_EVENTS.ENEMY_DEFEATED,
        {
            boss: true
        }
    );

    boss.destroy();

    notifyPlayer(
        scene,
        "BOSS DEFEATED"
    );
}
