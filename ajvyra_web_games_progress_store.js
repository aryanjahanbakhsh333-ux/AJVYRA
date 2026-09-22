class AJVYRAWebGamesProgressStore {
    constructor(
        key = "ajvyra_games_progress"
    ) {
        this.key = key;
    }

    readAll() {
        try {
            return JSON.parse(
                localStorage.getItem(
                    this.key
                ) || "{}"
            );
        } catch {
            return {};
        }
    }

    get(gameId) {
        return this.readAll()[gameId] || null;
    }

    save(gameId, progress) {
        const all =
            this.readAll();

        all[gameId] = {
            ...(all[gameId] || {}),
            ...progress,
            updatedAt:
                new Date().toISOString()
        };

        localStorage.setItem(
            this.key,
            JSON.stringify(all)
        );

        return all[gameId];
    }

    clear(gameId) {
        const all =
            this.readAll();

        delete all[gameId];

        localStorage.setItem(
            this.key,
            JSON.stringify(all)
        );
    }
}

window.AJVYRAWebGamesProgressStore =
    AJVYRAWebGamesProgressStore;
