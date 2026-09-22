(function (global) {
    "use strict";

    class AJVYRAWebFinalGameBoot {
        constructor(options = {}) {
            this.mount =
                options.mount || document.body;

            this.gate =
                new global.AJVYRAWebGameSiteReleaseGate();

            this.launcher =
                new global.AJVYRAMobileGameLauncher({
                    mount: this.mount
                });

            this.ready = false;
        }

        verify() {
            const result =
                this.gate.run();

            this.ready =
                result.approved;

            return result;
        }

        async launch(gameId) {
            if (!this.ready) {
                const result =
                    this.verify();

                if (!result.approved) {
                    throw new Error(
                        "AJVYRA Games are blocked by release gate."
                    );
                }
            }

            if (
                !global.AJVYRAWeb30GameReleaseManifest
                    .has(gameId)
            ) {
                throw new Error(
                    `Unknown release game: ${gameId}`
                );
            }

            return this.launcher.launch(
                gameId
            );
        }

        async close() {
            await this.launcher.close();
        }

        report() {
            return this.gate.getReport();
        }
    }

    global.AJVYRAWebFinalGameBoot =
        AJVYRAWebFinalGameBoot;

})(window);
