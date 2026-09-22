class AJVYRAWebAdvancedCamera {
    constructor(options = {}) {
        this.x = Number(options.x) || 0;
        this.y = Number(options.y) || 0;

        this.zoom =
            Number(options.zoom) || 1;

        this.target = null;

        this.smoothing =
            Math.max(
                0,
                Math.min(
                    1,
                    Number(options.smoothing) || 0.15
                )
            );

        this.deadZoneWidth =
            Math.max(
                0,
                Number(options.deadZoneWidth) || 120
            );

        this.deadZoneHeight =
            Math.max(
                0,
                Number(options.deadZoneHeight) || 80
            );

        this.shakeX = 0;
        this.shakeY = 0;
    }

    follow(target) {
        this.target = target;
    }

    setZoom(value) {
        this.zoom =
            Math.max(
                0.1,
                Math.min(
                    10,
                    Number(value) || 1
                )
            );
    }

    update(viewWidth, viewHeight, delta = 16) {
        if (!this.target) {
            return;
        }

        const targetX =
            Number(this.target.x) || 0;

        const targetY =
            Number(this.target.y) || 0;

        const desiredX =
            targetX -
            viewWidth /
            (2 * this.zoom);

        const desiredY =
            targetY -
            viewHeight /
            (2 * this.zoom);

        const factor =
            1 -
            Math.pow(
                1 - this.smoothing,
                Math.max(0.1, delta / 16)
            );

        this.x +=
            (desiredX - this.x) *
            factor;

        this.y +=
            (desiredY - this.y) *
            factor;
    }

    applyShake(x, y) {
        this.shakeX = Number(x) || 0;
        this.shakeY = Number(y) || 0;
    }

    clearShake() {
        this.shakeX = 0;
        this.shakeY = 0;
    }

    getPosition() {
        return {
            x: this.x + this.shakeX,
            y: this.y + this.shakeY
        };
    }

    worldToScreen(x, y) {
        const position =
            this.getPosition();

        return {
            x:
                (x - position.x) *
                this.zoom,

            y:
                (y - position.y) *
                this.zoom
        };
    }

    screenToWorld(x, y) {
        const position =
            this.getPosition();

        return {
            x:
                x / this.zoom +
                position.x,

            y:
                y / this.zoom +
                position.y
        };
    }

    clampToWorld(
        worldWidth,
        worldHeight,
        viewWidth,
        viewHeight
    ) {
        const visibleWidth =
            viewWidth /
            this.zoom;

        const visibleHeight =
            viewHeight /
            this.zoom;

        const maxX =
            Math.max(
                0,
                worldWidth -
                visibleWidth
            );

        const maxY =
            Math.max(
                0,
                worldHeight -
                visibleHeight
            );

        this.x =
            Math.max(
                0,
                Math.min(
                    this.x,
                    maxX
                )
            );

        this.y =
            Math.max(
                0,
                Math.min(
                    this.y,
                    maxY
                )
            );
    }
}
