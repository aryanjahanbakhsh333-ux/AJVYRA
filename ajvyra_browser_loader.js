(() => {
    "use strict";

    class AJVYRA_BrowserLoader {
        constructor() {
            this.loaded = new Set();
        }

        async load(game) {
            if (!game) {
                throw new Error("AJVYRA Loader: game missing.");
            }

            if (typeof game.assets === "function") {
                const assets = await game.assets();

                if (Array.isArray(assets)) {
                    await Promise.all(
                        assets.map(asset =>
                            this.loadAsset(asset)
                        )
                    );
                }
            }

            this.loaded.add(
                game.id || game.slug || "unknown"
            );

            return game;
        }

        loadAsset(asset) {
            return new Promise((resolve, reject) => {
                if (!asset?.src) {
                    resolve(null);
                    return;
                }

                const image = new Image();

                image.onload = () =>
                    resolve(image);

                image.onerror = () =>
                    reject(
                        new Error(
                            `AJVYRA: asset failed: ${asset.src}`
                        )
                    );

                image.src = asset.src;
            });
        }
    }

    window.AJVYRA_BrowserLoader = AJVYRA_BrowserLoader;
})();
