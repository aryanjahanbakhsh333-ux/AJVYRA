(function (global) {
    "use strict";

    class AJVYRAProfessionalGameSiteController {
        constructor(options = {}) {
            this.mount =
                options.mount ||
                document.body;

            this.catalog =
                options.catalog ||
                global.AJVYRAWeb30GameCatalog;

            this.save =
                options.save ||
                new global.AJVYRAProfessionalGameSave();

            this.activeGame = null;
            this.activeGameId = null;

            this.boundRequest =
                (event) => {
                    const detail =
                        event.detail || {};

                    if (
                        detail.gameId
                    ) {
                        this.launch(
                            detail.gameId
                        );
                    }
                };

            window.addEventListener(
                "ajvyra:game-requested",
                this.boundRequest
            );
        }

        resolveGame(gameId) {
            const id =
                String(gameId);

            if (
                this.catalog &&
                typeof this.catalog.get ===
                    "function"
            ) {
                return this.catalog.get(id);
            }

            if (
                this.catalog &&
                typeof this.catalog.find ===
                    "function"
            ) {
                return this.catalog.find(
                    (game) =>
                        String(game.id) === id
                );
            }

            if (
                Array.isArray(
                    this.catalog
                )
            ) {
                return this.catalog.find(
                    (game) =>
                        String(game.id) === id
                );
            }

            return null;
        }

        createShell(game) {
            const shell =
                document.createElement("section");

            shell.className =
                "ajvyra-professional-game-shell";

            shell.dataset.gameId =
                String(game.id);

            shell.style.position =
                "relative";

            shell.style.width =
                "100%";

            shell.style.maxWidth =
                "1280px";

            shell.style.margin =
                "0 auto";

            shell.style.background =
                "#050507";

            shell.style.border =
                "1px solid rgba(255,255,255,0.10)";

            shell.style.borderRadius =
                "18px";

            shell.style.overflow =
                "hidden";

            const header =
                document.createElement("div");

            header.style.display =
                "flex";

            header.style.justifyContent =
                "space-between";

            header.style.alignItems =
                "center";

            header.style.padding =
                "14px 18px";

            header.style.background =
                "#0a0a0e";

            const title =
                document.createElement("strong");

            title.textContent =
                game.title ||
                game.name ||
                game.id;

            title.style.color =
                "#ffffff";

            const close =
                document.createElement("button");

            close.type = "button";

            close.textContent =
                "EXIT";

            close.style.background =
                "transparent";

            close.style.border =
                "1px solid rgba(255,255,255,0.20)";

            close.style.color =
                "#ffffff";

            close.style.padding =
                "8px 14px";

            close.style.borderRadius =
                "10px";

            close.addEventListener(
                "click",
                () => this.close()
            );

            header.appendChild(title);
            header.appendChild(close);

            const canvas =
                document.createElement("canvas");

            canvas.style.display =
                "block";

            canvas.style.width =
                "100%";

            canvas.style.aspectRatio =
                "16 / 9";

            canvas.style.background =
                "#050507";

            shell.appendChild(header);
            shell.appendChild(canvas);

            return {
                shell,
                canvas
            };
        }

        async launch(gameId) {
            this.close();

            const game =
                this.resolveGame(gameId);

            if (!game) {
                throw new Error(
                    `Unknown AJVYRA game: ${gameId}`
                );
            }

            const parts =
                this.createShell(game);

            this.mount.appendChild(
                parts.shell
            );

            const scenario =
                this.resolveScenario(game);

            const engine =
                new global.AJVYRAProfessionalGameRuntime({
                    canvas:
                        parts.canvas,
                    scenario
                });

            this.activeGame =
                engine;

            this.activeGameId =
                String(game.id);

            const saved =
                await this.save.load(
                    this.activeGameId
                );

            if (
                saved &&
                saved.payload
            ) {
                engine.restoreProfessionalState(
                    saved.payload
                );
            }

            if (
                typeof engine.start ===
                "function"
            ) {
                engine.start();
            }

            engine.startProfessionalLoop();

            window.dispatchEvent(
                new CustomEvent(
                    "ajvyra:game-started",
                    {
                        detail: {
                            gameId:
                                this.activeGameId,
                            title:
                                game.title ||
                                game.name ||
                                game.id
                        }
                    }
                )
            );
        }

        resolveScenario(game) {
            if (
                game.scenario
            ) {
                return game.scenario;
            }

            if (
                global.AJVYRAWeb30GameScenarios &&
                typeof global.AJVYRAWeb30GameScenarios.get ===
                    "function"
            ) {
                return (
                    global.AJVYRAWeb30GameScenarios.get(
                        game.id
                    ) || {}
                );
            }

            return {};
        }

        async saveActiveGame() {
            if (
                !this.activeGame ||
                !this.activeGameId
            ) {
                return false;
            }

            await this.save.save(
                this.activeGameId,
                this.activeGame
                    .getProfessionalState()
            );

            return true;
        }

        async close() {
            if (
                this.activeGame
            ) {
                await this.saveActiveGame();

                this.activeGame.destroy();

                this.activeGame =
                    null;

                this.activeGameId =
                    null;
            }

            const shell =
                this.mount.querySelector(
                    ".ajvyra-professional-game-shell"
                );

            if (shell) {
                shell.remove();
            }

            window.dispatchEvent(
                new CustomEvent(
                    "ajvyra:game-closed"
                )
            );
        }

        destroy() {
            window.removeEventListener(
                "ajvyra:game-requested",
                this.boundRequest
            );

            this.close();
        }
    }

    global.AJVYRAProfessionalGameSiteController =
        AJVYRAProfessionalGameSiteController;

})(window);
