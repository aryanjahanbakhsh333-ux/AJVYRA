function finishLevel(scene) {

    if (GAME_STATE.gameOver) {
        return;
    }

    GAME_STATE.completed = true;
    GAME_STATE.gameOver = true;

    saveGame();

    scene.physics.pause();

    const highScore = getHighScore();

    const finalScore =
        GAME_STATE.score;

    let message =
        "SCORE: " + finalScore;

    if (finalScore >= highScore) {
        message += "\nNEW HIGH SCORE";
    }

    scene.add.rectangle(
        450,
        300,
        900,
        600,
        0x000000,
        0.85
    );

    scene.add.text(
        450,
        220,
        "MISSION COMPLETE",
        {
            fontSize: "40px",
            color: "#ffffff",
            fontStyle: "bold"
        }
    ).setOrigin(0.5);

    scene.add.text(
        450,
        300,
        message,
        {
            fontSize: "22px",
            color: "#aaaaaa",
            align: "center"
        }
    ).setOrigin(0.5);

    const restart =
        scene.add.text(
            450,
            390,
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

    restart.setInteractive();

    restart.on(
        "pointerdown",
        () => {
            scene.scene.restart();
        }
    );
}
