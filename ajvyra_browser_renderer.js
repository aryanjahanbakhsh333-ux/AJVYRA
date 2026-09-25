(() => {
    "use strict";

    class AJVYRA_BrowserRenderer {
        constructor(runtime) {
            this.runtime = runtime;
            this.canvas = runtime.canvas;
            this.ctx = runtime.ctx;

            this.background = "#050505";
        }

        beginFrame() {
            const width = this.canvas.width;
            const height = this.canvas.height;

            this.ctx.setTransform(1, 0, 0, 1, 0, 0);

            this.ctx.fillStyle = this.background;
            this.ctx.fillRect(0, 0, width, height);
        }

        endFrame() {
            this.ctx.setTransform(1, 0, 0, 1, 0, 0);
        }

        clear(color = this.background) {
            this.ctx.fillStyle = color;

            this.ctx.fillRect(
                0,
                0,
                this.canvas.width,
                this.canvas.height
            );
        }

        rect(x, y, width, height, color = "#ffffff") {
            this.ctx.fillStyle = color;
            this.ctx.fillRect(x, y, width, height);
        }

        circle(x, y, radius, color = "#ffffff") {
            this.ctx.beginPath();
            this.ctx.arc(x, y, radius, 0, Math.PI * 2);

            this.ctx.fillStyle = color;
            this.ctx.fill();
        }

        text(text, x, y, options = {}) {
            const size = options.size || 20;
            const font = options.font || "Arial";

            this.ctx.font = `${size}px ${font}`;
            this.ctx.fillStyle = options.color || "#ffffff";
            this.ctx.textAlign = options.align || "left";
            this.ctx.textBaseline = options.baseline || "alphabetic";

            this.ctx.fillText(text, x, y);
        }

        image(image, x, y, width, height) {
            if (!image) return;

            this.ctx.drawImage(
                image,
                x,
                y,
                width,
                height
            );
        }
    }

    window.AJVYRA_BrowserRenderer = AJVYRA_BrowserRenderer;
})();
