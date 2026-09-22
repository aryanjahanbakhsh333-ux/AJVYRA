/*
 * AJVYRA — Final Site Bootstrap Controller
 * File: ajvyra_final_site_bootstrap_controller_v1.js
 *
 * Final order:
 *
 * Release Manifest
 *      ↓
 * Asset Connector
 *      ↓
 * Release Gate
 *      ↓
 * Brand/UI
 *      ↓
 * Player
 */

(function () {
    "use strict";

    if (window.__AJVYRA_FINAL_BOOTSTRAP_V1__) {
        return;
    }

    window.__AJVYRA_FINAL_BOOTSTRAP_V1__ = true;

    const state = {
        catalogReady: false,
        assetsReady: false,
        releaseApproved: false,
        uiReady: false,
        playerReady: false
    };

    function mark(key) {
        state[key] = true;

        window.dispatchEvent(
            new CustomEvent(
                "ajvyra:bootstrap-state",
                {
                    detail: {
                        ...state
                    }
                }
            )
        );
    }

    function start() {
        if (
            !window.AJVYRAReleaseCatalog
        ) {
            console.error(
                "AJVYRA catalog connector is missing."
            );

            return;
        }

        window.AJVYRAReleaseCatalog
            .load()
            .then(() => {
                mark("catalogReady");

                if (
                    window.AJVYRAStorageAssets
                ) {
                    window.AJVYRAStorageAssets.apply();
                    mark("assetsReady");
                }

                const releaseState =
                    window.AJVYRAReleaseCatalog
                        .getState();

                if (
                    window.AJVYRAReleaseGate
                ) {
                    const approved =
                        window.AJVYRAReleaseGate
                            .evaluate(
                                releaseState
                            );

                    if (!approved) {
                        return;
                    }

                    mark("releaseApproved");
                }

                /*
                 * UI
                 */

                if (
                    window.AJVYRAFinalBrandUI
                ) {
                    window.AJVYRAFinalBrandUI
                        .refresh();

                    mark("uiReady");
                }

                /*
                 * Player
                 */

                if (
                    window.AJVYRAReleasePlayer
                ) {
                    mark("playerReady");
                }

                window.dispatchEvent(
                    new CustomEvent(
                        "ajvyra:site-ready",
                        {
                            detail: {
                                ...state
                            }
                        }
                    )
                );
            })
            .catch((error) => {
                console.error(
                    "AJVYRA final bootstrap failed:",
                    error
                );

                if (
                    window.AJVYRAReleaseGate
                ) {
                    window.AJVYRAReleaseGate
                        .evaluate({
                            ready: false,
                            animeCount: 0,
                            errors: [
                                error.message ||
                                "Unknown release bootstrap error."
                            ]
                        });
                }
            });
    }

    window.AJVYRAFinalBootstrap = {
        start,
        getState() {
            return {
                ...state
            };
        }
    };

    /*
     * Wait until DOM is usable.
     */

    if (
        document.readyState ===
        "loading"
    ) {
        document.addEventListener(
            "DOMContentLoaded",
            start,
            {
                once: true
            }
        );
    } else {
        start();
    }

})();
