"use strict";

class AJVYRAEffectManager {
    constructor() {
        this.particles = [];

        this.flashAlpha = 0;
        this.flashColor = "#ffffff";

        this.shakeTime = 0;
        this.shakeStrength = 0;

        this.maxParticles = 2000;
    }

    spawnParticle(options = {}) {
        if (
            this.particles.length >=
            this.maxParticles
        ) {
            return;
        }

        this.particles.push({
            x: Number(options.x || 0),
            y: Number(options.y || 0),

            vx: Number(options.vx || 0),
            vy: Number(options.vy || 0),

            life: Math.max(
                0.01,
                Number(options.life || 1)
            ),

            maxLife: Math.max(
                0.01,
                Number(options.life || 1)
            ),

            size: Math.max(
                0.5,
                Number(options.size || 4)
            ),

            gravity: Number(
                options.gravity || 0
            ),

            color:
                options.color ||
                "#ffffff",
        });
    }

    burst(
        x,
        y,
        count = 20,
        options = {}
    ) {
        const amount = Math.min(
            Math.max(0, Number(count) || 0),
            500
        );

        for (let i = 0; i < amount; i += 1) {
            const angle =
                Math.random() *
                Math.PI *
                2;

            const speed =
                Math.random() *
                Number(
                    options.speed || 200
                );

            this.spawnParticle({
                x,
                y,

                vx:
                    Math.cos(angle) *
                    speed,

                vy:
                    Math.sin(angle) *
                    speed,

                life:
                    options.life ||
                    0.7,

                size:
                    options.size ||
                    3,

                gravity:
                    options.gravity ||
                    100,

                color:
                    options.color ||
                    "#ffffff",
            });
        }
    }

    flash(
        color = "#ffffff",
        alpha = 0.6
    ) {
        this.flashColor = color;

        this.flashAlpha =
            Math.max(
                0,
                Math.min(
                    1,
                    Number(alpha) || 0
                )
            );
    }

    shake(
        strength = 10,
        duration = 0.25
    ) {
        this.shakeStrength =
            Math.max(
                this.shakeStrength,
                Number(strength) || 0
            );

        this.shakeTime =
            Math.max(
                this.shakeTime,
                Number(duration) || 0
            );
    }

    update(deltaSeconds) {
        const delta =
            Math.max(
                0,
                Number(deltaSeconds) || 0
            );

        for (
            let i = this.particles.length - 1;
            i >= 0;
            i -= 1
        ) {
            const particle =
                this.particles[i];

            particle.life -= delta;

            if (particle.life <= 0) {
                this.particles.splice(i, 1);
                continue;
            }

            particle.vy +=
                particle.gravity * delta;

            particle.x +=
                particle.vx * delta;

            particle.y +=
                particle.vy * delta;
        }

        this.flashAlpha = Math.max(
            0,
            this.flashAlpha -
                delta * 4
        );

        this.shakeTime = Math.max(
            0,
            this.shakeTime - delta
        );

        if (this.shakeTime <= 0) {
            this.shakeStrength = 0;
        }
    }

    render(renderer) {
        for (const particle of this.particles) {
            const alpha =
                particle.life /
                particle.maxLife;

            renderer.setAlpha(alpha);

            renderer.circle(
                particle.x,
                particle.y,
                particle.size,
                particle.color
            );
        }

        renderer.setAlpha(1);

        if (this.flashAlpha > 0) {
            renderer.setAlpha(
                this.flashAlpha
            );

            renderer.rectangle(
                0,
                0,
                renderer.width,
                renderer.height,
                this.flashColor
            );

            renderer.setAlpha(1);
        }
    }

    getCameraShake() {
        if (
            this.shakeTime <= 0 ||
            this.shakeStrength <= 0
        ) {
            return {
                x: 0,
                y: 0
            };
        }

        const intensity =
            this.shakeStrength *
            Math.min(
                1,
                this.shakeTime * 8
            );

        return {
            x:
                (
                    Math.random() * 2 - 1
                ) * intensity,

            y:
                (
                    Math.random() * 2 - 1
                ) * intensity
        };
    }

    clear() {
        this.particles.length = 0;
        this.flashAlpha = 0;
        this.shakeTime = 0;
        this.shakeStrength = 0;
    }
}


window.AJVYRAEffectManager =
    AJVYRAEffectManager;
