class AJVYRAWebGamesSiteBridge {
    constructor(options = {}) {
        this.root =
            options.root || null;

        this.host = null;

        this.handler =
            event => this.handle(event);
    }

    connect(root = this.root) {
        if (!root) {
            throw new Error(
                "AJVYRA Games root is required."
            );
        }

        this.root = root;

        window.addEventListener(
            "ajvyra:game-requested",
            this.handler
        );

        return this;
    }

    handle(event) {
        const detail =
            event?.detail || {};

        const id =
            detail.id ||
            detail.gameId;

        if (!id) {
            return;
        }

        const game =
            AJVYRAWeb30PlayableGames.byId(id);

        if (!game) {
            throw new Error(
                `Unknown AJVYRA game: ${id}`
            );
        }

        if (this.host) {
            this.host.stop();
        }

        this.host =
            new AJVYRAWebPlayableGameHost();

        this.host.mount(this.root);
        this.host.load(game);
    }

    disconnect() {
        window.removeEventListener(
            "ajvyra:game-requested",
            this.handler
        );

        this.host?.stop();
        this.host = null;
    }
}

window.AJVYRAWebGamesSiteBridge =
    AJVYRAWebGamesSiteBridge;
