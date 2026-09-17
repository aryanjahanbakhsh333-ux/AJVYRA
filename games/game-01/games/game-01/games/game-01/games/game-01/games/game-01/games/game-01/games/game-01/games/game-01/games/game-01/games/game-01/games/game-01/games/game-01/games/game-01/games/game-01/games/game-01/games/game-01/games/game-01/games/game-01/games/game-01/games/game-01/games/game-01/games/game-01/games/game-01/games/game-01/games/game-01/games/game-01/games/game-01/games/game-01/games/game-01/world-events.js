function createWorldEvents(scene) {

    scene.events.on(
        "update",
        () => {

            if (
                !player ||
                !player.body ||
                GAME_STATE.gameOver
            ) {
                return;
            }


            if (
                player.x >= 850 &&
                player.x < 950
            ) {

                activateCheckpoint(
                    "checkpoint-01"
                );
            }


            if (
                player.x >= 1550 &&
                player.x < 1650
            ) {

                activateCheckpoint(
                    "checkpoint-02"
                );
            }
        }
    );
}
