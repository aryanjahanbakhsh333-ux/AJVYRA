const MOBILE_INPUT = {
    left: false,
    right: false,
    jump: false
};

function setupMobileInput() {

    const left = document.getElementById("leftBtn");
    const right = document.getElementById("rightBtn");
    const jump = document.getElementById("jumpBtn");

    if (!left || !right || !jump) {
        return;
    }

    function press(button, key) {

        button.addEventListener(
            "pointerdown",
            (event) => {

                event.preventDefault();

                MOBILE_INPUT[key] = true;
            }
        );

        button.addEventListener(
            "pointerup",
            (event) => {

                event.preventDefault();

                MOBILE_INPUT[key] = false;
            }
        );

        button.addEventListener(
            "pointerleave",
            () => {
                MOBILE_INPUT[key] = false;
            }
        );
    }

    press(left, "left");
    press(right, "right");
    press(jump, "jump");
}
