(function (window) {
    "use strict";

    class AJVYRACinematicWebLibrary {
        constructor(container, catalog) {
            if (!container) {
                throw new Error(
                    "Library container is required."
                );
            }

            if (!catalog) {
                throw new Error(
                    "Cinematic catalog is required."
                );
            }

            this.container = container;
            this.catalog = catalog;
            this.onSelect = null;
        }

        setSelectHandler(callback) {
            this.onSelect =
                typeof callback === "function"
                    ? callback
                    : null;
        }

        render(movies) {
            const items =
                Array.isArray(movies)
                    ? movies
                    : this.catalog.getAll();

            this.container.innerHTML = "";

            if (!items.length) {
                const empty =
                    document.createElement("div");

                empty.className =
                    "ajvyra-cinematic-empty";

                empty.textContent =
                    "No cinematic films are currently available.";

                this.container.appendChild(empty);
                return;
            }

            items.forEach(movie => {
                this.container.appendChild(
                    this.createCard(movie)
                );
            });
        }

        createCard(movie) {
            const card =
                document.createElement("article");

            card.className =
                "ajvyra-cinematic-card";

            card.dataset.filmId =
                movie.film_id || "";

            const poster =
                document.createElement("img");

            poster.className =
                "ajvyra-cinematic-poster";

            poster.alt =
                `${movie.title || "Cinematic anime"} poster`;

            if (movie.poster_url) {
                poster.src =
                    movie.poster_url;
            } else {
                poster.alt =
                    `${movie.title || "Cinematic anime"} poster unavailable`;
            }

            const body =
                document.createElement("div");

            body.className =
                "ajvyra-cinematic-card-body";

            const title =
                document.createElement("h3");

            title.textContent =
                movie.title || movie.film_id;

            const genre =
                document.createElement("span");

            genre.textContent =
                movie.genre || "Cinematic Anime";

            const button =
                document.createElement("button");

            button.type = "button";
            button.textContent = "Play";

            button.addEventListener(
                "click",
                () => {
                    if (this.onSelect) {
                        this.onSelect(movie);
                    }
                }
            );

            body.appendChild(title);
            body.appendChild(genre);
            body.appendChild(button);

            card.appendChild(poster);
            card.appendChild(body);

            return card;
        }
    }

    window.AJVYRACinematicWebLibrary =
        AJVYRACinematicWebLibrary;
})(window);
