class AJVYRAWebGameInputBridge {
    constructor(options = {}) {
        this.input =
            options.input ||
            new AJVYRAWebUniversalInput();

        this.touchControls = null;

        this.enabled = true;
    }

    attachTouchControls(container) {
        this.touchControls =
            new AJVYRAWebTouchControls({
                input: this.input
            });

        this.touchControls.mount(container);

        return this.touchControls;
    }

    update() {
        if (!this.enabled) {
            return;
        }

        this.input.update();
    }

    isDown(action) {
        if (!this.enabled) {
            return false;
        }

        return this.input.isActionDown(
            action
        );
    }

    wasPressed(action) {
        if (!this.enabled) {
            return false;
        }

        return this.input.wasActionPressed(
            action
        );
    }

    getMovement() {
        if (!this.enabled) {
            return {
                x: 0,
                y: 0
            };
        }

        return this.input.getAxis();
    }

    enable() {
        this.enabled = true;
        this.input.enable();

        if (this.touchControls) {
            this.touchControls.show();
        }
    }

    disable() {
        this.enabled = false;
        this.input.disable();

        if (this.touchControls) {
            this.touchControls.hide();
        }
    }

    destroy() {
        this.input.destroy();

        this.touchControls = null;
    }
}

if (typeof window !== "undefined") {
    window.AJVYRAWebGameInputBridge =
        AJVYRAWebGameInputBridge;
}
