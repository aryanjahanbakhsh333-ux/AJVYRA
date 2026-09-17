const MOBILE_INPUT = {

    left: false,

    right: false,

    jump: false
};


function setupMobileInput() {

    const left =
        document.getElementById("leftBtn");

    const right =
        document.getElementById("rightBtn");

    const jump =
        document.getElementById("jumpBtn");


    if (
        !left ||
        !right ||
        !jump
    ) {
        return;
    }


    function bindButton(
        button,
        key
    ) {

        const start = (event) => {

            event.preventDefault();

            MOBILE_INPUT[key] = true;
        };


        const end = (event) => {

            event.preventDefault();

            MOBILE_INPUT[key] = false;
        };


        button.addEventListener(
            "pointerdown",
            start
        );

        button.addEventListener(
            "pointerup",
            end
        );

        button.addEventListener(
            "pointercancel",
            end
        );

        button.addEventListener(
            "pointerleave",
            end
        );
    }


    bindButton(
        left,
        "left"
    );

    bindButton(
        right,
        "right"
    );

    bindButton(
        jump,
        "jump"
    );
}
