function createPickup(
    scene,
    x,
    y,
    type,
    value = 1
) {

    const pickup =
        scene.add.circle(
            x,
            y,
            12,
            0xffffff
        );

    scene.physics.add.existing(
        pickup
    );

    pickup.body.setAllowGravity(
        false
    );

    pickup.pickupType = type;

    pickup.value = value;

    return pickup;
}

function handlePickup(
    playerObject,
    pickupObject
) {

    if (
        !pickupObject ||
        !pickupObject.active
    ) {
        return;
    }

    switch (
        pickupObject.pickupType
    ) {

        case "health":

            healPlayer(
                pickupObject.value
            );

            updateHealthBar();

            break;


        case "score":

            GAME_STATE.score +=
                pickupObject.value;

            updateHUD();

            break;
    }

    pickupObject.destroy();
}
