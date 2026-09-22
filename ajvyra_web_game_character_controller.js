"use strict";

class AJVYRAWebCharacterController {
    constructor(character, input, options = {}) {
        if (!character) {
            throw new TypeError(
                "Character is required."
            );
        }

        if (!input) {
            throw new TypeError(
                "Input runtime is required."
            );
        }

        this.character = character;
        this.input = input;

        this.moveLeftAction =
            options.moveLeftAction || "move_left";

        this.moveRightAction =
            options.moveRightAction || "move_right";

        this.jumpAction =
            options.jumpAction || "jump";

        this.runAction =
            options.runAction || "run";

        this.attackAction =
            options.attackAction || "primary";
    }

    update() {
        if (!this.character.isAlive()) {
            return;
        }

        let direction = 0;

        if (
            this.input.isActionDown(
                this.moveLeftAction
            )
        ) {
            direction -= 1;
        }

        if (
            this.input.isActionDown(
                this.moveRightAction
            )
        ) {
            direction += 1;
        }

        const running =
            this.input.isActionDown(
                this.runAction
            );

        this.character.move(
            direction,
            running
        );

        if (
            this.input.wasActionPressed &&
            this.input.wasActionPressed(
                this.jumpAction
            )
        ) {
            this.character.jump();
        }
    }
}

window.AJVYRAWebCharacterController =
    AJVYRAWebCharacterController;
