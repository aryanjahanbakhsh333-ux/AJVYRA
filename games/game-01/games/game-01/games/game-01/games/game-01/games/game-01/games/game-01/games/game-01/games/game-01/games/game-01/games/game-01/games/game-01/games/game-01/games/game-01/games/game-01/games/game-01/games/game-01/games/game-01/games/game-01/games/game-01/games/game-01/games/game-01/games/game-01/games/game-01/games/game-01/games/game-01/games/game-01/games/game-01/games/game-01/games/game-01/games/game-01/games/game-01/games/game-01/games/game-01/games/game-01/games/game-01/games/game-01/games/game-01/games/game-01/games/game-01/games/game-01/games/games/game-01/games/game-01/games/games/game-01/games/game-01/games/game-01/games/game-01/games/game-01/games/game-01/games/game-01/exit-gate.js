function createExitGate(
    scene,
    x,
    y
) {

    const gate =
        scene.add.rectangle(
            x,
            y,
            80,
            120,
            0x202020
        );

    scene.physics.add.existing(
        gate,
        true
    );

    gate.open = false;

    gate.setStrokeStyle(
        3,
        0x555555
    );

    return gate;
}


function unlockExitGate(
    scene,
    gate
) {

    if (!gate) {
        return;
    }

    if (
        !LEVEL_PROGRESS.objectivesComplete
    ) {

        notifyPlayer(
            scene,
            "COMPLETE THE OBJECTIVES"
        );

        return;
    }

    gate.open = true;

    gate.setFillStyle(
        0xffffff
    );

    notifyPlayer(
        scene,
        "EXIT UNLOCKED"
    );
}
