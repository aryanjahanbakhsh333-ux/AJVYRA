class AJVYRAWebGameContentRegistry {
    constructor() {
        this.games = new Map();
    }

    register(game) {
        if (!game || !game.id) {
            throw new Error("Game must contain an id.");
        }

        if (this.games.has(game.id)) {
            throw new Error(
                `Game "${game.id}" is already registered.`
            );
        }

        this.games.set(game.id, {
            ...game
        });

        return this.games.get(game.id);
    }

    registerMany(games) {
        if (!Array.isArray(games)) {
            throw new TypeError("Games must be an array.");
        }

        for (const game of games) {
            this.register(game);
        }

        return this;
    }

    get(id) {
        return this.games.get(id) || null;
    }

    has(id) {
        return this.games.has(id);
    }

    remove(id) {
        return this.games.delete(id);
    }

    getAll() {
        return [...this.games.values()];
    }

    getByGenre(genre) {
        return this.getAll().filter(
            game => game.genre === genre
        );
    }

    getByMode(mode) {
        return this.getAll().filter(
            game =>
                Array.isArray(game.modes) &&
                game.modes.includes(mode)
        );
    }

    search(query) {
        const text = String(query || "")
            .trim()
            .toLowerCase();

        if (!text) {
            return this.getAll();
        }

        return this.getAll().filter(game => {
            const haystack = [
                game.id,
                game.title,
                game.description,
                game.genre,
                ...(game.tags || [])
            ]
                .filter(Boolean)
                .join(" ")
                .toLowerCase();

            return haystack.includes(text);
        });
    }

    count() {
        return this.games.size;
    }
}

if (typeof window !== "undefined") {
    window.AJVYRAWebGameContentRegistry =
        AJVYRAWebGameContentRegistry;
}
