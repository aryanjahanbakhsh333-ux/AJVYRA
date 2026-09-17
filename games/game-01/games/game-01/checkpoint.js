let checkpoint = {
    x: 80,
    y: 480
};

function setCheckpoint(x, y) {

    checkpoint.x = x;
    checkpoint.y = y;
}

function respawnPlayer(player) {

    player.setPosition(
        checkpoint.x,
        checkpoint.y
    );

    player.body.setVelocity(
        0,
        0
    );
}
