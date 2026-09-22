class AJVYRAWebGamesPageController {
    constructor(options = {}) {
        this.registry = options.registry;
        this.launcher = options.launcher;

        this.root = options.root || null;
        this.genreSystem =
            options.genreSystem ||
            new AJVYRAWebGameGenreSystem(
                this.registry
            );

        this.elements = {};
    }

    mount(root) {
        if (!root) {
            throw new Error(
                "Games page root is required."
            );
        }

        this.root = root;

        this.render();
    }

    render() {
        if (!this.root) {
            return;
        }

        this.root.innerHTML = "";

        const page = document.createElement("main");
        page.className = "ajvyra-games-page";

        const hero = document.createElement("header");

        const title = document.createElement("h1");
        title.textContent = "GAMES";

        const subtitle = document.createElement("p");
        subtitle.textContent =
            "Play the AJVYRA collection.";

        hero.append(title, subtitle);

        const genreNavigation =
            document.createElement("nav");

        genreNavigation.className =
            "ajvyra-games-genre-navigation";

        const all = document.createElement("button");

        all.type = "button";
        all.textContent = "All Games";

        all.addEventListener("click", () => {
            this.launcher?.setGenre("all");
        });

        genreNavigation.appendChild(all);

        for (const genre of
            this.genreSystem.getAllGenres()) {

            const games =
                this.genreSystem.getGamesByGenre(
                    genre.id
                );

            if (games.length === 0) {
                continue;
            }

            const button =
                document.createElement("button");

            button.type = "button";

            button.textContent =
                `${genre.icon} ${genre.title} (${games.length})`;

            button.addEventListener("click", () => {
                this.launcher?.setGenre(
                    genre.id
                );
            });

            genreNavigation.appendChild(button);
        }

        const gameArea =
            document.createElement("div");

        gameArea.className =
            "ajvyra-games-launcher-root";

        page.append(
            hero,
            genreNavigation,
            gameArea
        );

        this.root.appendChild(page);

        if (this.launcher) {
            this.launcher.mount(gameArea);
        }
    }
}

if (typeof window !== "undefined") {
    window.AJVYRAWebGamesPageController =
        AJVYRAWebGamesPageController;
}
