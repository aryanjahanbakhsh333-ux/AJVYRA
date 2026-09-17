let gameTimer = null;


function startGameTimer(scene) {

    if (gameTimer) {

        gameTimer.remove(false);

        gameTimer = null;
    }

    gameTimer =
        scene.time.addEvent({

            delay: 1000,

            loop: true,

            callback: () => {

                if (
                    GAME_STATE.gameOver ||
                    !GAME_STATE.started
                ) {
                    return;
                }

                GAME_STATE.time--;

                updateHUD();

                if (
                    GAME_STATE.time <= 0
                ) {

                    GAME_STATE.time = 0;

                    showGameOver(
                        scene,
                        "TIME OVER",
                        "The world went dark."
                    );
                }
            }
        });
}
