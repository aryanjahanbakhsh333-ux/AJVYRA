function handlePlayerDamage(
    scene,
    player,
    source
) {

    if (
        !player ||
        player.hitCooldown ||
        GAME_STATE.gameOver
    ) {
        return;
    }

    player.hitCooldown = true;

    GAME_STATE.lives--;

    updateHUD();

    playerHitEffect(
        scene,
        player
    );

    player.setVelocity(
        0,
        -300
    );

    if (GAME_STATE.lives <= 0) {

        showGameOver(
            scene,
            "GAME OVER",
            "The shadows consumed you."
        );

        return;
    }

    scene.time.delayedCall(
        1000,
        () => {

            player.hitCooldown = false;

            if (player.active) {
                player.setAlpha(1);
            }
        }
    );

    respawnPlayer(player);
}
