class FinalPlayer {
    constructor(scene, x, y) {
        this.scene = scene;

        this.sprite = scene.physics.add.sprite(x, y, null);

        this.sprite.setDisplaySize(34, 48);
        this.sprite.setCollideWorldBounds(true);

        this.sprite.body.setSize(28, 44);
        this.sprite.body.setOffset(3, 2);

        this.speed = 230;
        this.jumpPower = 470;

        this.maxHealth = 100;
        this.health = 100;

        this.invulnerable = false;
        this.facing = 1;

        this.createVisual();
    }

    createVisual() {
        this.bodyVisual = this.scene.add.rectangle(
            this.sprite.x,
            this.sprite.y,
            34,
            48,
            0xffffff
        );

        this.bodyVisual.setDepth(10);
    }

    update(left, right, jump) {
        if (left) {
            this.sprite.setVelocityX(-this.speed);
            this.facing = -1;
        } else if (right) {
            this.sprite.setVelocityX(this.speed);
            this.facing = 1;
        } else {
            this.sprite.setVelocityX(0);
        }

        if (
            jump &&
            this.sprite.body.blocked.down
        ) {
            this.sprite.setVelocityY(-this.jumpPower);
        }

        this.bodyVisual.setPosition(
            this.sprite.x,
            this.sprite.y
        );
    }

    damage(amount) {
        if (this.invulnerable) return;

        this.health = Math.max(
            0,
            this.health - amount
        );

        this.invulnerable = true;

        this.scene.time.delayedCall(700, () => {
            this.invulnerable = false;
        });

        return this.health <= 0;
    }

    heal(amount) {
        this.health = Math.min(
            this.maxHealth,
            this.health + amount
        );
    }

    destroy() {
        this.bodyVisual.destroy();
        this.sprite.destroy();
    }
}
