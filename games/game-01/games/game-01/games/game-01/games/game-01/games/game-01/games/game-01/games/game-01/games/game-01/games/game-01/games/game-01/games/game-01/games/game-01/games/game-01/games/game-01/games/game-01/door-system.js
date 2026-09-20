function createDoor(
    scene,
    x,
    y,
    keyId = "main-key"
) {

    const door =
        scene.add.rectangle(
            x,
            y,
            55,
            90,
            0x303030
        );

    door.keyId = keyId;

    door.isOpen = false;

    makeInteractable(
        door,
        () => {

            tryOpenDoor(
                scene,
                door
            );
        }
    );

    return door;
}

function tryOpenDoor(
    scene,
    door
) {

    if (door.isOpen) {
        return;
    }

    if (
        !hasKey(
            door.keyId
        )
    ) {

        showWorldMessage(
            scene,
            "THE DOOR IS LOCKED"
        );

        return;
    }

    door.isOpen = true;

    door.setFillStyle(
        0xffffff
    );

    showWorldMessage(
        scene,
        "DOOR UNLOCKED"
    );
}
