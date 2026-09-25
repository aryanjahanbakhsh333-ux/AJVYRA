(() => {
    "use strict";

    class AJVYRA_BrowserInput {
        constructor() {
            this.keys = new Set();
            this.previousKeys = new Set();

            this.pointer = {
                x: 0,
                y: 0,
                down: false
            };

            this.touch = {
                left: false,
                right: false,
                up: false,
                down: false,
                jump: false,
                attack: false,
                dash: false,
                action: false
            };

            this._keydown = e => {
                this.keys.add(e.code);
            };

            this._keyup = e => {
                this.keys.delete(e.code);
            };

            this._pointerdown = e => {
                this.pointer.down = true;
                this.updatePointer(e);
            };

            this._pointerup = () => {
                this.pointer.down = false;
            };

            this._pointermove = e => {
                this.updatePointer(e);
            };

            window.addEventListener("keydown", this._keydown);
            window.addEventListener("keyup", this._keyup);

            window.addEventListener(
                "pointerdown",
                this._pointerdown,
                { passive: true }
            );

            window.addEventListener(
                "pointerup",
                this._pointerup,
                { passive: true }
            );

            window.addEventListener(
                "pointermove",
                this._pointermove,
                { passive: true }
            );

            this.bindTouchControls();
        }

        updatePointer(event) {
            this.pointer.x = event.clientX;
            this.pointer.y = event.clientY;
        }

        bindTouchControls() {
            const mapping = {
                left: "left",
                right: "right",
                up: "up",
                down: "down",
                jump: "jump",
                attack: "attack",
                dash: "dash",
                action: "action"
            };

            for (const [name, action] of Object.entries(mapping)) {
                const buttons = document.querySelectorAll(
                    `[data-aj-${name}]`
                );

                buttons.forEach(button => {
                    const press = e => {
                        e.preventDefault();
                        this.touch[action] = true;
                    };

                    const release = e => {
                        e.preventDefault();
                        this.touch[action] = false;
                    };

                    button.addEventListener(
                        "pointerdown",
                        press,
                        { passive: false }
                    );

                    button.addEventListener(
                        "pointerup",
                        release,
                        { passive: false }
                    );

                    button.addEventListener(
                        "pointercancel",
                        release,
                        { passive: false }
                    );

                    button.addEventListener(
                        "pointerleave",
                        release,
                        { passive: false }
                    );
                });
            }
        }

        update() {
            this.previousKeys = new Set(this.keys);
        }

        down(code) {
            return this.keys.has(code);
        }

        pressed(code) {
            return (
                this.keys.has(code) &&
                !this.previousKeys.has(code)
            );
        }

        left() {
            return (
                this.down("ArrowLeft") ||
                this.down("KeyA") ||
                this.touch.left
            );
        }

        right() {
            return (
                this.down("ArrowRight") ||
                this.down("KeyD") ||
                this.touch.right
            );
        }

        up() {
            return (
                this.down("ArrowUp") ||
                this.down("KeyW") ||
                this.touch.up
            );
        }

        downMove() {
            return (
                this.down("ArrowDown") ||
                this.down("KeyS") ||
                this.touch.down
            );
        }

        jump() {
            return (
                this.down("Space") ||
                this.down("KeyW") ||
                this.touch.jump
            );
        }

        attack() {
            return (
                this.down("KeyJ") ||
                this.down("KeyX") ||
                this.touch.attack
            );
        }

        dash() {
            return (
                this.down("ShiftLeft") ||
                this.down("KeyK") ||
                this.touch.dash
            );
        }

        action() {
            return (
                this.down("KeyE") ||
                this.down("Enter") ||
                this.touch.action
            );
        }

        destroy() {
            window.removeEventListener("keydown", this._keydown);
            window.removeEventListener("keyup", this._keyup);

            window.removeEventListener(
                "pointerdown",
                this._pointerdown
            );

            window.removeEventListener(
                "pointerup",
                this._pointerup
            );

            window.removeEventListener(
                "pointermove",
                this._pointermove
            );
        }
    }

    window.AJVYRA_BrowserInput = AJVYRA_BrowserInput;
})();
