let player;
let cursors;
let platforms;
let stars;
let score = 0;
let scoreText;
let gameOver = false;

const config = {
    type: Phaser.AUTO,

    width: 900,
    height: 600,

    parent: "game-container",

    backgroundColor: "#090909",

    physics: {
        default: "arcade",

        arcade: {
            gravity: {
                y: 900
            },

            debug: false
        }
    },

    scale: {
        mode: Phaser.Scale.FIT,
        autoCenter: Phaser.Scale.CENTER_BOTH
    },

    scene: {
        preload,
        create,
        update
    }
};

const game = new Phaser.Game(config);

function preload() {
}

function create() {

    this.add.rectangle(
        450,
        300,
        900,
        600,
        0x090909
    );

    this.add.text(
        30,
        25,
        "AJVYRA // BLACK RUN",
        {
            fontSize: "22px",
            color: "#ffffff",
            fontStyle: "bold"
        }
    );

    scoreText = this.add.text(
        700,
        30,
        "SCORE: 0",
        {
            fontSize: "18px",
            color: "#aaaaaa"
        }
    );

    platforms = this.physics.add.staticGroup();

    createPlatform(this, 450, 570, 900, 60);
    createPlatform(this, 200, 430, 250, 30);
    createPlatform(this, 600, 350, 250, 30);
    createPlatform(this, 400, 220, 220, 30);

    player = this.physics.add.rectangle(
        100,
        450,
        35,
        50,
        0xffffff
    );

    this.physics.add.existing(player);

    player.body.setCollideWorldBounds(true);

    this.physics.add.collider(
        player,
        platforms
    );

    stars = this.physics.add.group();

    createStar(this, 200, 380);
    createStar(this, 600, 300);
    createStar(this, 400, 170);

    this.physics.add.overlap(
        player,
        stars,
        collectStar,
        null,
        this
    );

    cursors = this.input.keyboard.createCursorKeys();

    setupMobileControls(this);
}

function update() {

    if (gameOver) {
        return;
    }

    if (cursors.left.isDown) {

        player.body.setVelocityX(-260);

    } else if (cursors.right.isDown) {

        player.body.setVelocityX(260);

    } else {

        player.body.setVelocityX(0);
    }

    if (
        cursors.up.isDown &&
        player.body.blocked.down
    ) {

        player.body.setVelocityY(-500);
    }
}

function createPlatform(scene, x, y, width, height) {

    const platform = scene.add.rectangle(
        x,
        y,
        width,
        height,
        0x252525
    );

    scene.physics.add.existing(
        platform,
        true
    );

    platforms.add(platform);
}

function createStar(scene, x, y) {

    const star = scene.add.circle(
        x,
        y,
        12,
        0xffffff
    );

    scene.physics.add.existing(star);

    stars.add(star);
}

function collectStar(playerObject, star) {

    star.destroy();

    score += 10;

    scoreText.setText(
        "SCORE: " + score
    );

    if (stars.countActive(true) === 0) {

        endGame(
            this,
            "LEVEL COMPLETE"
        );
    }
}

function endGame(scene, message) {

    gameOver = true;

    player.body.setVelocity(0);

    scene.add.rectangle(
        450,
        300,
        900,
        600,
        0x000000,
        0.75
    );

    scene.add.text(
        450,
        270,
        message,
        {
            fontSize: "42px",
            color: "#ffffff",
            fontStyle: "bold"
        }
    ).setOrigin(0.5);

    scene.add.text(
        450,
        330,
        "SCORE: " + score,
        {
            fontSize: "22px",
            color: "#aaaaaa"
        }
    ).setOrigin(0.5);
}

function setupMobileControls(scene) {

    const left = document.getElementById("leftBtn");
    const right = document.getElementById("rightBtn");
    const jump = document.getElementById("jumpBtn");

    left.addEventListener(
        "touchstart",
        () => {
            player.body.setVelocityX(-260);
        }
    );

    left.addEventListener(
        "touchend",
        () => {
            player.body.setVelocityX(0);
        }
    );

    right.addEventListener(
        "touchstart",
        () => {
            player.body.setVelocityX(260);
        }
    );

    right.addEventListener(
        "touchend",
        () => {
            player.body.setVelocityX(0);
        }
    );

    jump.addEventListener(
        "touchstart",
        () => {

            if (player.body.blocked.down) {
                player.body.setVelocityY(-500);
            }

        }
    );
}
