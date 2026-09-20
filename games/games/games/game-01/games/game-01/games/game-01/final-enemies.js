class FinalEnemies {
    constructor(scene, player) {
        this.scene = scene;
        this.player = player;
        this.list = [];

        this.createEnemies();
    }

    createEnemies() {
        const positions = [
            [620, 710],
            [1080, 630],
            [1510, 530],
            [1980, 650],
            [2440, 560],
            [2890, 460]
        ];

        positions.forEach(([x, y], index) => {
            this.createEnemy(x, y, index);
        });
    }

    createEnemy(x, y, index) {
        const enemy = this.scene.add.rectangle(
            x,
            y,
            34,
            42,
            0x777777
        );

        this.scene.physics.add.existing(enemy);

        enemy.body.setCollideWorldBounds(true);

        enemy.health = 30;
        enemy.speed = 45 + index * 4;
        enemy.direction = index % 2 === 0 ? 1 : -1;

        this.list.push(enemy);
    }

    update() {
        for (const enemy of this.list) {
            if (!enemy.active) continue;

            const distance =
                this.player.sprite.x - enemy.x;

            if (Math.abs(distance) < 360) {
                enemy.body.setVelocityX(
                    Math.sign(distance) * enemy.speed
                );
            } else {
                enemy.body.setVelocityX(
                    enemy.direction * enemy.speed
                );
            }

            if (
                enemy.body.blocked.left ||
                enemy.body.blocked.right
            ) {
                enemy.direction *= -1;
            }
        }
    }

    damage(enemy, amount) {
        if (!enemy || !enemy.active) return false;

        enemy.health -= amount;

        if (enemy.health <= 0) {
            enemy.destroy();
            return true;
        }

        return false;
    }
}
