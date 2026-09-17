function createEnemy(scene, x, y, minX, maxX) {

    const enemy = scene.add.rectangle(
        x,
        y,
        38,
        38,
        0x777777
    );

    scene.physics.add.existing(enemy);

    enemy.body.setAllowGravity(false);
    enemy.body.setVelocityX(90);

    enemy.minX = minX;
    enemy.maxX = maxX;

    return enemy;
}

function updateEnemy(enemy) {

    if (!enemy || !enemy.body) {
        return;
    }

    if (enemy.x <= enemy.minX) {
        enemy.body.setVelocityX(90);
    }

    if (enemy.x >= enemy.maxX) {
        enemy.body.setVelocityX(-90);
    }
}
