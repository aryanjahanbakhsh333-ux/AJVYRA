(function (global) {
    "use strict";

    class AJVYRA30GamesFinalConnection {

        constructor() {
            this.active = null;
        }

        launch(options = {}) {
            const gameId =
                options.gameId ||
                this.readGameId();

            if (!gameId) {
                throw new Error(
                    "AJVYRA gameId is required."
                );
            }

            const Registry =
                global.AJVYRA30GameExperienceRegistry;

            if (!Registry) {
                throw new Error(
                    "AJVYRA game registry unavailable."
                );
            }

            const profile =
                Registry.get(gameId);

            if (!profile) {
                throw new Error(
                    `Game ${gameId} is not registered.`
                );
            }

            const canvas =
                options.canvas ||
                this.createCanvas();

            const Runtime =
                global.AJVYRARealGameplayRuntime;

            if (!Runtime) {
                throw new Error(
                    "AJVYRARealGameplayRuntime unavailable."
                );
            }

            const runtime =
                new Runtime({
                    gameId,
                    canvas,
                    profile
                });

            if (
                typeof runtime.start ===
                "function"
            ) {
                runtime.start();
            }

            const Experience =
                global.AJVYRA30GameFinalExperience;

            if (!Experience) {
                throw new Error(
                    "Final game experience unavailable."
                );
            }

            const experience =
                new Experience(
                    runtime,
                    gameId
                );

            experience.initialize();
            experience.start();

            this.active = {
                gameId,
                profile,
                canvas,
                runtime,
                experience
            };

            this.bindInput(
                this.active
            );

            return this.active;
        }

        createCanvas() {
            const canvas =
                document.createElement(
                    "canvas"
                );

            canvas.width = 1280;
            canvas.height = 720;

            canvas.style.width =
                "100%";

            canvas.style.height =
                "auto";

            canvas.setAttribute(
                "aria-label",
                "AJVYRA game canvas"
            );

            document.body.appendChild(
                canvas
            );

            return canvas;
        }

        readGameId() {
            const query =
                new URLSearchParams(
                    window.location.search
                );

            return (
                query.get("game") ||
                document.body.dataset.gameId ||
                null
            );
        }

        bindInput(active) {
            const {
                canvas,
                experience
            } = active;

            const keys =
                new Set();

            window.addEventListener(
                "keydown",
                event => {
                    keys.add(
                        event.key.toLowerCase()
                    );

                    const action =
                        this.keyToAction(
                            event.key
                        );

                    if (action) {
                        experience.action(
                            action
                        );
                    }
                }
            );

            window.addEventListener(
                "keyup",
                event => {
                    keys.delete(
                        event.key.toLowerCase()
                    );
                }
            );

            canvas.addEventListener(
                "pointerdown",
                event => {
                    const rect =
                        canvas.getBoundingClientRect();

                    const x =
                        event.clientX -
                        rect.left;

                    const half =
                        rect.width / 2;

                    if (x < half) {
                        experience.action(
                            "attack"
                        );
                    } else {
                        experience.action(
                            "ability"
                        );
                    }
                }
            );
        }

        keyToAction(key) {
            switch (
                String(key).toLowerCase()
            ) {
                case " ":
                    return "attack";

                case "j":
                    return "attack";

                case "k":
                    return "ability";

                case "l":
                    return "dash";

                case "r":
                    return "reload";

                case "e":
                    return "interact";

                case "q":
                    return "quest";

                case "b":
                    return "build";

                case "f":
                    return "scavenge";

                case "d":
                    return "dodge";

                default:
                    return null;
            }
        }

        action(action, payload = {}) {
            if (!this.active) {
                return false;
            }

            return this.active.experience.action(
                action,
                payload
            );
        }

        getActiveGame() {
            return this.active;
        }

        close() {
            if (!this.active) {
                return;
            }

            const runtime =
                this.active.runtime;

            if (
                runtime &&
                typeof runtime.stop ===
                "function"
            ) {
                runtime.stop();
            }

            this.active = null;
        }
    }

    global.AJVYRA30GamesFinalConnection =
        AJVYRA30GamesFinalConnection;

})(window);
