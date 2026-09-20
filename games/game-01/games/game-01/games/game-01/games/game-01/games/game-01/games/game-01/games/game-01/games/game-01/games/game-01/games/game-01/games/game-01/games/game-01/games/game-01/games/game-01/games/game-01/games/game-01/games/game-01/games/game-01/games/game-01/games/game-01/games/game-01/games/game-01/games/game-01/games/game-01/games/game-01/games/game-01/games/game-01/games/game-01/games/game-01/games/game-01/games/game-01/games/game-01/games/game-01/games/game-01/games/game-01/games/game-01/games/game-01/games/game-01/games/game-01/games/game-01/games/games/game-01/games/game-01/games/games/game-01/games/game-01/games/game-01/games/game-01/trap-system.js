function createTrap(
    scene,
    x,
    y,
    width = 60,
    height = 20,
    damage = 35
) {

    const trap =
        scene.add.rectangle(
            x,
            y,
            width,
            height,
            0x444444
        );

    scene.physics.add.existing(
        trap,
        true
    );

    trap.damage =
        damage;

    return trap;
}


function activateTrap(
    scene,
    playerObject,
    trap
) {

    if (
        !playerObject ||
        !trap ||
        playerObject.hitCooldown
    ) {
        return;
    }

    handlePlayerDamage(
        scene,
        playerObject,
        trap
    );
}
