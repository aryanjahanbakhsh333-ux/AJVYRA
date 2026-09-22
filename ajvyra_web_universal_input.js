class AJVYRAWebUniversalInput {
    constructor(options = {}) {
        this.deadzone = Math.max(
            0,
            Math.min(0.5, Number(options.deadzone) || 0.15)
        );

        this.keys = new Set();
        this.previousKeys = new Set();

        this.buttons = new Set();
        this.previousButtons = new Set();

        this.axes = {
            x: 0,
            y: 0
        };

        this.previousAxes = {
            x: 0,
            y: 0
        };

        this.pointer = {
            x: 0,
            y: 0,
            active: false
        };

        this.actionMap = {
            left: ["ArrowLeft", "KeyA"],
            right: ["ArrowRight", "KeyD"],
            up: ["ArrowUp", "KeyW"],
            down: ["ArrowDown", "KeyS"],
            jump: ["Space"],
            attack: ["KeyJ", "KeyZ"],
            special: ["KeyK", "KeyX"],
            interact: ["KeyE"],
            pause: ["Escape"],
            confirm: ["Enter"]
        };

        this.touchActions = new Map();

        this.gamepad = null;

        this.enabled = true;

        this.boundKeyDown =
            event => this.handleKeyDown(event);

        this.boundKeyUp =
            event => this.handleKeyUp(event);

        this.boundPointerDown =
            event => this.handlePointerDown(event);

        this.boundPointerUp =
            event => this.handlePointerUp(event);

        this.boundPointerMove =
            event => this.handlePointerMove(event);

        this.boundGamepadConnected =
            event => this.handleGamepadConnected(event);

        this.boundGamepadDisconnected =
            event => this.handleGamepadDisconnected(event);

        this.attach();
    }

    attach() {
        window.addEventListener(
            "keydown",
            this.boundKeyDown
        );

        window.addEventListener(
            "keyup",
            this.boundKeyUp
        );

        window.addEventListener(
            "pointerdown",
            this.boundPointerDown
        );

        window.addEventListener(
            "pointerup",
            this.boundPointerUp
        );

        window.addEventListener(
            "pointermove",
            this.boundPointerMove
        );

        window.addEventListener(
            "gamepadconnected",
            this.boundGamepadConnected
        );

        window.addEventListener(
            "gamepaddisconnected",
            this.boundGamepadDisconnected
        );
    }

    handleKeyDown(event) {
        if (!this.enabled) {
            return;
        }

        this.keys.add(event.code);

        if (
            [
                "ArrowUp",
                "ArrowDown",
                "ArrowLeft",
                "ArrowRight",
                "Space"
            ].includes(event.code)
        ) {
            event.preventDefault();
        }
    }

    handleKeyUp(event) {
        this.keys.delete(event.code);
    }

    handlePointerDown(event) {
        if (!this.enabled) {
            return;
        }

        this.pointer.active = true;
        this.pointer.x = event.clientX;
        this.pointer.y = event.clientY;
    }

    handlePointerUp(event) {
        this.pointer.active = false;

        this.pointer.x = event.clientX;
        this.pointer.y = event.clientY;
    }

    handlePointerMove(event) {
        this.pointer.x = event.clientX;
        this.pointer.y = event.clientY;
    }

    handleGamepadConnected(event) {
        this.gamepad = event.gamepad;
    }

    handleGamepadDisconnected(event) {
        if (
            this.gamepad &&
            this.gamepad.index === event.gamepad.index
        ) {
            this.gamepad = null;
        }
    }

    update() {
        this.previousKeys = new Set(this.keys);
        this.previousButtons = new Set(this.buttons);

        this.previousAxes = {
            ...this.axes
        };

        this.buttons.clear();

        if (
            typeof navigator !== "undefined" &&
            navigator.getGamepads
        ) {
            const pads = navigator.getGamepads();

            if (this.gamepad) {
                const latest =
                    pads[this.gamepad.index];

                if (latest) {
                    this.gamepad = latest;
                }
            }

            if (!this.gamepad) {
                this.gamepad =
                    [...pads].find(Boolean) || null;
            }
        }

        if (this.gamepad) {
            this.readGamepad();
        }
    }

    readGamepad() {
        const gp = this.gamepad;

        const x =
            Number(gp.axes?.[0]) || 0;

        const y =
            Number(gp.axes?.[1]) || 0;

        this.axes.x =
            Math.abs(x) >= this.deadzone
                ? x
                : 0;

        this.axes.y =
            Math.abs(y) >= this.deadzone
                ? y
                : 0;

        const buttonMap = {
            0: "jump",
            1: "attack",
            2: "special",
            3: "interact",
            9: "pause"
        };

        for (
            const [index, action]
            of Object.entries(buttonMap)
        ) {
            const button =
                gp.buttons?.[Number(index)];

            if (
                button &&
                (button.pressed ||
                    button.value > 0.5)
            ) {
                this.buttons.add(action);
            }
        }

        if (this.axes.x < -this.deadzone) {
            this.buttons.add("left");
        }

        if (this.axes.x > this.deadzone) {
            this.buttons.add("right");
        }

        if (this.axes.y < -this.deadzone) {
            this.buttons.add("up");
        }

        if (this.axes.y > this.deadzone) {
            this.buttons.add("down");
        }
    }

    isKeyDown(code) {
        return this.keys.has(code);
    }

    wasKeyPressed(code) {
        return (
            this.keys.has(code) &&
            !this.previousKeys.has(code)
        );
    }

    isActionDown(action) {
        if (this.touchActions.get(action)) {
            return true;
        }

        if (this.buttons.has(action)) {
            return true;
        }

        const keys =
            this.actionMap[action] || [];

        return keys.some(
            code => this.keys.has(code)
        );
    }

    wasActionPressed(action) {
        if (
            this.buttons.has(action) &&
            !this.previousButtons.has(action)
        ) {
            return true;
        }

        const keys =
            this.actionMap[action] || [];

        return keys.some(
            code =>
                this.keys.has(code) &&
                !this.previousKeys.has(code)
        );
    }

    setTouchAction(action, active) {
        if (active) {
            this.touchActions.set(
                action,
                true
            );
        } else {
            this.touchActions.delete(action);
        }
    }

    getAxis() {
        let x = this.axes.x;
        let y = this.axes.y;

        if (this.isActionDown("left")) {
            x = -1;
        }

        if (this.isActionDown("right")) {
            x = 1;
        }

        if (this.isActionDown("up")) {
            y = -1;
        }

        if (this.isActionDown("down")) {
            y = 1;
        }

        return {
            x,
            y
        };
    }

    enable() {
        this.enabled = true;
    }

    disable() {
        this.enabled = false;
        this.keys.clear();
        this.buttons.clear();
        this.touchActions.clear();
    }

    destroy() {
        window.removeEventListener(
            "keydown",
            this.boundKeyDown
        );

        window.removeEventListener(
            "keyup",
            this.boundKeyUp
        );

        window.removeEventListener(
            "pointerdown",
            this.boundPointerDown
        );

        window.removeEventListener(
            "pointerup",
            this.boundPointerUp
        );

        window.removeEventListener(
            "pointermove",
            this.boundPointerMove
        );

        window.removeEventListener(
            "gamepadconnected",
            this.boundGamepadConnected
        );

        window.removeEventListener(
            "gamepaddisconnected",
            this.boundGamepadDisconnected
        );
    }
}

if (typeof window !== "undefined") {
    window.AJVYRAWebUniversalInput =
        AJVYRAWebUniversalInput;
}
