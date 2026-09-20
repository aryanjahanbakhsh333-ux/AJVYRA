let PAUSE_UI = null;


function createPauseUI(scene) {

    PAUSE_UI =
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
            0.82
        );

    const title =
        createUIText(
            scene,
            0,
            -60,
            "PAUSED",
            46
        ).setOrigin(0.5);

    const resume =
        createMenuButton(
            scene,
            0,
            30,
            "RESUME"
        );

    resume.on(
        "pointerdown",
        () => {

            togglePause(
                scene
            );
        }
    );

    PAUSE_UI.add([
        background,
        title,
        resume
    ]);

    PAUSE_UI.setVisible(false);

    return PAUSE_UI;
}


function updatePauseUI() {

    if (!PAUSE_UI) {
        return;
    }

    PAUSE_UI.setVisible(
        paused
    );
}
