function createExit(
    scene,
    x,
    y
) {

    const exit =
        scene.add.rectangle(
            x,
            y,
            70,
            110,
            0x111111
        );

    scene.physics.add.existing(
        exit,
        true
    );

    exit.setStrokeStyle(
        2,
        0xffffff
    );

    return exit;
}

function checkExit(
    scene,
    playerObject,
    exitObject
) {

    if (
        !playerObject ||
        !exitObject ||
        GAME_STATE.gameOver
    ) {
        return;
    }

    if (
        checkLevelObjectives()
    ) {

        completeLevel(scene);

    } else {

        showWorldMessage(
            scene,
            "OBJECTIVES INCOMPLETE"
        );
    }
}
