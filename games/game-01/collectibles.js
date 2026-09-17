function createCoin(scene, x, y) {

    const coin = scene.add.circle(
        x,
        y,
        10,
        0xffffff
    );

    scene.physics.add.existing(coin);

    coin.body.setAllowGravity(false);

    return coin;
}

function collectCoin(player, coin) {

    if (!coin.active) {
        return;
    }

    coin.destroy();

    GAME_STATE.score += 25;

    if (window.updateHUD) {
        window.updateHUD();
    }
}
