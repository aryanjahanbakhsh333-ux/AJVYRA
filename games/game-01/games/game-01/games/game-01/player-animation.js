function updatePlayerAnimation(
    player,
    movingLeft,
    movingRight
) {

    if (!player) {
        return;
    }

    const moving =
        movingLeft ||
        movingRight;

    if (
        player.anims &&
        player.anims.exists("run")
    ) {

        if (moving) {

            player.anims.play(
                "run",
                true
            );

        } else {

            player.anims.stop();
        }
    }

    if (movingLeft) {
        player.setFlipX(true);
    }

    if (movingRight) {
        player.setFlipX(false);
    }
}
