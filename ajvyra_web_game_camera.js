"use strict";

class AJVYRAWebGameCamera {
    constructor(options = {}) {
        this.x = Number(options.x || 0);
        this.y = Number(options.y || 0);

        this.targetX = this.x;
        this.targetY = this.y;

        this.zoom = Math.max(
            0.1,
            Number(options.zoom || 1)
        );

        this.minZoom = Math.max(
            0.1,
            Number(options.minZoom || 0.5)
        );

        this.maxZoom = Math.max(
            this.minZoom,
            Number(options.maxZoom || 3)
        );

        this.followSpeed =
            Math.max(
                0,
                Number(options.followSpeed || 8)
            );

        this.smoothing =
            options.smoothing !== false;
    }

    setPosition(x, y) {
        this.x = Number(x) || 0;
        this.y = Number(y) || 0;

        this.targetX = this.x;
        this.targetY = this.y;
    }

    lookAt(x, y) {
        this.targetX = Number(x) || 0;
        this.targetY = Number(y) || 0;
    }

    follow(target, offsetX = 0, offsetY = 0) {
        if (!target) {
            return;
        }

        this.lookAt(
            Number(target.x || 0) + offsetX,
            Number(target.y || 0) + offsetY
        );
    }

    update(deltaSeconds) {
        const delta =
            Math.max(
                0,
                Number(deltaSeconds) || 0
            );

        if (!this.smoothing) {
            this.x = this.targetX;
            this.y = this.targetY;
            return;
        }

        const factor =
            1 -
            Math.exp(
                -this.followSpeed * delta
            );

        this.x +=
            (this.targetX - this.x) * factor;

        this.y +=
            (this.targetY - this.y) * factor;
    }

    setZoom(value) {
        this.zoom = Math.max(
            this.minZoom,
            Math.min(
                this.maxZoom,
                Number(value) || 1
            )
        );
    }

    zoomBy(amount) {
        this.setZoom(
            this.zoom + Number(amount || 0)
        );
    }

    begin(renderer) {
        renderer.save();

        const centerX =
            renderer.width / 2;

        const centerY =
            renderer.height / 2;

        renderer.translate(
            centerX,
            centerY
        );

        renderer.scale(
            this.zoom,
            this.zoom
        );

        renderer.translate(
            -this.x,
            -this.y
        );
    }

    end(renderer) {
        renderer.restore();
    }

    screenToWorld(
        screenX,
        screenY,
        renderer
    ) {
        return {
            x:
                this.x +
                (
                    screenX -
                    renderer.width / 2
                ) / this.zoom,

            y:
                this.y +
                (
                    screenY -
                    renderer.height / 2
                ) / this.zoom
        };
    }
}


window.AJVYRAWebGameCamera =
    AJVYRAWebGameCamera;
