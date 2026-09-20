const INTERACT_INPUT = {
    pressed: false
};


function setupInteractInput(scene) {

    const interactKey =
        scene.input.keyboard.addKey(
            Phaser.Input.Keyboard.KeyCodes.E
        );

    interactKey.on(
        "down",
        () => {

            INTERACT_INPUT.pressed =
                true;

            performInteraction(
                scene
            );
        }
    );

    interactKey.on(
        "up",
        () => {

            INTERACT_INPUT.pressed =
                false;
        }
    );
}


function performInteraction(scene) {

    if (
        !player ||
        !player.active
    ) {
        return;
    }

    const range = 85;

    let closest = null;

    let closestDistance =
        Infinity;

    scene.children.list.forEach(
        object => {

            if (
                !object.interactionAction ||
                !object.active
            ) {
                return;
            }

            const distance =
                Phaser.Math.Distance.Between(
                    player.x,
                    player.y,
                    object.x,
                    object.y
                );

            if (
                distance <= range &&
                distance < closestDistance
            ) {

                closest = object;

                closestDistance =
                    distance;
            }
        }
    );

    if (closest) {

        closest.interactionAction();
    }
}
