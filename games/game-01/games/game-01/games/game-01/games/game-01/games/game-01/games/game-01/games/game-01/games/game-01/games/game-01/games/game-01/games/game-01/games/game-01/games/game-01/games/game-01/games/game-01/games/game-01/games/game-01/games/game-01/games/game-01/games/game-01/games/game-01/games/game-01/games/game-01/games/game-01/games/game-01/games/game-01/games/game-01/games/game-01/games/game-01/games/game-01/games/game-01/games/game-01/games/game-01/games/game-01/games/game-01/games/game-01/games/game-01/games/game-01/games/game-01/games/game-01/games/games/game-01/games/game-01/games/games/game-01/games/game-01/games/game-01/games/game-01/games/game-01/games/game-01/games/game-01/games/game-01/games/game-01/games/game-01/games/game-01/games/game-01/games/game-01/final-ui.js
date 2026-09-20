class FinalUI {
    constructor(scene, player) {
        this.scene = scene;
        this.player = player;

        this.score = 0;
        this.orbs = 0;

        this.scoreText = scene.add.text(
            24,
            20,
            "SCORE 000000",
            {
                fontFamily: "Arial",
                fontSize: "20px",
                color: "#ffffff"
            }
        );

        this.healthText = scene.add.text(
            24,
            50,
            "HP 100",
            {
                fontFamily: "Arial",
                fontSize: "18px",
                color: "#aaaaaa"
            }
        );

        this.orbText = scene.add.text(
            24,
            78,
            "ORBS 0 / 7",
            {
                fontFamily: "Arial",
                fontSize: "18px",
                color: "#aaaaaa"
            }
        );

        this.scoreText.setScrollFactor(0);
        this.healthText.setScrollFactor(0);
        this.orbText.setScrollFactor(0);

        this.createHelp();
    }

    createHelp() {
        this.help = this.scene.add.text(
            24,
            0,
            "A / D or ← / →   •   SPACE = JUMP   •   F = ATTACK",
            {
                fontFamily: "Arial",
                fontSize: "13px",
                color: "#777777"
            }
        );

        this.help.setPosition(
            24,
            this.scene.scale.height - 30
        );

        this.help.setScrollFactor(0);
    }

    update() {
        this.scoreText.setText(
            `SCORE ${String(this.score).padStart(6, "0")}`
        );

        this.healthText.setText(
            `HP ${this.player.health}`
        );

        this.orbText.setText(
            `ORBS ${this.orbs} / 7`
        );
    }

    addScore(amount) {
        this.score += amount;
    }

    collectOrb() {
        this.orbs++;
        this.score += 250;
    }

    destroy() {
        this.scoreText.destroy();
        this.healthText.destroy();
        this.orbText.destroy();
        this.help.destroy();
    }
}
