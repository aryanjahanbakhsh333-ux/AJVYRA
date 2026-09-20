function createKey(
    scene,
    x,
    y,
    id = "main-key"
) {

    const key =
        scene.add.rectangle(
            x,
            y,
            18,
            28,
            0xffffff
        );

    scene.physics.add.existing(key);

    key.body.setAllowGravity(false);

    key.keyId = id;

    return key;
}

function collectKeyObject(
    playerObject,
    keyObject
) {

    if (!keyObject.active) {
        return;
    }

    collectKey(
        keyObject.keyId
    );

    keyObject.destroy();
}
