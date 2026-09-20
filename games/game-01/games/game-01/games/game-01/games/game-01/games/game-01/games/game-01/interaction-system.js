function createInteractionSystem(scene) {

    scene.input.on(
        "gameobjectdown",
        (pointer, object) => {

            if (
                object &&
                object.interactionAction
            ) {

                object.interactionAction();
            }
        }
    );
}

function makeInteractable(
    object,
    action
) {

    object.setInteractive();

    object.interactionAction =
        action;

    return object;
}
