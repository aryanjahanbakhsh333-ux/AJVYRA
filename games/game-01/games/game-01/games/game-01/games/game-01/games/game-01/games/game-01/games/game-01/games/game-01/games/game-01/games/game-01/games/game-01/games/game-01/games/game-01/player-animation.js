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
        player.anims.exists("player-run")
    ) {

        if (moving) {

            player.anims.play(
                "player-run",
                true
            );

        } else {

            player.anims.stop();
        }
    }

    if (movingLeft) {

        player.setFlipX(true);

    } else if (movingRight) {

        player.setFlipX(false);
    }
}
