/*
 * AJVYRA — Final Release Catalog Connector
 * File: ajvyra_final_release_catalog_connector_v1.js
 *
 * Role:
 * Final release manifest -> validated anime/game catalog
 *
 * No generation.
 * No fake media.
 * No runtime video creation.
 */

(function () {
    "use strict";

    if (window.__AJVYRA_RELEASE_CATALOG_CONNECTOR_V1__) {
        return;
    }

    window.__AJVYRA_RELEASE_CATALOG_CONNECTOR_V1__ = true;

    const CONFIG = {
        manifestUrl:
            window.AJVYRA_RELEASE_MANIFEST_URL ||
            "assets/releases/ajvyra-final-release-manifest.json",

        expectedAnimeCount: 30,

        strict: true
    };

    function normalizeRelease(item) {
        if (!item || typeof item !== "object") {
            return null;
        }

        const title =
            item.title ||
            item.name ||
            "";

        if (!title.trim()) {
            return null;
        }

        return {
            id:
                item.id ||
                item.slug ||
                title.toLowerCase()
                    .replace(/[^a-z0-9]+/g, "-")
                    .replace(/^-|-$/g, ""),

            title,

            description:
                item.description ||
                item.synopsis ||
                "",

            poster:
                item.poster ||
                item.posterUrl ||
                item.cover ||
                "",

            video:
                item.video ||
                item.videoUrl ||
                item.mediaUrl ||
                item.mp4 ||
                "",

            subtitle:
                item.subtitle ||
                item.subtitleUrl ||
                item.vtt ||
                "",

            duration:
                Number.isFinite(Number(item.duration))
                    ? Number(item.duration)
                    : null,

            type:
                item.type ||
                "anime",

            ready:
                item.ready === true,

            published:
                item.published === true
        };
    }

    function extractAnime(manifest) {
        if (Array.isArray(manifest)) {
            return manifest;
        }

        if (
            manifest &&
            Array.isArray(manifest.anime)
        ) {
            return manifest.anime;
        }

        if (
            manifest &&
            Array.isArray(manifest.films)
        ) {
            return manifest.films;
        }

        if (
            manifest &&
            manifest.releases &&
            Array.isArray(manifest.releases.anime)
        ) {
            return manifest.releases.anime;
        }

        return [];
    }

    function extractGames(manifest) {
        if (
            manifest &&
            Array.isArray(manifest.games)
        ) {
            return manifest.games;
        }

        if (
            manifest &&
            manifest.releases &&
            Array.isArray(manifest.releases.games)
        ) {
            return manifest.releases.games;
        }

        return [];
    }

    function validateAnime(anime) {
        const errors = [];

        if (
            anime.length !==
            CONFIG.expectedAnimeCount
        ) {
            errors.push(
                `Expected ${CONFIG.expectedAnimeCount} anime releases, received ${anime.length}.`
            );
        }

        anime.forEach((item, index) => {
            if (!item.title) {
                errors.push(
                    `Anime #${index + 1} has no title.`
                );
            }

            if (!item.ready) {
                errors.push(
                    `${item.title || `Anime #${index + 1}`} is not READY.`
                );
            }

            if (!item.published) {
                errors.push(
                    `${item.title || `Anime #${index + 1}`} is not PUBLISHED.`
                );
            }

            if (!item.video) {
                errors.push(
                    `${item.title || `Anime #${index + 1}`} has no video URL.`
                );
            }
        });

        return errors;
    }

    async function load() {
        const response =
            await fetch(CONFIG.manifestUrl, {
                cache: "no-store"
            });

        if (!response.ok) {
            throw new Error(
                `Release manifest request failed: HTTP ${response.status}`
            );
        }

        const manifest =
            await response.json();

        const anime =
            extractAnime(manifest)
                .map(normalizeRelease)
                .filter(Boolean);

        const games =
            extractGames(manifest)
                .map(normalizeRelease)
                .filter(Boolean);

        const errors =
            validateAnime(anime);

        const ready =
            errors.length === 0;

        if (
            CONFIG.strict &&
            !ready
        ) {
            const error =
                new Error(
                    "AJVYRA release catalog is not production-ready."
                );

            error.code =
                "AJVYRA_RELEASE_CATALOG_INVALID";

            error.details = errors;

            throw error;
        }

        window.AJVYRA_FINAL_ANIME_CATALOG =
            anime;

        window.AJVYRA_FINAL_GAME_CATALOG =
            games;

        window.AJVYRA_FINAL_RELEASE_STATE = {
            ready,
            animeCount: anime.length,
            gameCount: games.length,
            errors,
            loadedAt:
                new Date().toISOString()
        };

        window.dispatchEvent(
            new CustomEvent(
                "ajvyra:release-catalog-ready",
                {
                    detail:
                        window.AJVYRA_FINAL_RELEASE_STATE
                }
            )
        );

        return window.AJVYRA_FINAL_RELEASE_STATE;
    }

    window.AJVYRAReleaseCatalog = {
        load,
        getAnime() {
            return (
                window.AJVYRA_FINAL_ANIME_CATALOG ||
                []
            );
        },
        getGames() {
            return (
                window.AJVYRA_FINAL_GAME_CATALOG ||
                []
            );
        },
        getState() {
            return (
                window.AJVYRA_FINAL_RELEASE_STATE ||
                null
            );
        }
    };

})();
