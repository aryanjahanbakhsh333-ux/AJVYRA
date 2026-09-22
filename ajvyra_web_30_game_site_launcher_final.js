/* AJVYRA — Final 30 Game Site Launcher
 * New file.
 */

class AJVYRA30GameSiteLauncherFinal {

    constructor(options = {}) {
        this.options = options;

        this.container =
            options.container ||
            document.querySelector(
                "[data-ajvyra-game-container]"
            ) ||
            document.body;

        this.activeGame = null;
        this.canvas = null;

        this.boundKeyboard = null;
        this.boundPointer = null;
        this.boundControl = null;
    }

    resolveGameId(input) {
        if (typeof input === "string") {
            return input;
        }

        if (input?.gameId) {
            return input.gameId;
        }

        const params = new URLSearchParams(
            window.location.search
        );

        return (
            params.get("game") ||
            params.get("gameId") ||
            null
        );
    }

    createCanvas() {
        let canvas =
            this.container.querySelector(
                "canvas[data-ajvyra-game-canvas]"
            );

        if (!canvas) {
            canvas = document.createElement("canvas");

            canvas.dataset.ajvyraGameCanvas = "true";

            canvas.width = 1280;
            canvas.height = 720;

            canvas.style.width = "100%";
            canvas.style.height = "auto";
            canvas.style.display = "block";

            this.container.appendChild(canvas);
        }

        this.canvas = canvas;

        return canvas;
    }

    ensureRuntime(gameId, canvas) {
        if (
            typeof globalThis.AJVYRARealGameplayRuntime !==
            "function"
        ) {
            throw new Error(
                "AJVYRARealGameplayRuntime is not loaded."
            );
        }

        const runtime =
            new globalThis.AJVYRARealGameplayRuntime({
                canvas,
                gameId
            });

        return runtime;
    }

    launch(input) {
        const gameId = this.resolveGameId(input);

        if (!gameId) {
            throw new Error(
                "AJVYRA gameId was not provided."
            );
        }

        const registry =
            globalThis.AJVYRA30GameExperienceRegistry;

        if (!registry?.has?.(gameId)) {
            throw new Error(
                `Game '${gameId}' is not registered.`
            );
        }

        this.close();

        const canvas = this.createCanvas();

        const runtime =
            this.ensureRuntime(
                gameId,
                canvas
            );

        const adapter =
            new globalThis.AJVYRAWebFinalGameRuntimeAdapter(
                runtime,
                gameId
            );

        adapter.attach();
        adapter.start();

        this.activeGame = {
            gameId,
            runtime,
            adapter,
            canvas
        };

        this.bindKeyboard();
        this.bindPointer();
        this.bindUniqueControls();

        document.dispatchEvent(
            new CustomEvent(
                "ajvyra:final-game-launched",
                {
                    detail: {
                        gameId,
                        runtime,
                        adapter
                    }
                }
            )
        );

        return this.activeGame;
    }

    bindKeyboard() {
        this.boundKeyboard = event => {
            if (!this.activeGame) {
                return;
            }

            const key = event.key.toLowerCase();

            const actions = {
                " ": "attack",
                "j": "attack",
                "k": "ability",
                "l": "dash",
                "r": "reload",
                "e": "interact",
                "q": "quest",
                "b": "build",
                "f": "scavenge",
                "d": "dodge",
                "enter": "story-next"
            };

            const action = actions[key];

            if (action) {
                event.preventDefault();

                this.activeGame.adapter.action(
                    action
                );
            }

            if (
                key >= "1" &&
                key <= "9"
            ) {
                const index =
                    Number(key) - 1;

                const choices =
                    this.activeGame
                        .adapter
                        .storyRuntime
                        ?.getChoices?.() || [];

                if (choices[index]) {
                    event.preventDefault();

                    this.activeGame.adapter.action(
                        `choice:${choices[index].id}`
                    );
                }
            }
        };

        window.addEventListener(
            "keydown",
            this.boundKeyboard
        );
    }

    bindPointer() {
        this.boundPointer = event => {
            if (!this.activeGame) {
                return;
            }

            const rect =
                this.canvas.getBoundingClientRect();

            const x =
                event.clientX - rect.left;

            const midpoint =
                rect.width / 2;

            if (x < midpoint) {
                this.activeGame.adapter.action(
                    "attack"
                );
            } else {
                this.activeGame.adapter.action(
                    "ability"
                );
            }
        };

        this.canvas.addEventListener(
            "pointerdown",
            this.boundPointer
        );
    }

    bindUniqueControls() {
        this.boundControl = event => {
            if (!this.activeGame) {
                return;
            }

            const action =
                event.detail?.action;

            if (!action) {
                return;
            }

            this.activeGame.adapter.action(
                action,
                event.detail
            );
        };

        document.addEventListener(
            "ajvyra:unique-control",
            this.boundControl
        );
    }

    action(action, payload = {}) {
        return (
            this.activeGame?.adapter?.action(
                action,
                payload
            ) || false
        );
    }

    getActive() {
        return this.activeGame;
    }

    close() {
        if (this.boundKeyboard) {
            window.removeEventListener(
                "keydown",
                this.boundKeyboard
            );
        }

        if (
            this.boundPointer &&
            this.canvas
        ) {
            this.canvas.removeEventListener(
                "pointerdown",
                this.boundPointer
            );
        }

        if (this.boundControl) {
            document.removeEventListener(
                "ajvyra:unique-control",
                this.boundControl
            );
        }

        try {
            this.activeGame?.adapter?.stop?.();
        } catch (error) {
            console.warn(
                "[AJVYRA] Game close:",
                error
            );
        }

        this.activeGame = null;

        this.boundKeyboard = null;
        this.boundPointer = null;
        this.boundControl = null;
    }
}

globalThis.AJVYRA30GameSiteLauncherFinal =
    AJVYRA30GameSiteLauncherFinal;
