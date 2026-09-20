let MAIN_MENU_UI = null;


function createMainMenuUI(scene) {

    MAIN_MENU_UI =
        scene.add.container(
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
            0.92
        );

    const title =
        createUIText(
            scene,
            0,
            -150,
            "BLACK RUN",
            52
        ).setOrigin(0.5);

    const subtitle =
        createUIText(
            scene,
            0,
            -90,
            "AN AJVYRA ORIGINAL",
            14
        ).setOrigin(0.5);

    const start =
        createMenuButton(
            scene,
            0,
            20,
            "START"
        );

    const settings =
        createMenuButton(
            scene,
            0,
            95,
            "SETTINGS"
        );

    start.on(
        "pointerdown",
        () => {

            MAIN_MENU_UI.setVisible(false);

            GAME_STATE.started = true;

            startRuntime();
        }
    );

    settings.on(
        "pointerdown",
        () => {

            showWorldMessage(
                scene,
                "SETTINGS AVAILABLE IN OPTIONS"
            );
        }
    );

    MAIN_MENU_UI.add([
        background,
        title,
        subtitle,
        start,
        settings
    ]);

    return MAIN_MENU_UI;
}


function createMenuButton(
    scene,
    x,
    y,
    label
) {

    const button =
        createUIText(
            scene,
            x,
            y,
            label,
            20
        ).setOrigin(0.5);

    button.setPadding(
        28,
        12,
        28,
        12
    );

    button.setBackgroundColor(
        "#171717"
    );

    button.setInteractive({
        useHandCursor: true
    });

    button.on(
        "pointerover",
        () => {
            button.setColor("#cccccc");
        }
    );

    button.on(
        "pointerout",
        () => {
            button.setColor("#ffffff");
        }
    );

    return button;
}
