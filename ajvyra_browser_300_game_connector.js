(() => {
    "use strict";

    class AJVYRA_Browser300GameConnector {
        constructor(options = {}) {
            this.runtime =
                options.runtime ||
                window.AJVYRA_RUNTIME ||
                window.AJVYRA_BROWSER?.runtime;

            this.registry =
                options.registry ||
                window.AJVYRA_GAMES ||
                null;

            this.definitions = new Map();
            this.connected = new Set();
            this.currentId = null;

            this.sources = [
                window.AJVYRA_GAME_DEFINITIONS,
                window.AJVYRA_GAMES_DATA,
                window.AJVYRA_GAME_LIBRARY,
                window.AJVYRA_300_GAMES,
                window.AJVYRA_GAMES_LIST
            ];

            this.scanSources();
            this.scanNumberedGames();

            window.AJVYRA_300_CONNECTOR = this;
        }

        normalizeId(id) {
            const raw = String(id)
                .replace(/^game[-_ ]?/i, "")
                .replace(/^0+/, "");

            const number = parseInt(raw, 10);

            if (!Number.isFinite(number)) {
                return null;
            }

            if (number < 1 || number > 300) {
                return null;
            }

            return String(number).padStart(3, "0");
        }

        scanSources() {
            for (const source of this.sources) {
                if (!source) continue;

                if (Array.isArray(source)) {
                    source.forEach((game, index) => {
                        this.registerCandidate(
                            game,
                            index + 1
                        );
                    });

                    continue;
                }

                if (typeof source === "object") {
                    for (const [key, game] of Object.entries(source)) {
                        this.registerCandidate(game, key);
                    }
                }
            }
        }

        scanNumberedGames() {
            for (let i = 1; i <= 300; i++) {
                const id =
                    String(i).padStart(3, "0");

                const names = [
                    `AJVYRA_GAME_${id}`,
                    `AJVYRA_GAME_${i}`,
                    `AJVYRA_GAME${id}`,
                    `AJVYRA_GAME${i}`
                ];

                for (const name of names) {
                    if (window[name]) {
                        this.registerCandidate(
                            window[name],
                            id
                        );
                    }
                }
            }
        }

        registerCandidate(game, fallbackId) {
            if (!game) return;

            const rawId =
                game.id ??
                game.gameId ??
                game.slug ??
                fallbackId;

            const id = this.normalizeId(rawId);

            if (!id) return;

            const normalized = {
                ...game,
                id: `game-${id}`,
                gameNumber: Number(id)
            };

            this.definitions.set(id, normalized);
        }

        get(id) {
            const normalized =
                this.normalizeId(id);

            if (!normalized) return null;

            return (
                this.definitions.get(normalized) ||
                this.findFromRegistry(normalized)
            );
        }

        findFromRegistry(id) {
            if (!this.registry) return null;

            try {
                if (
                    typeof this.registry.getGame ===
                    "function"
                ) {
                    return this.registry.getGame(
                        `game-${id}`
                    );
                }

                if (
                    typeof this.registry.get ===
                    "function"
                ) {
                    return (
                        this.registry.get(
                            `game-${id}`
                        ) ||
                        this.registry.get(id)
                    );
                }

                if (
                    Array.isArray(this.registry)
                ) {
                    return this.registry.find(
                        game =>
                            this.normalizeId(
                                game?.id
                            ) === id
                    );
                }
            } catch (error) {
                console.error(
                    "AJVYRA registry lookup failed:",
                    error
                );
            }

            return null;
        }

        count() {
            return this.definitions.size;
        }

        missingIds() {
            const missing = [];

            for (let i = 1; i <= 300; i++) {
                const id =
                    String(i).padStart(3, "0");

                if (!this.get(id)) {
                    missing.push(id);
                }
            }

            return missing;
        }

        validateGame(game) {
            if (!game) {
                return {
                    valid: false,
                    reason: "Game definition missing."
                };
            }

            const executable =
                typeof game.update === "function" ||
                typeof game.initialize === "function" ||
                typeof game.render === "function" ||
                typeof game.create === "function";

            return {
                valid: executable,
                reason: executable
                    ? null
                    : "Game has no executable lifecycle."
            };
        }

        async play(id) {
            const game = this.get(id);

            if (!game) {
                throw new Error(
                    `AJVYRA: Game ${id} was not found.`
                );
            }

            const validation =
                this.validateGame(game);

            if (!validation.valid) {
                throw new Error(
                    `AJVYRA: Game ${id} is not executable.`
                );
            }

            if (!this.runtime) {
                throw new Error(
                    "AJVYRA: Browser Runtime is unavailable."
                );
            }

            this.currentId =
                this.normalizeId(id);

            const executable =
                this.createExecutableGame(game);

            await this.runtime.load(
                executable
            );

            this.runtime.start();

            this.connected.add(
                this.currentId
            );

            return executable;
        }

        createExecutableGame(game) {
            const original = game;

            return {
                ...original,

                id: original.id,

                async initialize(runtime) {
                    if (
                        typeof original.create ===
                        "function"
                    ) {
                        await original.create(
                            runtime
                        );
                    }

                    if (
                        typeof original.initialize ===
                        "function"
                    ) {
                        await original.initialize(
                            runtime
                        );
                    }

                    if (
                        typeof original.start ===
                        "function"
                    ) {
                        await original.start(
                            runtime
                        );
                    }
                },

                update(dt, runtime) {
                    if (
                        typeof original.update ===
                        "function"
                    ) {
                        original.update(
                            dt,
                            runtime
                        );
                    }

                    if (
                        typeof original.tick ===
                        "function"
                    ) {
                        original.tick(
                            dt,
                            runtime
                        );
                    }
                },

                render(runtime) {
                    if (
                        typeof original.render ===
                        "function"
                    ) {
                        original.render(
                            runtime
                        );
                        return;
                    }

                    if (
                        typeof original.draw ===
                        "function"
                    ) {
                        original.draw(
                            runtime.ctx,
                            runtime
                        );
                    }
                },

                destroy(runtime) {
                    if (
                        typeof original.destroy ===
                        "function"
                    ) {
                        original.destroy(
                            runtime
                        );
                    }

                    if (
                        typeof original.stop ===
                        "function"
                    ) {
                        original.stop(
                            runtime
                        );
                    }
                },

                onPause(runtime) {
                    original.onPause?.(
                        runtime
                    );
                },

                onResume(runtime) {
                    original.onResume?.(
                        runtime
                    );
                }
            };
        }

        async next() {
            const current =
                Number(this.currentId || "000");

            for (
                let i = current + 1;
                i <= 300;
                i++
            ) {
                const id =
                    String(i).padStart(3, "0");

                if (this.get(id)) {
                    return this.play(id);
                }
            }

            return null;
        }

        async previous() {
            const current =
                Number(this.currentId || "001");

            for (
                let i = current - 1;
                i >= 1;
                i--
            ) {
                const id =
                    String(i).padStart(3, "0");

                if (this.get(id)) {
                    return this.play(id);
                }
            }

            return null;
        }

        async playAllAvailable() {
            const results = [];

            for (let i = 1; i <= 300; i++) {
                const id =
                    String(i).padStart(3, "0");

                if (!this.get(id)) {
                    results.push({
                        id,
                        status: "missing"
                    });

                    continue;
                }

                try {
                    await this.play(id);

                    results.push({
                        id,
                        status: "playable"
                    });

                    this.runtime.stop();
                } catch (error) {
                    results.push({
                        id,
                        status: "error",
                        error: error.message
                    });
                }
            }

            return results;
        }

        status() {
            const missing =
                this.missingIds();

            return {
                total: 300,
                discovered: this.count(),
                connected: this.connected.size,
                missing: missing.length,
                missingIds: missing,
                currentGame: this.currentId
            };
        }
    }

    function AJVYRA_CONNECT_300_GAMES() {
        const connector =
            new AJVYRA_Browser300GameConnector();

        window.AJVYRA_300_GAMES_RUNTIME =
            connector;

        return connector;
    }

    window.AJVYRA_Browser300GameConnector =
        AJVYRA_Browser300GameConnector;

    window.AJVYRA_CONNECT_300_GAMES =
        AJVYRA_CONNECT_300_GAMES;

    if (document.readyState === "loading") {
        document.addEventListener(
            "DOMContentLoaded",
            () => {
                AJVYRA_CONNECT_300_GAMES();
            },
            { once: true }
        );
    } else {
        AJVYRA_CONNECT_300_GAMES();
    }
})();
