"use strict";

class AJVYRAWebGameRenderer {
    constructor(canvas, options = {}) {
        if (!(canvas instanceof HTMLCanvasElement)) {
            throw new TypeError("A valid HTMLCanvasElement is required.");
        }

        this.canvas = canvas;

        this.ctx = canvas.getContext("2d", {
            alpha: false,
            desynchronized: true
        });

        if (!this.ctx) {
            throw new Error("Canvas 2D context is not available.");
        }

        this.width = Math.max(
            320,
            Number(options.width || canvas.width || 1280)
        );

        this.height = Math.max(
            240,
            Number(options.height || canvas.height || 720)
        );

        this.pixelRatio = Math.min(
            2,
            Math.max(
                1,
                window.devicePixelRatio || 1
            )
        );

        this.background = options.background || "#050505";

        this.resize(this.width, this.height);
    }

    resize(width, height) {
        this.width = Math.max(320, Number(width) || 1280);
        this.height = Math.max(240, Number(height) || 720);

        this.canvas.width =
            Math.round(this.width * this.pixelRatio);

        this.canvas.height =
            Math.round(this.height * this.pixelRatio);

        this.canvas.style.width =
            `${this.width}px`;

        this.canvas.style.height =
            `${this.height}px`;

        this.ctx.setTransform(
            this.pixelRatio,
            0,
            0,
            this.pixelRatio,
            0,
            0
        );
    }

    clear(color = this.background) {
        this.ctx.save();

        this.ctx.setTransform(
            this.pixelRatio,
            0,
            0,
            this.pixelRatio,
            0,
            0
        );

        this.ctx.fillStyle = color;
        this.ctx.fillRect(
            0,
            0,
            this.width,
            this.height
        );

        this.ctx.restore();
    }

    beginFrame() {
        this.ctx.save();

        this.ctx.setTransform(
            this.pixelRatio,
            0,
            0,
            this.pixelRatio,
            0,
            0
        );

        this.ctx.clearRect(
            0,
            0,
            this.width,
            this.height
        );
    }

    endFrame() {
        this.ctx.restore();
    }

    rectangle(
        x,
        y,
        width,
        height,
        color = "#ffffff"
    ) {
        this.ctx.fillStyle = color;
        this.ctx.fillRect(
            x,
            y,
            width,
            height
        );
    }

    circle(
        x,
        y,
        radius,
        color = "#ffffff"
    ) {
        this.ctx.beginPath();

        this.ctx.arc(
            x,
            y,
            Math.max(0, radius),
            0,
            Math.PI * 2
        );

        this.ctx.fillStyle = color;
        this.ctx.fill();
    }

    line(
        x1,
        y1,
        x2,
        y2,
        color = "#ffffff",
        width = 1
    ) {
        this.ctx.beginPath();

        this.ctx.moveTo(x1, y1);
        this.ctx.lineTo(x2, y2);

        this.ctx.strokeStyle = color;
        this.ctx.lineWidth = Math.max(1, width);

        this.ctx.stroke();
    }

    text(
        value,
        x,
        y,
        options = {}
    ) {
        this.ctx.save();

        this.ctx.font =
            options.font || "20px sans-serif";

        this.ctx.fillStyle =
            options.color || "#ffffff";

        this.ctx.textAlign =
            options.align || "left";

        this.ctx.textBaseline =
            options.baseline || "alphabetic";

        if (options.shadow) {
            this.ctx.shadowColor =
                options.shadow.color || "#000000";

            this.ctx.shadowBlur =
                Number(options.shadow.blur || 0);
        }

        this.ctx.fillText(
            String(value),
            x,
            y
        );

        this.ctx.restore();
    }

    image(
        image,
        x,
        y,
        width = null,
        height = null
    ) {
        if (!image) {
            return;
        }

        if (
            width === null ||
            height === null
        ) {
            this.ctx.drawImage(
                image,
                x,
                y
            );

            return;
        }

        this.ctx.drawImage(
            image,
            x,
            y,
            width,
            height
        );
    }

    sprite(
        image,
        source,
        destination
    ) {
        if (!image) {
            return;
        }

        this.ctx.drawImage(
            image,

            source.x,
            source.y,
            source.width,
            source.height,

            destination.x,
            destination.y,
            destination.width,
            destination.height
        );
    }

    save() {
        this.ctx.save();
    }

    restore() {
        this.ctx.restore();
    }

    translate(x, y) {
        this.ctx.translate(x, y);
    }

    rotate(angle) {
        this.ctx.rotate(angle);
    }

    scale(x, y) {
        this.ctx.scale(x, y);
    }

    setAlpha(alpha) {
        this.ctx.globalAlpha =
            Math.max(
                0,
                Math.min(1, Number(alpha))
            );
    }

    getContext() {
        return this.ctx;
    }
}

window.AJVYRAWebGameRenderer =
    AJVYRAWebGameRenderer;
