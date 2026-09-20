class FinalEffects {
    constructor(scene) {
        this.scene = scene;
    }

    attack(x, y) {
        const slash = this.scene.add.rectangle(
            x,
            y,
            50,
            5,
            0xffffff
        );

        this.scene.tweens.add({
            targets: slash,
            alpha: 0,
            scaleX: 1.8,
            duration: 120,
            onComplete: () => slash.destroy()
        });
    }

    hit(x, y) {
        for (let i = 0; i < 7; i++) {
            const particle = this.scene.add.circle(
                x,
                y,
                3,
                0xffffff
            );

            const angle =
                Phaser.Math.FloatBetween(0, Math.PI * 2);

            const distance =
                Phaser.Math.Between(20, 50);

            this.scene.tweens.add({
                targets: particle,
                x: x + Math.cos(angle) * distance,
                y: y + Math.sin(angle) * distance,
                alpha: 0,
                duration: 250,
                onComplete: () => particle.destroy()
            });
        }
    }

    damage(x, y) {
        const flash = this.scene.add.rectangle(
            x,
            y,
            100,
            100,
            0xffffff
        );

        flash.setAlpha(0.12);

        this.scene.tweens.add({
            targets: flash,
            alpha: 0,
            duration: 160,
            onComplete: () => flash.destroy()
        });
    }
}
