(function (global) {
    "use strict";

    class AJVYRALandscapeGameShell {
        constructor(options = {}) {
            this.root =
                options.root || document.body;

            this.onReady =
                options.onReady || null;

            this.ready = false;

            this.rotateOverlay =
                null;

            this.boundOrientation =
                () => this.checkOrientation();

            this.create();
        }

        create() {
            this.root.classList.add(
                "ajvyra-game-landscape-root"
            );

            this.rotateOverlay =
                document.createElement("div");

            this.rotateOverlay.style.position =
                "absolute";

            this.rotateOverlay.style.inset =
                "0";

            this.rotateOverlay.style.zIndex =
                "99999";

            this.rotateOverlay.style.display =
                "none";

            this.rotateOverlay.style.alignItems =
                "center";

            this.rotateOverlay.style.justifyContent =
                "center";

            this.rotateOverlay.style.textAlign =
                "center";

            this.rotateOverlay.style.background =
                "#050507";

            this.rotateOverlay.style.color =
                "#ffffff";

            this.rotateOverlay.innerHTML = `
                <div style="
                    max-width:320px;
                    padding:32px;
                    font-family:system-ui;
                ">
                    <div style="
                        font-size:56px;
                        margin-bottom:18px;
                    ">↻</div>

                    <h2 style="
                        margin:0 0 10px;
                    ">
                        Rotate your phone
                    </h2>

                    <p style="
                        opacity:.65;
                        line-height:1.6;
                        margin:0;
                    ">
                        AJVYRA games are designed
                        for a wide landscape screen.
                    </p>
                </div>
            `;

            this.root.appendChild(
                this.rotateOverlay
            );

            window.addEventListener(
                "resize",
                this.boundOrientation
            );

            if (
                screen.orientation
            ) {
                screen.orientation.addEventListener(
                    "change",
                    this.boundOrientation
                );
            }

            this.checkOrientation();
        }

        isLandscape() {
            return (
                window.innerWidth >
                window.innerHeight
            );
        }

        async enterFullscreen() {
            const target =
                this.root;

            if (
                document.fullscreenElement
            ) {
                return true;
            }

            if (
                !target.requestFullscreen
            ) {
                return false;
            }

            try {
                await target.requestFullscreen({
                    navigationUI: "hide"
                });

                return true;
            } catch {
                return false;
            }
        }

        async lockLandscape() {
            if (
                !screen.orientation ||
                !screen.orientation.lock
            ) {
                return false;
            }

            try {
                await screen.orientation.lock(
                    "landscape"
                );

                return true;
            } catch {
                return false;
            }
        }

        async prepare() {
            await this.enterFullscreen();

            await this.lockLandscape();

            this.checkOrientation();

            return this.ready;
        }

        checkOrientation() {
            const landscape =
                this.isLandscape();

            if (
                !this.rotateOverlay
            ) {
                return;
            }

            if (landscape) {
                this.rotateOverlay.style.display =
                    "none";

                if (!this.ready) {
                    this.ready = true;

                    if (
                        typeof this.onReady ===
                        "function"
                    ) {
                        this.onReady();
                    }
                }
            } else {
                this.rotateOverlay.style.display =
                    "flex";

                this.ready = false;
            }
        }

        async exit() {
            if (
                screen.orientation &&
                screen.orientation.unlock
            ) {
                try {
                    screen.orientation.unlock();
                } catch {}
            }

            if (
                document.fullscreenElement &&
                document.exitFullscreen
            ) {
                try {
                    await document.exitFullscreen();
                } catch {}
            }
        }

        destroy() {
            window.removeEventListener(
                "resize",
                this.boundOrientation
            );

            if (
                screen.orientation
            ) {
                screen.orientation.removeEventListener(
                    "change",
                    this.boundOrientation
                );
            }

            this.rotateOverlay?.remove();
        }
    }

    global.AJVYRALandscapeGameShell =
        AJVYRALandscapeGameShell;

})(window);
