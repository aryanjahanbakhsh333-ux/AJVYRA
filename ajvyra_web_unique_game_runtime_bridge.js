(function (global) {
    "use strict";

    class AJVYRAUniqueGameRuntimeBridge {
        constructor(options = {}) {
            this.gameId =
                String(options.gameId);

            this.game =
                global.AJVYRAWeb30UniqueGameProfiles
                    ?.get(this.gameId);

            if (!this.game) {
                throw new Error(
                    `No unique profile for ${this.gameId}`
                );
            }

            this.controls =
                options.controls || null;

            this.story =
                options.story || null;

            this.engine =
                options.engine || null;

            this.bind();
        }

        bind() {
            if (this.controls) {
                this.controls.root.addEventListener(
                    "ajvyra:unique-control",
                    (event) => {
                        this.handleControl(
                            event.detail
                        );
                    }
                );
            }
        }

        handleControl(detail) {
            if (!detail) {
                return;
            }

            const action =
                detail.action;

            const pressed =
                Boolean(detail.pressed);

            if (!pressed) {
                return;
            }

            if (
                this.engine &&
                typeof this.engine.handleUniqueAction ===
                    "function"
            ) {
                this.engine.handleUniqueAction(
                    action
                );
            }

            window.dispatchEvent(
                new CustomEvent(
                    "ajvyra:game-action",
                    {
                        detail: {
                            gameId:
                                this.gameId,
                            action
                        }
                    }
                )
            );
        }

        getProfile() {
            return this.game;
        }

        getControls() {
            return this.game.controls;
        }

        getMechanics() {
            return this.game.mechanics;
        }
    }

    global.AJVYRAUniqueGameRuntimeBridge =
        AJVYRAUniqueGameRuntimeBridge;

})(window);
