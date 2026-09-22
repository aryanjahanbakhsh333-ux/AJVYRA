"use strict";

class AJVYRAWebCharacter {
    constructor(options = {}) {
        this.id = String(
            options.id || `character_${Date.now()}`
        );

        this.name = String(
            options.name || this.id
        );

        this.team = String(
            options.team || "neutral"
        );

        this.body = options.body || null;

        this.speed = Math.max(
            0,
            Number(options.speed || 180)
        );

        this.runSpeed = Math.max(
            this.speed,
            Number(options.runSpeed || this.speed * 1.5)
        );

        this.jumpForce = Math.max(
            0,
            Number(options.jumpForce || 500)
        );

        this.maxHealth = Math.max(
            1,
            Number(options.maxHealth || 100)
        );

        this.health = this.maxHealth;

        this.staminaMax = Math.max(
            0,
            Number(options.staminaMax || 100)
        );

        this.stamina = this.staminaMax;

        this.alive = true;

        this.invulnerable = false;

        this.facing = 1;

        this.state = "idle";

        this.damageCooldown = 0;

        this.damageCooldownDuration = Math.max(
            0,
            Number(
                options.damageCooldownDuration || 0.15
            )
        );

        this.tags = new Set(
            Array.isArray(options.tags)
                ? options.tags
                : []
        );
    }

    update(delta) {
        if (!this.alive) {
            return;
        }

        const dt = Math.max(
            0,
            Number(delta) || 0
        );

        this.damageCooldown = Math.max(
            0,
            this.damageCooldown - dt
        );

        if (this.body) {
            if (this.body.vx > 0.01) {
                this.facing = 1;
            } else if (this.body.vx < -0.01) {
                this.facing = -1;
            }
        }

        this.stamina = Math.min(
            this.staminaMax,
            this.stamina + dt * 8
        );
    }

    move(direction, running = false) {
        if (!this.alive || !this.body) {
            return;
        }

        const normalized =
            Math.max(
                -1,
                Math.min(
                    1,
                    Number(direction) || 0
                )
            );

        const speed =
            running &&
            this.stamina > 0
                ? this.runSpeed
                : this.speed;

        this.body.vx =
            normalized * speed;

        if (running && normalized !== 0) {
            this.stamina = Math.max(
                0,
                this.stamina - 0.8
            );
        }

        if (normalized !== 0) {
            this.facing =
                normalized > 0
                    ? 1
                    : -1;

            this.state = running
                ? "running"
                : "walking";
        } else if (this.body.grounded) {
            this.body.vx = 0;
            this.state = "idle";
        }
    }

    jump() {
        if (
            !this.alive ||
            !this.body ||
            !this.body.grounded
        ) {
            return false;
        }

        this.body.vy =
            -this.jumpForce;

        this.body.grounded = false;

        this.state = "jumping";

        return true;
    }

    takeDamage(amount, source = null) {
        if (
            !this.alive ||
            this.invulnerable ||
            this.damageCooldown > 0
        ) {
            return false;
        }

        const damage = Math.max(
            0,
            Number(amount) || 0
        );

        this.health = Math.max(
            0,
            this.health - damage
        );

        this.damageCooldown =
            this.damageCooldownDuration;

        if (this.health <= 0) {
            this.die(source);
        } else {
            this.state = "hurt";
        }

        return true;
    }

    heal(amount) {
        if (!this.alive) {
            return 0;
        }

        const before = this.health;

        this.health = Math.min(
            this.maxHealth,
            this.health +
                Math.max(
                    0,
                    Number(amount) || 0
                )
        );

        return this.health - before;
    }

    die(source = null) {
        this.health = 0;
        this.alive = false;
        this.state = "dead";

        return {
            characterId: this.id,
            sourceId: source?.id || null
        };
    }

    getHealthRatio() {
        return this.health / this.maxHealth;
    }

    distanceTo(other) {
        if (!other?.body || !this.body) {
            return Infinity;
        }

        return Math.hypot(
            this.body.centerX -
                other.body.centerX,
            this.body.centerY -
                other.body.centerY
        );
    }

    isAlive() {
        return this.alive;
    }
}

window.AJVYRAWebCharacter =
    AJVYRAWebCharacter;
