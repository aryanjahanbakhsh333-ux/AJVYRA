function setupAttackInput(scene) {

    const attackKey =
        scene.input.keyboard.addKey(
            Phaser.Input.Keyboard.KeyCodes.SPACE
        );

    attackKey.on(
        "down",
        () => {
            attackPlayer(scene);
        }
    );
}
