class AJVYRAWebGameGenreSystem {
    constructor(registry = null) {
        this.registry = registry;
        this.genreMetadata = new Map();

        this.registerDefaults();
    }

    registerGenre(id, metadata = {}) {
        if (!id) {
            throw new Error("Genre ID is required.");
        }

        this.genreMetadata.set(id, {
            id,
            title: metadata.title || id,
            description: metadata.description || "",
            icon: metadata.icon || "🎮"
        });
    }

    registerDefaults() {
        const genres = [
            ["action", "Action", "Fast-paced combat and movement.", "⚔️"],
            ["rpg", "RPG", "Characters, progression, quests and worlds.", "🗡️"],
            ["racing", "Racing", "Speed, vehicles and competition.", "🏎️"],
            ["horror", "Horror", "Dark exploration and survival.", "🌑"],
            ["shooter", "Shooter", "Aim, combat and ranged battles.", "🎯"],
            ["adventure", "Adventure", "Exploration and story-driven gameplay.", "🧭"],
            ["fighting", "Fighting", "Close-range competitive combat.", "🥊"],
            ["strategy", "Strategy", "Planning, resources and tactical decisions.", "♟️"],
            ["survival", "Survival", "Resource management and staying alive.", "🔥"],
            ["puzzle", "Puzzle", "Logic, timing and problem solving.", "🧩"],
            ["arcade", "Arcade", "Short, fast and score-driven gameplay.", "🕹️"],
            ["boss", "Boss Battle", "Focused battles against powerful enemies.", "👹"]
        ];

        for (const [id, title, description, icon] of genres) {
            this.registerGenre(id, {
                title,
                description,
                icon
            });
        }
    }

    getGenre(id) {
        return this.genreMetadata.get(id) || null;
    }

    getAllGenres() {
        return [...this.genreMetadata.values()];
    }

    getGamesByGenre(id) {
        if (!this.registry) {
            return [];
        }

        return this.registry.getByGenre(id);
    }

    getGenreCounts() {
        const counts = {};

        for (const genre of this.getAllGenres()) {
            counts[genre.id] =
                this.getGamesByGenre(genre.id).length;
        }

        return counts;
    }
}

if (typeof window !== "undefined") {
    window.AJVYRAWebGameGenreSystem =
        AJVYRAWebGameGenreSystem;
}
