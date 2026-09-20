class FinalCombat {
    constructor(scene, player, enemies) {
        this.scene = scene;
        this.player = player;
        this.enemies = enemies;

        this.cooldown = false;
        this.damage = 20;
        this.range = 75;
    }

    attack() {
        if (this.cooldown) return;

        this.cooldown = true;

        this.scene.time.delayedCall(280, () => {
            this.cooldown = false;
        });

        const playerX = this.player.sprite.x;
        const playerY = this.player.sprite.y;

        for (const enemy of this.enemies.list) {
            if (!enemy.active) continue;

            const distance = Phaser.Math.Distance.Between(
                playerX,
                playerY,
                enemy.x,
                enemy.y
            );

            const direction =
                Math.sign(enemy.x - playerX);

            if (
                distance <= this.range &&
                direction === this.player.facing
            ) {
                const defeated =
                    this.enemies.damage(enemy, this.damage);

                if (defeated) {
                    this.scene.addScore(100);
                }

                this.scene.finalEffects.hit(
                    enemy.x,
                    enemy.y
                );
            }
        }

        this.scene.finalEffects.attack(
            playerX + this.player.facing * 35,
            playerY
        );
    }

    checkEnemyCollision() {
        for (const enemy of this.enemies.list) {
            if (!enemy.active) continue;

            const distance = Phaser.Math.Distance.Between(
                this.player.sprite.x,
                this.player.sprite.y,
                enemy.x,
                enemy.y
            );

            if (distance < 35) {
                const dead = this.player.damage(10);

                this.scene.finalEffects.damage(
                    this.player.sprite.x,
                    this.player.sprite.y
                );

                if (dead) {
                    this.scene.endGame();
                }
            }
        }
    }
}
