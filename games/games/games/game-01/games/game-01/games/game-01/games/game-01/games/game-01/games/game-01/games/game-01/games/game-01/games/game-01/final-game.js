class BlackRunFinal extends Phaser.Scene {

    constructor() {
        super("BlackRunFinal");
    }

    create() {

        this.finalLevel = new FinalLevel(this);

        this.player = new FinalPlayer(
            this,
            120,
            650
        );

        this.enemies = new FinalEnemies(
            this,
            this.player
        );

        this.finalEffects =
            new FinalEffects(this);

        this.finalUI =
            new FinalUI(this, this.player);

        this.finalSave =
            new FinalSave();

        this.finalAudio =
            new FinalAudio(this);

        this.finalCombat =
            new FinalCombat(
                this,
                this.player,
                this.enemies
            );

        this.cursors =
            this.input.keyboard.createCursorKeys();

        this.keys =
            this.input.keyboard.addKeys(
                "A,D,F"
            );

        this.setupCollisions();

        this.createExit();

        this.cameras.main.startFollow(
            this.player.sprite,
            true,
            0.08,
            0.08
        );

        this.started = false;

        this.createStartScreen();
    }

    setupCollisions() {

        for (const platform of this.finalLevel.platforms) {
            this.physics.add.collider(
                this.player.sprite,
                platform
            );

            for (const enemy of this.enemies.list) {
                this.physics.add.collider(
                    enemy,
                    platform
                );
            }
        }

        for (const orb of this.finalLevel.orbs) {
            this.physics.add.overlap(
                this.player.sprite,
                orb,
                () => {
                    if (!orb.active) return;

                    orb.destroy();

                    this.finalUI.collectOrb();
                    this.finalAudio.beep(700, 0.1);
                }
            );
        }
    }

    createExit() {

        this.exit = this.add.rectangle(
            3160,
            640,
            45,
            120,
            0x333333
        );

        this.exit.setStrokeStyle(
            2,
            0xffffff
        );

        this.physics.add.existing(
            this.exit,
            true
        );

        this.physics.add.overlap(
            this.player.sprite,
            this.exit,
            () => {

                if (
                    this.finalUI.orbs >= 7
                ) {
                    this.completeGame();
                }
            }
        );
    }

    createStartScreen() {

        this.startOverlay =
            this.add.rectangle(
                0,
                0,
                this.scale.width,
                this.scale.height,
                0x000000
            );

        this.startOverlay.setOrigin(0);
        this.startOverlay.setScrollFactor(0);
        this.startOverlay.setDepth(100);

        this.startTitle =
            this.add.text(
                this.scale.width / 2,
                this.scale.height / 2 - 60,
                "BLACK RUN",
                {
                    fontFamily: "Arial",
                    fontSize: "54px",
                    fontStyle: "bold",
                    color: "#ffffff"
                }
            )
            .setOrigin(0.5)
            .setScrollFactor(0)
            .setDepth(101);

        this.startText =
            this.add.text(
                this.scale.width / 2,
                this.scale.height / 2 + 20,
                "TAP / CLICK / ENTER TO START",
                {
                    fontFamily: "Arial",
                    fontSize: "16px",
                    color: "#999999"
                }
            )
            .setOrigin(0.5)
            .setScrollFactor(0)
            .setDepth(101);

        this.input.keyboard.once(
            "keydown-ENTER",
            () => this.startGame()
        );

        this.input.once(
            "pointerdown",
            () => this.startGame()
        );
    }

    startGame() {

        if (this.started) return;

        this.started = true;

        this.startOverlay.destroy();
        this.startTitle.destroy();
        this.startText.destroy();

        this.finalAudio.init();

        this.finalAudio.beep(300, 0.15);
    }

    update() {

        if (!this.started) return;

        const left =
            this.cursors.left.isDown ||
            this.keys.A.isDown;

        const right =
            this.cursors.right.isDown ||
            this.keys.D.isDown;

        const jump =
            Phaser.Input.Keyboard.JustDown(
                this.cursors.up
            ) ||
            Phaser.Input.Keyboard.JustDown(
                this.cursors.space
            );

        this.player.update(
            left,
            right,
            jump
        );

        this.enemies.update();

        this.finalCombat.checkEnemyCollision();

        this.finalUI.update();

        if (
            Phaser.Input.Keyboard.JustDown(
                this.keys.F
            )
        ) {
            this.finalCombat.attack();
        }

        if (
            this.player.sprite.y >
            this.finalLevel.height
        ) {
            this.endGame();
        }
    }

    addScore(amount) {
        this.finalUI.addScore(amount);
        this.finalAudio.beep(520, 0.06);
    }

    completeGame() {

        this.started = false;

        this.finalSave.save({
            score: this.finalUI.score,
            orbs: this.finalUI.orbs
        });

        const overlay =
            this.add.rectangle(
                0,
                0,
                this.scale.width,
                this.scale.height,
                0x000000
            );

        overlay.setOrigin(0);
        overlay.setScrollFactor(0);
        overlay.setDepth(200);

        this.add.text(
            this.scale.width / 2,
            this.scale.height / 2 - 40,
            "RUN COMPLETE",
            {
                fontFamily: "Arial",
                fontSize: "48px",
                fontStyle: "bold",
                color: "#ffffff"
            }
        )
        .setOrigin(0.5)
        .setScrollFactor(0)
        .setDepth(201);

        this.add.text(
            this.scale.width / 2,
            this.scale.height / 2 + 25,
            `SCORE ${this.finalUI.score}`,
            {
                fontFamily: "Arial",
                fontSize: "20px",
                color: "#aaaaaa"
            }
        )
        .setOrigin(0.5)
        .setScrollFactor(0)
        .setDepth(201);
    }

    endGame() {

        this.started = false;

        this.finalSave.save({
            score: this.finalUI.score,
            orbs: this.finalUI.orbs
        });

        const overlay =
            this.add.rectangle(
                0,
                0,
                this.scale.width,
                this.scale.height,
                0x000000
            );

        overlay.setOrigin(0);
        overlay.setScrollFactor(0);
        overlay.setDepth(200);

        this.add.text(
            this.scale.width / 2,
            this.scale.height / 2 - 30,
            "RUN OVER",
            {
                fontFamily: "Arial",
                fontSize: "48px",
                fontStyle: "bold",
                color: "#ffffff"
            }
        )
        .setOrigin(0.5)
        .setScrollFactor(0)
        .setDepth(201);

        this.add.text(
            this.scale.width / 2,
            this.scale.height / 2 + 35,
            `SCORE ${this.finalUI.score}`,
            {
                fontFamily: "Arial",
                fontSize: "20px",
                color: "#888888"
            }
        )
        .setOrigin(0.5)
        .setScrollFactor(0)
        .setDepth(201);
    }
}


const BLACK_RUN_CONFIG = {
    type: Phaser.AUTO,

    width: 1000,
    height: 650,

    backgroundColor: "#050505",

    physics: {
        default: "arcade",
        arcade: {
            gravity: {
                y: 1000
            },
            debug: false
        }
    },

    scale: {
        mode: Phaser.Scale.FIT,
        autoCenter: Phaser.Scale.CENTER_BOTH
    },

    parent: "black-run-game",

    scene: BlackRunFinal
};


new Phaser.Game(BLACK_RUN_CONFIG);
