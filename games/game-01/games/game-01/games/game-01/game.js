let player;
let enemies;
let coins;
let platforms;

let cursors;
let restartKey;

const config = {

    type: Phaser.AUTO,

    width: 900,
    height: 600,

    parent: "game-container",

    backgroundColor: "#080808",

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

        autoCenter:
            Phaser.Scale.CENTER_BOTH
    },

    scene: {

        create,
        update
    }
};

new Phaser.Game(config);

function create() {

    resetGameState();

    this.add.text(
        450,
        125,
        "BLACK RUN",
        {
            fontSize: "38px",
            color: "#ffffff",
            fontStyle: "bold"
        }
    ).setOrigin(0.5);

    createHUD(this);

    platforms =
        this.physics.add.staticGroup();

    createPlatform(
        this,
        450,
        570,
        900,
        60
    );

    createPlatform(
        this,
        180,
        440,
        260,
        30
    );

    createPlatform(
        this,
        620,
        390,
        260,
        30
    );

    createPlatform(
        this,
        430,
        260,
        220,
        30
    );

    player =
        createPlayer(
            this,
            80,
            480
        );

    this.physics.add.collider(
        player,
        platforms
    );

    enemies =
        this.physics.add.group();

    const enemy1 =
        createEnemy(
            this,
            180,
            400,
            80,
            330
        );

    const enemy2 =
        createEnemy(
            this,
            620,
            350,
            500,
            760
        );

    enemies.add(enemy1);
    enemies.add(enemy2);

    this.physics.add.collider(
        enemies,
        platforms
    );

    this.physics.add.overlap(
        player,
        enemies,
        () => {

            damagePlayer(
                this,
                player
            );

        }
    );

    coins =
        this.physics.add.group();

    coins.add(
        createCoin(
            this,
            180,
            390
        )
    );

    coins.add(
        createCoin(
            this,
            620,
            340
        )
    );

    coins.add(
        createCoin(
            this,
            430,
            210
        )
    );

    this.physics.add.overlap(
        player,
        coins,
        collectCoin,
        null,
        this
    );

    cursors =
        this.input.keyboard.createCursorKeys();

    restartKey =
        this.input.keyboard.addKey(
            Phaser.Input.Keyboard.KeyCodes.R
        );

    setupMobileInput();

    startGameTimer(this);
}

function update() {

    if (
        !player ||
        GAME_STATE.gameOver
    ) {
        return;
    }

    if (
        cursors.left.isDown ||
        MOBILE_INPUT.left
    ) {

        player.body.setVelocityX(
            -player.speed
        );

    } else if (
        cursors.right.isDown ||
        MOBILE_INPUT.right
    ) {

        player.body.setVelocityX(
            player.speed
        );

    } else {

        player.body.setVelocityX(0);
    }

    if (
        (
            cursors.up.isDown ||
            MOBILE_INPUT.jump
        ) &&
        player.body.blocked.down
    ) {

        player.body.setVelocityY(
            -player.jumpPower
        );

        MOBILE_INPUT.jump = false;
    }

    enemies.children.iterate(
        enemy => {

            if (enemy) {
                updateEnemy(enemy);
            }
        }
    );

    if (
        Phaser.Input.Keyboard.JustDown(
            restartKey
        )
    ) {

        this.scene.restart();
    }

    if (
        coins.countActive(true) === 0 &&
        !GAME_STATE.completed
    ) {

        GAME_STATE.completed = true;

        showGameOver(
            this,
            "LEVEL COMPLETE",
            "Score: " + GAME_STATE.score
        );
    }
}

function createPlatform(
    scene,
    x,
    y,
    width,
    height
) {

    const platform =
        scene.add.rectangle(
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
