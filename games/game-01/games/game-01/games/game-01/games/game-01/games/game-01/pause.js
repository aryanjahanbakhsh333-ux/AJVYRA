let pauseOverlay = null;
let paused = false;

function createPauseSystem(scene) {

    const pauseKey =
        scene.input.keyboard.addKey(
            Phaser.Input.Keyboard.KeyCodes.ESC
        );

    pauseKey.on(
        "down",
        () => {
            togglePause(scene);
        }
    );
}

function togglePause(scene) {

    if (GAME_STATE.gameOver) {
        return;
    }

    paused = !paused;

    if (paused) {

        scene.physics.pause();

        createPauseOverlay(scene);

    } else {

        scene.physics.resume();

        if (pauseOverlay) {
            pauseOverlay.destroy();
            pauseOverlay = null;
        }
    }
}

function createPauseOverlay(scene) {

    pauseOverlay = scene.add.container(
        450,
        300
    );

    const background =
        scene.add.rectangle(
            0,
            0,
            900,
            600,
            0x000000,
            0.75
        );

    const title =
        scene.add.text(
            0,
            -30,
            "PAUSED",
            {
                fontSize: "46px",
                color: "#ffffff",
                fontStyle: "bold"
            }
        ).setOrigin(0.5);

    const hint =
        scene.add.text(
            0,
            40,
            "Press ESC to continue",
            {
                fontSize: "18px",
                color: "#999999"
            }
        ).setOrigin(0.5);

    pauseOverlay.add([
        background,
        title,
        hint
    ]);
}
