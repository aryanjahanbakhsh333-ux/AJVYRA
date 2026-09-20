class FinalLevel {
    constructor(scene) {
        this.scene = scene;

        this.width = 3200;
        this.height = 900;

        this.platforms = [];
        this.orbs = [];

        this.createWorld();
    }

    createWorld() {
        const scene = this.scene;

        scene.physics.world.setBounds(
            0,
            0,
            this.width,
            this.height
        );

        scene.cameras.main.setBounds(
            0,
            0,
            this.width,
            this.height
        );

        this.createBackground();
        this.createPlatforms();
        this.createOrbs();
    }

    createBackground() {
        const scene = this.scene;

        scene.add.rectangle(
            1600,
            450,
            3200,
            900,
            0x050505
        ).setDepth(-10);

        for (let i = 0; i < 45; i++) {
            const x = Phaser.Math.Between(0, 3200);
            const y = Phaser.Math.Between(50, 600);

            scene.add.circle(
                x,
                y,
                Phaser.Math.Between(1, 3),
                0x555555
            ).setAlpha(0.45).setDepth(-5);
        }

        scene.add.rectangle(
            1600,
            620,
            3200,
            260,
            0x0d0d0d
        ).setDepth(-4);
    }

    createPlatforms() {
        const data = [
            [0, 760, 700, 40],
            [820, 680, 300, 40],
            [1230, 580, 330, 40],
            [1660, 700, 420, 40],
            [2200, 610, 280, 40],
            [2600, 510, 350, 40],
            [3000, 700, 400, 40]
        ];

        for (const [x, y, width, height] of data) {
            const platform = this.scene.add.rectangle(
                x + width / 2,
                y,
                width,
                height,
                0x202020
            );

            this.scene.physics.add.existing(
                platform,
                true
            );

            this.platforms.push(platform);
        }
    }

    createOrbs() {
        const positions = [
            [300, 690],
            [900, 610],
            [1360, 510],
            [1800, 630],
            [2320, 540],
            [2730, 440],
            [3150, 630]
        ];

        for (const [x, y] of positions) {
            const orb = this.scene.add.circle(
                x,
                y,
                9,
                0xffffff
            );

            this.scene.physics.add.existing(orb);

            orb.body.setAllowGravity(false);
            orb.body.setImmovable(true);

            this.orbs.push(orb);
        }
    }
}
