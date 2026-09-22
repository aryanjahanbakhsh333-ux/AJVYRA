class AJVYRAWebGameRuntime {
    constructor(options = {}) {
        this.canvas = options.canvas || null;

        this.keys = new Set();
        this.previousKeys = new Set();

        this.gamepads = new Map();

        this.actions = options.actions || {};

        this.started = false;

        this._onKeyDown = this._onKeyDown.bind(this);
        this._onKeyUp = this._onKeyUp.bind(this);
        this._onGamepadConnected =
            this._onGamepadConnected.bind(this);
        this._onGamepadDisconnected =
            this._onGamepadDisconnected.bind(this);
    }

    start() {
        if (this.started) {
            return;
        }

        this.started = true;

        window.addEventListener(
            "keydown",
            this._onKeyDown,
            { passive: false }
        );

        window.addEventListener(
            "keyup",
            this._onKeyUp,
            { passive: false }
        );

        window.addEventListener(
            "gamepadconnected",
            this._onGamepadConnected
        );

        window.addEventListener(
            "gamepaddisconnected",
            this._onGamepadDisconnected
        );
    }

    stop() {
        if (!this.started) {
            return;
        }

        this.started = false;

        window.removeEventListener(
            "keydown",
            this._onKeyDown
        );

        window.removeEventListener(
            "keyup",
            this._onKeyUp
        );

        window.removeEventListener(
            "gamepadconnected",
            this._onGamepadConnected
        );

        window.removeEventListener(
            "gamepaddisconnected",
            this._onGamepadDisconnected
        );

        this.keys.clear();
        this.previousKeys.clear();
        this.gamepads.clear();
    }

    beginFrame() {
        this.previousKeys = new Set(this.keys);
        this._pollGamepads();
    }

    isKeyDown(key) {
        return this.keys.has(key);
    }

    wasKeyPressed(key) {
        return (
            this.keys.has(key) &&
            !this.previousKeys.has(key)
        );
    }

    isActionDown(actionId) {
        const action = this.actions[actionId];

        if (!action) {
            return false;
        }

        for (const key of action.keys || []) {
            if (this.isKeyDown(key)) {
                return true;
            }
        }

        for (const gamepad of this.gamepads.values()) {
            for (const index of action.gamepad_buttons || []) {
                const button = gamepad.buttons[index];

                if (
                    button &&
                    (button.pressed || button.value > 0.25)
                ) {
                    return true;
                }
            }
        }

        return false;
    }

    getAxis(index = 0) {
        for (const gamepad of this.gamepads.values()) {
            if (
                gamepad.axes &&
                Number.isFinite(gamepad.axes[index])
            ) {
                return gamepad.axes[index];
            }
        }

        return 0;
    }

    getGamepadState() {
        const result = [];

        for (const gamepad of this.gamepads.values()) {
            result.push({
                index: gamepad.index,
                id: gamepad.id,
                connected: gamepad.connected,
                mapping: gamepad.mapping,
                axes: Array.from(gamepad.axes || []),
                buttons: Array.from(gamepad.buttons || []).map(
                    (button) => ({
                        pressed: Boolean(button.pressed),
                        value: Number(button.value || 0),
                    })
                ),
            });
        }

        return result;
    }

    _pollGamepads() {
        if (
            !navigator.getGamepads ||
            typeof navigator.getGamepads !== "function"
        ) {
            return;
        }

        const pads = navigator.getGamepads();

        for (const pad of pads) {
            if (pad && pad.connected) {
                this.gamepads.set(pad.index, pad);
            }
        }
    }

    _onKeyDown(event) {
        this.keys.add(event.key);

        if (
            [
                "ArrowUp",
                "ArrowDown",
                "ArrowLeft",
                "ArrowRight",
                " ",
            ].includes(event.key)
        ) {
            event.preventDefault();
        }
    }

    _onKeyUp(event) {
        this.keys.delete(event.key);
    }

    _onGamepadConnected(event) {
        if (event.gamepad) {
            this.gamepads.set(
                event.gamepad.index,
                event.gamepad
            );
        }
    }

    _onGamepadDisconnected(event) {
        if (event.gamepad) {
            this.gamepads.delete(
                event.gamepad.index
            );
        }
    }
}

window.AJVYRAWebGameRuntime = AJVYRAWebGameRuntime;
