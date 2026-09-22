(function (window) {
    "use strict";

    class AJVYRACinematicWebCatalog {
        constructor(manifestUrl) {
            this.manifestUrl =
                manifestUrl || "/cinematic_player_manifest.json";

            this.movies = [];
            this.loaded = false;
        }

        async load() {
            const response = await fetch(this.manifestUrl, {
                cache: "no-store"
            });

            if (!response.ok) {
                throw new Error(
                    `Cinematic manifest request failed: ${response.status}`
                );
            }

            const payload = await response.json();

            if (!payload || !Array.isArray(payload.movies)) {
                throw new Error(
                    "Invalid AJVYRA cinematic manifest."
                );
            }

            this.movies = payload.movies.filter(
                movie =>
                    movie &&
                    movie.watchable === true &&
                    typeof movie.movie_url === "string" &&
                    movie.movie_url.trim() !== ""
            );

            this.loaded = true;

            return this.movies;
        }

        getAll() {
            return [...this.movies];
        }

        getById(filmId) {
            return this.movies.find(
                movie => movie.film_id === filmId
            ) || null;
        }

        search(query) {
            const value = String(query || "")
                .trim()
                .toLowerCase();

            if (!value) {
                return this.getAll();
            }

            return this.movies.filter(movie => {
                const title =
                    String(movie.title || "").toLowerCase();

                const genre =
                    String(movie.genre || "").toLowerCase();

                const filmId =
                    String(movie.film_id || "").toLowerCase();

                return (
                    title.includes(value) ||
                    genre.includes(value) ||
                    filmId.includes(value)
                );
            });
        }

        genres() {
            return [
                ...new Set(
                    this.movies
                        .map(movie => String(movie.genre || "").trim())
                        .filter(Boolean)
                )
            ];
        }
    }

    window.AJVYRACinematicWebCatalog =
        AJVYRACinematicWebCatalog;
})(window);
