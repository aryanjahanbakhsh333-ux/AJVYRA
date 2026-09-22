"use strict";

class AJVYRAWebPhysicsBody {
    constructor(options = {}) {
        this.x = Number(options.x || 0);
        this.y = Number(options.y || 0);

        this.width = Math.max(
            1,
            Number(options.width || 32)
        );

        this.height = Math.max(
            1,
            Number(options.height || 32)
        );

        this.vx = Number(options.vx || 0);
        this.vy = Number(options.vy || 0);

        this.ax = Number(options.ax || 0);
        this.ay = Number(options.ay || 0);

        this.mass = Math.max(
            0.0001,
            Number(options.mass || 1)
        );

        this.gravityScale =
            Number(options.gravityScale ?? 1);

        this.friction =
            Math.max(
                0,
                Math.min(
                    1,
                    Number(options.friction ?? 0.8)
                )
            );

        this.restitution =
            Math.max(
                0,
                Math.min(
                    1,
                    Number(options.restitution ?? 0)
                )
            );

        this.dynamic =
            options.dynamic !== false;

        this.kinematic =
            options.kinematic === true;

        this.grounded = false;

        this.enabled =
            options.enabled !== false;

        this.maxSpeed =
            Math.max(
                0,
                Number(options.maxSpeed || 0)
            );
    }

    get left() {
        return this.x;
    }

    get right() {
        return this.x + this.width;
    }

    get top() {
        return this.y;
    }

    get bottom() {
        return this.y + this.height;
    }

    get centerX() {
        return this.x + this.width / 2;
    }

    get centerY() {
        return this.y + this.height / 2;
    }

    setPosition(x, y) {
        this.x = Number(x) || 0;
        this.y = Number(y) || 0;
    }

    setVelocity(vx, vy) {
        this.vx = Number(vx) || 0;
        this.vy = Number(vy) || 0;
    }

    applyForce(fx, fy) {
        if (!this.dynamic || !this.enabled) {
            return;
        }

        this.ax +=
            Number(fx || 0) / this.mass;

        this.ay +=
            Number(fy || 0) / this.mass;
    }

    applyImpulse(ix, iy) {
        if (!this.dynamic || !this.enabled) {
            return;
        }

        this.vx +=
            Number(ix || 0) / this.mass;

        this.vy +=
            Number(iy || 0) / this.mass;
    }

    integrate(delta, gravityX, gravityY) {
        if (
            !this.dynamic ||
            !this.enabled
        ) {
            return;
        }

        const dt = Math.min(
            Math.max(
                Number(delta) || 0,
                0
            ),
            0.1
        );

        this.vx +=
            (
                this.ax +
                gravityX * this.gravityScale
            ) * dt;

        this.vy +=
            (
                this.ay +
                gravityY * this.gravityScale
            ) * dt;

        if (this.maxSpeed > 0) {
            const speed = Math.hypot(
                this.vx,
                this.vy
            );

            if (speed > this.maxSpeed) {
                const scale =
                    this.maxSpeed / speed;

                this.vx *= scale;
                this.vy *= scale;
            }
        }

        this.x += this.vx * dt;
        this.y += this.vy * dt;

        this.ax = 0;
        this.ay = 0;
    }
}


class AJVYRAWebPhysicsWorld {
    constructor(options = {}) {
        this.gravityX =
            Number(options.gravityX || 0);

        this.gravityY =
            Number(options.gravityY || 1200);

        this.bodies = new Set();

        this.iterations =
            Math.max(
                1,
                Number(options.iterations || 4)
            );
    }

    addBody(body) {
        if (
            !(body instanceof AJVYRAWebPhysicsBody)
        ) {
            throw new TypeError(
                "PhysicsWorld requires AJVYRAWebPhysicsBody."
            );
        }

        this.bodies.add(body);
        return body;
    }

    removeBody(body) {
        this.bodies.delete(body);
    }

    step(delta) {
        for (const body of this.bodies) {
            body.integrate(
                delta,
                this.gravityX,
                this.gravityY
            );
        }
    }

    clear() {
        this.bodies.clear();
    }
}


window.AJVYRAWebPhysicsBody =
    AJVYRAWebPhysicsBody;

window.AJVYRAWebPhysicsWorld =
    AJVYRAWebPhysicsWorld;
