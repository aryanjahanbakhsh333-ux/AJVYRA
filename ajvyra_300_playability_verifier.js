(() => {
    "use strict";

    class AJVYRA_300_PlayabilityVerifier {

        constructor(options = {}) {
            this.connector =
                options.connector ||
                window.AJVYRA_300_GAMES_RUNTIME;

            this.runtime =
                options.runtime ||
                window.AJVYRA_RUNTIME ||
                window.AJVYRA_BROWSER?.runtime;

            this.results = new Map();

            this.startedAt = null;
            this.finishedAt = null;
            this.running = false;

            window.AJVYRA_300_VERIFIER = this;
        }

        id(number) {
            return String(number).padStart(3, "0");
        }

        getGame(id) {
            if (!this.connector) return null;

            if (typeof this.connector.get === "function") {
                return this.connector.get(id);
            }

            return null;
        }

        hasLifecycle(game) {
            if (!game) return false;

            return (
                typeof game.initialize === "function" ||
                typeof game.create === "function"
            ) && (
                typeof game.update === "function" ||
                typeof game.tick === "function"
            ) && (
                typeof game.render === "function" ||
                typeof game.draw === "function"
            );
        }

        async verifyDefinition(id) {

            const game = this.getGame(id);

            if (!game) {
                return {
                    id,
                    status: "missing",
                    playable: false,
                    reason: "Game definition not found."
                };
            }

            if (!this.hasLifecycle(game)) {
                return {
                    id,
                    status: "invalid",
                    playable: false,
                    reason:
                        "Game does not expose a complete executable lifecycle."
                };
            }

            return {
                id,
                status: "ready",
                playable: true,
                reason: null
            };
        }

        async verifyAllDefinitions() {

            this.running = true;
            this.startedAt = Date.now();

            this.results.clear();

            for (let number = 1; number <= 300; number++) {

                const id = this.id(number);

                const result =
                    await this.verifyDefinition(id);

                this.results.set(id, result);
            }

            this.running = false;
            this.finishedAt = Date.now();

            return this.getReport();
        }

        async runtimeSmokeTest(id) {

            const game = this.getGame(id);

            if (!game) {
                return {
                    id,
                    playable: false,
                    status: "missing"
                };
            }

            if (!this.runtime) {
                return {
                    id,
                    playable: false,
                    status: "runtime-missing"
                };
            }

            const originalGame =
                this.runtime.game;

            try {

                const executable =
                    this.connector.createExecutableGame
                        ? this.connector.createExecutableGame(game)
                        : game;

                await this.runtime.load(executable);

                /*
                 * اجرای واقعی چند چرخهٔ بازی.
                 * requestAnimationFrame لازم نیست؛
                 * اینجا مستقیماً Lifecycle را Smoke Test می‌کنیم.
                 */

                const dt = 1 / 60;

                for (let frame = 0; frame < 5; frame++) {

                    if (typeof executable.update === "function") {
                        executable.update(
                            dt,
                            this.runtime
                        );
                    }

                    if (typeof executable.render === "function") {
                        executable.render(
                            this.runtime
                        );
                    }
                }

                this.runtime.stop();

                if (originalGame) {
                    this.runtime.game =
                        originalGame;
                }

                return {
                    id,
                    playable: true,
                    status: "runtime-ok",
                    framesTested: 5
                };

            } catch (error) {

                try {
                    this.runtime.stop();
                } catch {}

                return {
                    id,
                    playable: false,
                    status: "runtime-error",
                    error: error?.message ||
                        String(error)
                };
            }
        }

        async verifyRuntimeBatch(start = 1, end = 300) {

            const output = [];

            for (
                let number = start;
                number <= end;
                number++
            ) {

                const id = this.id(number);

                const result =
                    await this.runtimeSmokeTest(id);

                output.push(result);

                const existing =
                    this.results.get(id);

                if (existing) {
                    this.results.set(id, {
                        ...existing,
                        ...result
                    });
                } else {
                    this.results.set(id, result);
                }
            }

            return output;
        }

        getReport() {

            const values =
                Array.from(this.results.values());

            const ready =
                values.filter(
                    x => x.playable === true
                ).length;

            const missing =
                values.filter(
                    x => x.status === "missing"
                ).length;

            const invalid =
                values.filter(
                    x => x.status === "invalid"
                ).length;

            const runtimeErrors =
                values.filter(
                    x => x.status === "runtime-error"
                ).length;

            return {
                total: 300,
                checked: values.length,
                playable: ready,
                missing,
                invalid,
                runtimeErrors,

                percent:
                    values.length
                        ? Math.round(
                            (ready / values.length) * 100
                        )
                        : 0,

                durationMs:
                    this.startedAt &&
                    this.finishedAt
                        ? this.finishedAt -
                          this.startedAt
                        : null,

                results: values
            };
        }

        getMissing() {

            return Array
                .from(this.results.values())
                .filter(
                    x => x.status === "missing"
                )
                .map(x => x.id);
        }

        getBroken() {

            return Array
                .from(this.results.values())
                .filter(
                    x => !x.playable
                )
                .map(x => ({
                    id: x.id,
                    status: x.status,
                    reason: x.reason,
                    error: x.error
                }));
        }

        getPlayableIds() {

            return Array
                .from(this.results.values())
                .filter(
                    x => x.playable
                )
                .map(x => x.id);
        }

        isReadyForPublishing() {

            if (this.results.size !== 300) {
                return false;
            }

            return Array
                .from(this.results.values())
                .every(
                    x => x.playable === true
                );
        }

        printReport() {

            const report =
                this.getReport();

            console.table({
                TOTAL: report.total,
                CHECKED: report.checked,
                PLAYABLE: report.playable,
                MISSING: report.missing,
                INVALID: report.invalid,
                RUNTIME_ERRORS:
                    report.runtimeErrors,
                PERCENT:
                    `${report.percent}%`,
                READY_FOR_PUBLISH:
                    this.isReadyForPublishing()
            });

            if (report.missing > 0) {
                console.warn(
                    "Missing games:",
                    this.getMissing()
                );
            }

            if (report.runtimeErrors > 0) {
                console.warn(
                    "Runtime errors:",
                    this.getBroken()
                );
            }

            return report;
        }

        async runFullVerification() {

            console.log(
                "AJVYRA: Starting 300-game verification..."
            );

            await this.verifyAllDefinitions();

            console.log(
                "AJVYRA: Definition verification complete."
            );

            await this.verifyRuntimeBatch(
                1,
                300
            );

            console.log(
                "AJVYRA: Runtime verification complete."
            );

            return this.printReport();
        }
    }


    /*
     * اتصال خودکار
     */

    function AJVYRA_START_300_VERIFICATION() {

        const verifier =
            new AJVYRA_300_PlayabilityVerifier();

        window.AJVYRA_300_VERIFIER =
            verifier;

        return verifier;
    }


    window.AJVYRA_300_PlayabilityVerifier =
        AJVYRA_300_PlayabilityVerifier;

    window.AJVYRA_START_300_VERIFICATION =
        AJVYRA_START_300_VERIFICATION;


    /*
     * کنترل‌های اختیاری صفحه
     */

    document.addEventListener(
        "DOMContentLoaded",
        () => {

            const verifier =
                window.AJVYRA_300_VERIFIER ||
                AJVYRA_START_300_VERIFICATION();

            const verifyButton =
                document.querySelector(
                    "[data-ajvyra-verify-300]"
                );

            if (verifyButton) {

                verifyButton.addEventListener(
                    "click",
                    async () => {

                        verifyButton.disabled = true;

                        try {

                            await verifier
                                .runFullVerification();

                        } finally {

                            verifyButton.disabled = false;
                        }
                    }
                );
            }
        },
        { once: true }
    );

})();
