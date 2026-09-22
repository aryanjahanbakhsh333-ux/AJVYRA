class AJVYRAWebGamesBootstrap {
    constructor(options = {}) {
        this.root =
            options.root ||
            document.querySelector(
                "[data-ajvyra-games]"
            );

        this.registry =
            options.registry ||
            new AJVYRAWebGameContentRegistry();

        this.contentRuntime =
            options.contentRuntime ||
            new AJVYRAWebGameContentRuntime({
                registry: this.registry
            });

        this.launcherRuntime =
            options.launcherRuntime ||
            new AJVYRAWebGameLauncherRuntime({
                registry: this.registry,
                contentRuntime: this.contentRuntime
            });

        this.launcher =
            options.launcher ||
            new AJVYRAWebGamesLauncher({
                registry: this.registry,
                contentRuntime: this.contentRuntime,
                onPlay: game =>
                    this.openGame(game)
            });

        this.page =
            options.page ||
            new AJVYRAWebGamesPageController({
                registry: this.registry,
                launcher: this.launcher
            });

        this.initialized = false;
    }

    initialize() {
        if (this.initialized) {
            return;
        }

        if (!this.root) {
            throw new Error(
                "AJVYRA Games root element was not found."
            );
        }

        if (
            typeof AJVYRAWeb30GameCatalog !==
            "undefined"
        ) {
            this.registry.registerMany(
                AJVYRAWeb30GameCatalog
            );
        }

        this.page.mount(this.root);

        this.initialized = true;
    }

    openGame(game) {
        if (!game || !game.id) {
            return;
        }

        this.launcherRuntime.load(game.id);

        /*
         * The actual gameplay surface will be
         * mounted by the next integration layer.
         *
         * We intentionally do not pretend that
         * clicking PLAY already means the complete
         * game exists.
         */
        const event =
            new CustomEvent(
                "ajvyra:game-requested",
                {
                    detail: {
                        game
                    }
                }
            );

        window.dispatchEvent(event);
    }

    getRegisteredGames() {
        return this.registry.getAll();
    }

    getGameCount() {
        return this.registry.count();
    }
}

if (typeof window !== "undefined") {
    window.AJVYRAWebGamesBootstrap =
        AJVYRAWebGamesBootstrap;
}
