function showGameOver(scene, title, message) {

    GAME_STATE.gameOver = true;

    scene.physics.pause();

    scene.add.rectangle(
        450,
        300,
        900,
        600,
        0x000000,
        0.82
    );

    scene.add.text(
        450,
        245,
        title,
        {
            fontSize: "44px",
            color: "#ffffff",
            fontStyle: "bold"
        }
    ).setOrigin(0.5);

    scene.add.text(
        450,
        310,
        message,
        {
            fontSize: "20px",
            color: "#aaaaaa"
        }
    ).setOrigin(0.5);

    const restart = scene.add.text(
        450,
        370,
        "TAP TO RESTART",
        {
            fontSize: "20px",
            color: "#ffffff",
            backgroundColor: "#222222",
            padding: {
                left: 20,
                right: 20,
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
