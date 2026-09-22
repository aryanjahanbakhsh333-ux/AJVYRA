class AJVYRAWebGamesReleaseManifest {
    static build() {
        const games =
            AJVYRAWeb30PlayableGames.list;

        return {
            version: "1.0.0",

            requiredGameCount: 30,

            games: games.map(game => ({
                id: game.id,
                title: game.title,
                genre: game.genre,
                mode: game.mode
            }))
        };
    }

    static assert() {
        const manifest =
            this.build();

        if (
            manifest.games.length !==
            manifest.requiredGameCount
        ) {
            throw new Error(
                "Game manifest count mismatch."
            );
        }

        return manifest;
    }
}

window.AJVYRAWebGamesReleaseManifest =
    AJVYRAWebGamesReleaseManifest;
