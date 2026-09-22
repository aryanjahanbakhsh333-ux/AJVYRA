"use strict";

class AJVYRASpriteSheet {
    constructor(options = {}) {
        this.url = options.url || "";
        this.frameWidth =
            Math.max(1, Number(options.frameWidth || 64));

        this.frameHeight =
            Math.max(1, Number(options.frameHeight || 64));

        this.columns =
            Math.max(1, Number(options.columns || 1));

        this.rows =
            Math.max(1, Number(options.rows || 1));

        this.image = null;
        this.loaded = false;
        this.failed = false;
    }

    async load() {
        if (!this.url) {
            throw new Error("Sprite sheet URL is required.");
        }

        const image = new Image();

        image.decoding = "async";

        await new Promise((resolve, reject) => {
            image.onload = resolve;

            image.onerror = () => {
                reject(
                    new Error(
                        `Failed to load sprite sheet: ${this.url}`
                    )
                );
            };

            image.src = this.url;
        });

        this.image = image;
        this.loaded = true;
        this.failed = false;

        return this;
    }

    frame(index) {
        const total =
            this.columns * this.rows;

        if (
            !Number.isInteger(index) ||
            index < 0 ||
            index >= total
        ) {
            throw new RangeError(
                `Invalid sprite frame: ${index}`
            );
        }

        const column =
            index % this.columns;

        const row =
            Math.floor(index / this.columns);

        return {
            x: column * this.frameWidth,
            y: row * this.frameHeight,
            width: this.frameWidth,
            height: this.frameHeight
        };
    }

    getFrameCount() {
        return this.columns * this.rows;
    }
}


class AJVYRAAnimatedSprite {
    constructor(sheet, options = {}) {
        if (!(sheet instanceof AJVYRASpriteSheet)) {
            throw new TypeError(
                "A valid AJVYRASpriteSheet is required."
            );
        }

        this.sheet = sheet;

        this.startFrame =
            Math.max(
                0,
                Number(options.startFrame || 0)
            );

        this.endFrame =
            Math.max(
                this.startFrame,
                Number(
                    options.endFrame ??
                    sheet.getFrameCount() - 1
                )
            );

        this.fps =
            Math.max(
                0,
                Number(options.fps || 10)
            );

        this.loop =
            options.loop !== false;

        this.currentFrame =
            this.startFrame;

        this.timer = 0;

        this.finished = false;
    }

    reset() {
        this.currentFrame = this.startFrame;
        this.timer = 0;
        this.finished = false;
    }

    update(deltaSeconds) {
        if (
            this.finished ||
            this.fps <= 0
        ) {
            return;
        }

        this.timer += Math.max(
            0,
            Number(deltaSeconds) || 0
        );

        const frameDuration =
            1 / this.fps;

        while (
            this.timer >= frameDuration
        ) {
            this.timer -= frameDuration;

            this.currentFrame += 1;

            if (
                this.currentFrame >
                this.endFrame
            ) {
                if (this.loop) {
                    this.currentFrame =
                        this.startFrame;
                } else {
                    this.currentFrame =
                        this.endFrame;

                    this.finished = true;
                    break;
                }
            }
        }
    }

    getSourceRectangle() {
        return this.sheet.frame(
            this.currentFrame
        );
    }
}


window.AJVYRASpriteSheet =
    AJVYRASpriteSheet;

window.AJVYRAAnimatedSprite =
    AJVYRAAnimatedSprite;
