let attackCooldown = false;

function attackPlayer(scene) {

    if (
        !player ||
        GAME_STATE.gameOver ||
        attackCooldown
    ) {
        return;
    }

    attackCooldown = true;

    const attackRange = 70;

    enemies.children.iterate(
        enemy => {

            if (!enemy || !enemy.active) {
                return;
            }

            const distance =
                Phaser.Math.Distance.Between(
                    player.x,
                    player.y,
                    enemy.x,
                    enemy.y
                );

            if (distance <= attackRange) {

                damageEnemy(
                    enemy,
                    PLAYER_STATS.damage
                );
            }
        }
    );

    scene.time.delayedCall(
        350,
        () => {
            attackCooldown = false;
        }
    );
}
