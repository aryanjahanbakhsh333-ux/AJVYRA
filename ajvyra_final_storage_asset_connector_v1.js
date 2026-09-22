/*
 * AJVYRA — Final Storage Asset Connector
 * File: ajvyra_final_storage_asset_connector_v1.js
 *
 * Converts release asset paths into final public URLs.
 *
 * Supports:
 * - MP4
 * - Poster
 * - WebVTT subtitles
 */

(function () {
    "use strict";

    if (window.__AJVYRA_STORAGE_ASSET_CONNECTOR_V1__) {
        return;
    }

    window.__AJVYRA_STORAGE_ASSET_CONNECTOR_V1__ = true;

    const CONFIG = {
        baseUrl:
            window.AJVYRA_ASSET_BASE_URL ||
            "",

        requireHttps:
            window.AJVYRA_REQUIRE_HTTPS_ASSETS !== false
    };

    function resolve(path) {
        if (!path) {
            return "";
        }

        if (
            /^https?:\/\//i.test(path)
        ) {
            if (
                CONFIG.requireHttps &&
                !/^https:\/\//i.test(path)
            ) {
                return "";
            }

            return path;
        }

        if (!CONFIG.baseUrl) {
            return path;
        }

        return (
            CONFIG.baseUrl.replace(/\/+$/, "") +
            "/" +
            String(path).replace(/^\/+/, "")
        );
    }

    function attachAssets(release) {
        if (!release) {
            return null;
        }

        return {
            ...release,

            poster:
                resolve(
                    release.poster
                ),

            video:
                resolve(
                    release.video
                ),

            subtitle:
                resolve(
                    release.subtitle
                )
        };
    }

    function attachCatalog(catalog) {
        if (!Array.isArray(catalog)) {
            return [];
        }

        return catalog.map(
            attachAssets
        );
    }

    function apply() {
        if (
            Array.isArray(
                window.AJVYRA_FINAL_ANIME_CATALOG
            )
        ) {
            window.AJVYRA_FINAL_ANIME_CATALOG =
                attachCatalog(
                    window.AJVYRA_FINAL_ANIME_CATALOG
                );
        }

        if (
            Array.isArray(
                window.AJVYRA_FINAL_GAME_CATALOG
            )
        ) {
            window.AJVYRA_FINAL_GAME_CATALOG =
                attachCatalog(
                    window.AJVYRA_FINAL_GAME_CATALOG
                );
        }

        window.dispatchEvent(
            new CustomEvent(
                "ajvyra:assets-connected"
            )
        );
    }

    window.AJVYRAStorageAssets = {
        resolve,
        attachAssets,
        attachCatalog,
        apply
    };

    window.addEventListener(
        "ajvyra:release-catalog-ready",
        apply
    );

})();
