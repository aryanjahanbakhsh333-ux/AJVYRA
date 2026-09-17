const CONTROL_STATE = {

    left: false,

    right: false,

    jump: false,

    pause: false
};

function setupControls(scene) {

    const keyboard =
        scene.input.keyboard;

    keyboard.on(
        "keydown-LEFT",
        () => {
            CONTROL_STATE.left = true;
        }
    );

    keyboard.on(
        "keyup-LEFT",
        () => {
            CONTROL_STATE.left = false;
        }
    );

    keyboard.on(
        "keydown-RIGHT",
        () => {
            CONTROL_STATE.right = true;
        }
    );

    keyboard.on(
        "keyup-RIGHT",
        () => {
            CONTROL_STATE.right = false;
        }
    );

    keyboard.on(
        "keydown-UP",
        () => {
            CONTROL_STATE.jump = true;
        }
    );

    keyboard.on(
        "keyup-UP",
        () => {
            CONTROL_STATE.jump = false;
        }
    );
}
