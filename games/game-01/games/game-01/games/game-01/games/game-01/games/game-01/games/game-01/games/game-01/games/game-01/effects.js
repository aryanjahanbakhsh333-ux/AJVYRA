function playerHitEffect(scene, player) {

    scene.cameras.main.shake(
        180,
        0.008
    );

    scene.tweens.add({
        targets: player,

        alpha: 0.2,

        duration: 100,

        yoyo: true,

        repeat: 4
    });
}

function coinEffect(scene, x, y) {

    const text = scene.add.text(
        x,
        y,
        "+25",
        {
            fontSize: "18px",
            color: "#ffffff",
            fontStyle: "bold"
        }
    ).setOrigin(0.5);

    scene.tweens.add({

        targets: text,

        y: y - 40,

        alpha: 0,

        duration: 500,

        onComplete: () => {
            text.destroy();
        }
    });
}
