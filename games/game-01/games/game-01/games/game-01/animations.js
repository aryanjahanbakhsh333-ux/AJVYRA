function createPlayerAnimations(scene) {

    /*
     * این بخش وقتی Sprite Sheet واقعی
     * شخصیت AJVYRA اضافه شود فعال می‌شود.
     */

    if (
        !scene.textures.exists("player-run")
    ) {
        return;
    }

    scene.anims.create({

        key: "player-run",

        frames:
            scene.anims.generateFrameNumbers(
                "player-run",
                {
                    start: 0,
                    end: 5
                }
            ),

        frameRate: 10,

        repeat: -1
    });
}

function playPlayerAnimation(
    player,
    moving
) {

    if (
        !player ||
        !player.anims
    ) {
        return;
    }

    if (moving) {

        player.anims.play(
            "player-run",
            true
        );

    } else {

        player.anims.stop();
    }
}
