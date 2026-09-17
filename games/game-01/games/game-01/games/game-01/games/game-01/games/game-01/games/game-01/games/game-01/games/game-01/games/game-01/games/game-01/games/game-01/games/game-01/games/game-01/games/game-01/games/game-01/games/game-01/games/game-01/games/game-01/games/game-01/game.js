let player;

let enemies;

let coins;

let platforms;

let cursors;

let restartKey;

let camera;


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

        mode:
            Phaser.Scale.FIT,

        autoCenter:
            Phaser.Scale.CENTER_BOTH
    },

    scene: {

        preload,

        create,

        update
    }
};


new Phaser.Game(config);


function preload() {

    createLoadingScreen(this);

    loadGameAssets(this);
}


function create() {

    resetGameState();

    applyGameSettings(this);

    createWorld(this);

    createPlayerSystem(this);

    createEnemySystem(this);

    createCoinSystem(this);

    createInputSystem(this);

    createCameraSystem(this);

    createInterface(this);

    createStartSystem(this);

    createPauseSystem(this);

    createAudioSystem(this);
}


function update() {

    if (
        !player ||
        GAME_STATE.gameOver ||
        !GAME_STATE.started
    ) {

        return;
    }


    const left =
        cursors.left.isDown ||
        MOBILE_INPUT.left ||
        CONTROL_STATE.left;


    const right =
        cursors.right.isDown ||
        MOBILE_INPUT.right ||
        CONTROL_STATE.right;


    if (left) {

        player.body.setVelocityX(
            -player.speed
        );

    } else if (right) {

        player.body.setVelocityX(
            player.speed
        );

    } else {

        player.body.setVelocityX(0);
    }


    const jump =
        cursors.up.isDown ||
        MOBILE_INPUT.jump ||
        CONTROL_STATE.jump;


    if (
        jump &&
        player.body.blocked.down
    ) {

        player.body.setVelocityY(
            -player.jumpPower
        );

        MOBILE_INPUT.jump = false;

        CONTROL_STATE.jump = false;
    }


    updatePlayerAnimation(
        player,
        left,
        right
    );


    enemies.children.iterate(
        (enemy) => {

            if (enemy) {

                updateEnemy(
                    enemy
                );
            }
        }
    );


    if (
        Phaser.Input.Keyboard.JustDown(
            restartKey
        )
    ) {

        this.scene.restart();

        return;
    }


    if (
        coins.countActive(true) === 0 &&
        !GAME_STATE.completed
    ) {

        completeLevel(this);
    }
}


function createWorld(scene) {

    platforms =
        scene.physics.add.staticGroup();


    createPlatform(
        scene,
        900,
        570,
        1800,
        60
    );


    createPlatform(
        scene,
        180,
        440,
        260,
        30
    );


    createPlatform(
        scene,
        620,
        390,
        260,
        30
    );


    createPlatform(
        scene,
        430,
        260,
        220,
        30
    );


    createPlatform(
        scene,
        1050,
        430,
        260,
        30
    );


    createPlatform(
        scene,
        1400,
        340,
        260,
        30
    );
}


function createPlayerSystem(scene) {

    player =
        createPlayer(
            scene,
            80,
            480
        );


    scene.physics.add.collider(
        player,
        platforms
    );


    setCheckpoint(
        80,
        480
    );
}


function createEnemySystem(scene) {

    enemies =
        scene.physics.add.group();


    const enemy1 =
        createEnemy(
            scene,
            180,
            400,
            80,
            330
        );


    const enemy2 =
        createEnemy(
            scene,
            620,
            350,
            500,
            760
        );


    const enemy3 =
        createEnemy(
            scene,
            1050,
            390,
            920,
            1180
        );


    enemies.add(enemy1);

    enemies.add(enemy2);

    enemies.add(enemy3);


    scene.physics.add.collider(
        enemies,
        platforms
    );


    scene.physics.add.overlap(
        player,
        enemies,
        (playerObject, enemyObject) => {

            handlePlayerDamage(
                scene,
                playerObject,
                enemyObject
            );
        }
    );
}


function createCoinSystem(scene) {

    coins =
        scene.physics.add.group();


    const positions = [

        [180, 390],

        [620, 340],

        [430, 210],

        [1050, 380],

        [1400, 290]
    ];


    positions.forEach(
        ([x, y]) => {

            coins.add(
                createCoin(
                    scene,
                    x,
                    y
                )
            );
        }
    );


    scene.physics.add.overlap(
        player,
        coins,
        (playerObject, coinObject) => {

            const x = coinObject.x;

            const y = coinObject.y;

            collectCoin(
                playerObject,
                coinObject
            );

            coinEffect(
                scene,
                x,
                y
            );
        }
    );
}


function createInputSystem(scene) {

    cursors =
        scene.input.keyboard
            .createCursorKeys();


    restartKey =
        scene.input.keyboard.addKey(
            Phaser.Input.Keyboard.KeyCodes.R
        );


    setupControls(scene);

    setupMobileInput();
}


function createCameraSystem(scene) {

    camera =
        setupCamera(
            scene,
            player
        );
}


function createInterface(scene) {

    createHUD(scene);

    updateHUD();
}


function createStartSystem(scene) {

    createStartMenu(scene);

    startGameTimer(scene);
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
