class AJVYRAWebGamesLauncher {
    constructor(options = {}) {
        this.registry = options.registry || null;
        this.contentRuntime = options.contentRuntime || null;

        this.container = options.container || null;
        this.onPlay = options.onPlay || (() => {});

        this.selectedGenre = "all";
        this.searchQuery = "";
        this.currentGame = null;
    }

    mount(container) {
        if (!container) {
            throw new Error("Games launcher container is required.");
        }

        this.container = container;
        this.render();
    }

    setGenre(genre) {
        this.selectedGenre = genre || "all";
        this.render();
    }

    search(query) {
        this.searchQuery = String(query || "").trim();
        this.render();
    }

    getGames() {
        if (!this.registry) {
            return [];
        }

        let games = this.registry.getAll();

        if (this.selectedGenre !== "all") {
            games = games.filter(
                game => game.genre === this.selectedGenre
            );
        }

        if (this.searchQuery) {
            const query = this.searchQuery.toLowerCase();

            games = games.filter(game => {
                const text = [
                    game.title,
                    game.genre,
                    game.description,
                    ...(game.tags || [])
                ]
                    .filter(Boolean)
                    .join(" ")
                    .toLowerCase();

                return text.includes(query);
            });
        }

        return games;
    }

    getGenres() {
        if (!this.registry) {
            return [];
        }

        return [
            ...new Set(
                this.registry
                    .getAll()
                    .map(game => game.genre)
                    .filter(Boolean)
            )
        ];
    }

    playGame(gameId) {
        if (!this.registry) {
            return false;
        }

        const game = this.registry.get(gameId);

        if (!game) {
            return false;
        }

        this.currentGame = game;

        if (this.contentRuntime) {
            this.contentRuntime.loadGame(game);
        }

        this.onPlay(game);

        return true;
    }

    render() {
        if (!this.container) {
            return;
        }

        const games = this.getGames();
        const genres = this.getGenres();

        this.container.innerHTML = "";

        const wrapper = document.createElement("section");
        wrapper.className = "ajvyra-games-launcher";

        const header = document.createElement("div");
        header.className = "ajvyra-games-header";

        const title = document.createElement("h1");
        title.textContent = "AJVYRA GAMES";

        const count = document.createElement("span");
        count.textContent = `${games.length} games`;

        header.append(title, count);

        const controls = document.createElement("div");
        controls.className = "ajvyra-games-controls";

        const search = document.createElement("input");
        search.type = "search";
        search.placeholder = "Search games...";
        search.value = this.searchQuery;

        search.addEventListener("input", event => {
            this.searchQuery = event.target.value;
            this.render();
        });

        controls.appendChild(search);

        const genreBar = document.createElement("div");
        genreBar.className = "ajvyra-game-genres";

        const allButton = this.createGenreButton(
            "all",
            "All"
        );

        genreBar.appendChild(allButton);

        genres.forEach(genre => {
            genreBar.appendChild(
                this.createGenreButton(
                    genre,
                    this.formatGenre(genre)
                )
            );
        });

        const grid = document.createElement("div");
        grid.className = "ajvyra-games-grid";

        games.forEach(game => {
            grid.appendChild(this.createGameCard(game));
        });

        wrapper.append(
            header,
            controls,
            genreBar,
            grid
        );

        this.container.appendChild(wrapper);
    }

    createGenreButton(value, label) {
        const button = document.createElement("button");

        button.type = "button";
        button.textContent = label;

        if (this.selectedGenre === value) {
            button.dataset.active = "true";
        }

        button.addEventListener("click", () => {
            this.setGenre(value);
        });

        return button;
    }

    createGameCard(game) {
        const card = document.createElement("article");
        card.className = "ajvyra-game-card";

        const title = document.createElement("h2");
        title.textContent = game.title;

        const genre = document.createElement("span");
        genre.textContent = this.formatGenre(game.genre);

        const description = document.createElement("p");
        description.textContent =
            game.description || "AJVYRA game.";

        const modes = document.createElement("small");
        modes.textContent =
            (game.modes || ["singleplayer"])
                .join(" • ");

        const play = document.createElement("button");
        play.type = "button";
        play.textContent = "PLAY";

        play.addEventListener("click", () => {
            this.playGame(game.id);
        });

        card.append(
            title,
            genre,
            description,
            modes,
            play
        );

        return card;
    }

    formatGenre(genre) {
        return String(genre || "")
            .replace(/[-_]/g, " ")
            .replace(/\b\w/g, char => char.toUpperCase());
    }
}

if (typeof window !== "undefined") {
    window.AJVYRAWebGamesLauncher =
        AJVYRAWebGamesLauncher;
}
