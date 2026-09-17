const GAME_SETTINGS = {

    width: 900,

    height: 600,

    playerSpeed: 280,

    jumpPower: 500,

    startingLives: 3,

    startingTime: 60,

    soundVolume: 0.5
};

function applyGameSettings(scene) {

    scene.sound.volume =
        GAME_SETTINGS.soundVolume;
}
