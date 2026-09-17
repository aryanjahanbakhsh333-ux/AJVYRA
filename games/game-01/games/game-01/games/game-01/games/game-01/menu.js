let startMenu;

function createStartMenu(scene) {

    startMenu = scene.add.container(450, 300);

    const background = scene.add.rectangle(
        0,
        0,
        900,
        600,
        0x000000,
        0.88
    );

    const title = scene.add.text(
        0,
        -100,
        "BLACK RUN",
        {
            fontSize: "52px",
            fontStyle: "bold",
            color: "#ffffff"
        }
    ).setOrigin(0.5);

    const subtitle = scene.add.text(
        0,
        -40,
        "AN AJVYRA ORIGINAL",
        {
            fontSize: "14px",
            letterSpacing: 4,
            color: "#888888"
        }
    ).setOrigin(0.5);

    const startButton = scene.add.text(
        0,
        70,
        "START GAME",
        {
            fontSize: "22px",
            color: "#ffffff",
            backgroundColor: "#222222",
            padding: {
                left: 30,
                right: 30,
                top: 15,
                bottom: 15
            }
        }
    ).setOrigin(0.5);

    startButton.setInteractive();

    startButton.on(
        "pointerdown",
        () => {
            startMenu.setVisible(false);
            scene.physics.resume();
        }
    );

    startButton.on(
        "pointerover",
        () => {
            startButton.setColor("#cccccc");
        }
    );

    startButton.on(
        "pointerout",
        () => {
            startButton.setColor("#ffffff");
        }
    );

    startMenu.add([
        background,
        title,
        subtitle,
        startButton
    ]);

    scene.physics.pause();
}
