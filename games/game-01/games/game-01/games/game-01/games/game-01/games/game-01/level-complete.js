function completeLevel(scene) {

    if (
        GAME_STATE.completed ||
        GAME_STATE.gameOver
    ) {
        return;
    }

    GAME_STATE.completed = true;
    GAME_STATE.gameOver = true;

    saveGame();

    scene.physics.pause();

    const overlay =
        scene.add.rectangle(
            450,
            300,
            900,
            600,
            0x000000,
            0.86
        );

    const title =
        scene.add.text(
            450,
            210,
            "LEVEL COMPLETE",
            {
                fontSize: "42px",
                fontStyle: "bold",
                color: "#ffffff"
            }
        ).setOrigin(0.5);

    const score =
        scene.add.text(
            450,
            285,
            "SCORE: " +
            GAME_STATE.score,
            {
                fontSize: "22px",
                color: "#aaaaaa"
            }
        ).setOrigin(0.5);

    const next =
        scene.add.text(
            450,
            370,
            "NEXT LEVEL",
            {
                fontSize: "20px",
                color: "#ffffff",
                backgroundColor: "#222222",
                padding: {
                    left: 25,
                    right: 25,
                    top: 12,
                    bottom: 12
                }
            }
        ).setOrigin(0.5);

    next.setInteractive();

    next.on(
        "pointerdown",
        () => {

            scene.scene.restart();

        }
    );

    return {
        overlay,
        title,
        score,
        next
    };
}
