(function (window, document) {
    "use strict";

    async function bootAJVYRACinematicSite(config) {
        const settings = Object.assign(
            {
                manifestUrl:
                    "/cinematic_player_manifest.json",
                librarySelector:
                    "[data-ajvyra-cinematic-library]",
                videoSelector:
                    "[data-ajvyra-cinematic-player]",
                statusSelector:
                    "[data-ajvyra-cinematic-status]"
            },
            config || {}
        );

        const libraryElement =
            document.querySelector(
                settings.librarySelector
            );

        const videoElement =
            document.querySelector(
                settings.videoSelector
            );

        const statusElement =
            document.querySelector(
                settings.statusSelector
            );

        if (!libraryElement) {
            throw new Error(
                "AJVYRA cinematic library element was not found."
            );
        }

        if (!videoElement) {
            throw new Error(
                "AJVYRA cinematic video element was not found."
            );
        }

        const catalog =
            new window.AJVYRACinematicWebCatalog(
                settings.manifestUrl
            );

        const player =
            new window.AJVYRACinematicWebPlayer(
                videoElement
            );

        const library =
            new window.AJVYRACinematicWebLibrary(
                libraryElement,
                catalog
            );

        const setStatus = message => {
            if (statusElement) {
                statusElement.textContent =
                    message;
            }
        };

        setStatus("Loading cinematic library...");

        try {
            await catalog.load();

            library.setSelectHandler(
                movie => {
                    setStatus(
                        `Playing ${movie.title || movie.film_id}`
                    );

                    player.playMovie(movie)
                        .catch(error => {
                            setStatus(
                                `Playback failed: ${error.message}`
                            );
                        });
                }
            );

            library.render();

            setStatus(
                `${catalog.getAll().length} cinematic films available`
            );

            return {
                catalog,
                player,
                library
            };
        } catch (error) {
            setStatus(
                `Cinematic library unavailable: ${error.message}`
            );

            throw error;
        }
    }

    window.bootAJVYRACinematicSite =
        bootAJVYRACinematicSite;
})(window, document);
