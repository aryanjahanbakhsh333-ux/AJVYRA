function createPlayer(scene, x, y) {

    const player = scene.add.rectangle(
        x,
        y,
        35,
        50,
        0xffffff
    );

    scene.physics.add.existing(player);

    player.body.setCollideWorldBounds(true);

    player.speed = 280;
    player.jumpPower = 500;

    player.hitCooldown = false;

    return player;
}

function damagePlayer(scene, player) {

    if (
        GAME_STATE.gameOver ||
        player.hitCooldown
    ) {
        return;
    }

    GAME_STATE.lives--;

    updateHUD();

    player.hitCooldown = true;

    player.setAlpha(0.35);

    scene.time.delayedCall(
        1000,
        () => {

            player.hitCooldown = false;

            if (player.active) {
                player.setAlpha(1);
            }
        }
    );

    if (GAME_STATE.lives <= 0) {

        showGameOver(
            scene,
            "GAME OVER",
            "Black Run has ended."
        );
    }
}
