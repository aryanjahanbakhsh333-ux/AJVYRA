class AJVYRAWebGameVFXSystem {
    constructor() {
        this.effects = [];
        this.shakes = [];
        this.flashes = [];
    }

    addEffect(effect = {}) {
        const value = {
            id:
                effect.id ||
                `effect_${Date.now()}_${Math.random()}`,

            type:
                effect.type ||
                "generic",

            x:
                Number(effect.x) || 0,

            y:
                Number(effect.y) || 0,

            duration:
                Math.max(
                    1,
                    Number(effect.duration) || 300
                ),

            elapsed: 0,

            strength:
                Number(effect.strength) || 1,

            metadata:
                effect.metadata || {}
        };

        this.effects.push(value);

        return value;
    }

    explosion(x, y, options = {}) {
        return this.addEffect({
            type: "explosion",
            x,
            y,
            duration:
                options.duration || 500,
            strength:
                options.strength || 1,
            metadata: {
                radius:
                    options.radius || 80,
                particles:
                    options.particles || 20
            }
        });
    }

    hit(x, y, options = {}) {
        return this.addEffect({
            type: "hit",
            x,
            y,
            duration:
                options.duration || 180,
            strength:
                options.strength || 1
        });
    }

    flash(options = {}) {
        const flash = {
            duration:
                Math.max(
                    1,
                    Number(options.duration) || 120
                ),

            elapsed: 0,

            strength:
                Math.max(
                    0,
                    Number(options.strength) || 1
                )
        };

        this.flashes.push(
            flash
        );

        return flash;
    }

    shake(options = {}) {
        const shake = {
            duration:
                Math.max(
                    1,
                    Number(options.duration) || 250
                ),

            elapsed: 0,

            strength:
                Math.max(
                    0,
                    Number(options.strength) || 5
                )
        };

        this.shakes.push(
            shake
        );

        return shake;
    }

    update(delta) {
        const dt =
            Math.max(
                0,
                Number(delta) || 0
            );

        this.effects =
            this.effects.filter(effect => {
                effect.elapsed += dt;

                return (
                    effect.elapsed <
                    effect.duration
                );
            });

        this.flashes =
            this.flashes.filter(effect => {
                effect.elapsed += dt;

                return (
                    effect.elapsed <
                    effect.duration
                );
            });

        this.shakes =
            this.shakes.filter(effect => {
                effect.elapsed += dt;

                return (
                    effect.elapsed <
                    effect.duration
                );
            });
    }

    getShakeOffset() {
        let x = 0;
        let y = 0;

        for (const shake of this.shakes) {
            const progress =
                Math.min(
                    1,
                    shake.elapsed /
                    shake.duration
                );

            const strength =
                shake.strength *
                (1 - progress);

            x +=
                (Math.random() * 2 - 1) *
                strength;

            y +=
                (Math.random() * 2 - 1) *
                strength;
        }

        return { x, y };
    }

    getFlashStrength() {
        let strength = 0;

        for (const flash of this.flashes) {
            const progress =
                Math.min(
                    1,
                    flash.elapsed /
                    flash.duration
                );

            strength =
                Math.max(
                    strength,
                    flash.strength *
                    (1 - progress)
                );
        }

        return strength;
    }

    getActiveEffects() {
        return [
            ...this.effects
        ];
    }

    clear() {
        this.effects.length = 0;
        this.shakes.length = 0;
        this.flashes.length = 0;
    }
}
