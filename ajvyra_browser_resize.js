(() => {
    "use strict";

    class AJVYRA_BrowserResize {
        constructor(runtime) {
            this.runtime = runtime;
            this.canvas = runtime.canvas;

            this.maxDPR = 2;

            this.resize = this.resize.bind(this);

            window.addEventListener(
                "resize",
                this.resize
            );

            window.addEventListener(
                "orientationchange",
                this.resize
            );

            this.resize();
        }

        resize() {
            const rect =
                this.canvas.getBoundingClientRect();

            const width =
                Math.max(1, Math.floor(rect.width));

            const height =
                Math.max(1, Math.floor(rect.height));

            const dpr =
                Math.min(
                    window.devicePixelRatio || 1,
                    this.maxDPR
                );

            this.canvas.width =
                Math.floor(width * dpr);

            this.canvas.height =
                Math.floor(height * dpr);

            this.runtime.ctx.setTransform(
                dpr,
                0,
                0,
                dpr,
                0,
                0
            );
        }

        isMobile() {
            return (
                window.matchMedia(
                    "(pointer: coarse)"
                ).matches ||
                /Android|iPhone|iPad|iPod/i.test(
                    navigator.userAgent
                )
            );
        }

        isLandscape() {
            return window.matchMedia(
                "(orientation: landscape)"
            ).matches;
        }

        destroy() {
            window.removeEventListener(
                "resize",
                this.resize
            );

            window.removeEventListener(
                "orientationchange",
                this.resize
            );
        }
    }

    window.AJVYRA_BrowserResize = AJVYRA_BrowserResize;
})();
