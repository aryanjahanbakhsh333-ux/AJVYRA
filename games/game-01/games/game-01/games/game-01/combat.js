function damageEnemy(
    enemy,
    amount
) {

    if (!enemy || !enemy.active) {
        return;
    }

    enemy.health =
        (enemy.health ?? 50) - amount;

    enemy.setAlpha(0.5);

    if (enemy.scene) {

        enemy.scene.time.delayedCall(
            120,
            () => {

                if (enemy.active) {
                    enemy.setAlpha(1);
                }
            }
        );
    }

    if (enemy.health <= 0) {

        destroyEnemy(enemy);
    }
}

function destroyEnemy(enemy) {

    if (!enemy || !enemy.active) {
        return;
    }

    GAME_STATE.score += 50;

    if (window.updateHUD) {
        window.updateHUD();
    }

    enemy.destroy();
}
