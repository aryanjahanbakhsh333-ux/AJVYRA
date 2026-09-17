function completeLevel(scene) {

    if (
        GAME_STATE.completed ||
        GAME_STATE.gameOver
    ) {
        return;
    }

    GAME_STATE.completed = true;

    GAME_STATE.gameOver = true;

    const finalScore =
        GAME_STATE.score;

    const oldHighScore =
        getHighScore();

    const newHighScore =
        saveGame(finalScore);

    scene.physics.pause();

    const overlay =
        scene.add.rectangle(
            450,
            300,
            900,
            600,
            0x000000,
            0.88
        );

    scene.add.text(
        450,
        210,
        "LEVEL COMPLETE",
        {
            fontSize: "42px",
            color: "#ffffff",
            fontStyle: "bold"
        }
    ).setOrigin(0.5);

    scene.add.text(
        450,
        280,
        "SCORE: " + finalScore,
        {
            fontSize: "22px",
            color: "#aaaaaa"
        }
    ).setOrigin(0.5);

    if (newHighScore > oldHighScore) {

        scene.add.text(
            450,
            325,
            "NEW HIGH SCORE",
            {
                fontSize: "18px",
                color: "#ffffff"
            }
        ).setOrigin(0.5);
    }

    const next =
        scene.add.text(
            450,
            400,
            "PLAY AGAIN",
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

    return overlay;
}
