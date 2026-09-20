let healthBarBackground;
let healthBarFill;

function createHealthBar(scene) {

    healthBarBackground = scene.add.rectangle(
        25,
        120,
        180,
        16,
        0x222222
    ).setOrigin(0, 0);

    healthBarFill = scene.add.rectangle(
        25,
        120,
        180,
        16,
        0xffffff
    ).setOrigin(0, 0);

    updateHealthBar();
}

function updateHealthBar() {

    if (!healthBarFill) {
        return;
    }

    const percent =
        PLAYER_STATS.health /
        PLAYER_STATS.maxHealth;

    healthBarFill.width =
        180 * percent;
}
