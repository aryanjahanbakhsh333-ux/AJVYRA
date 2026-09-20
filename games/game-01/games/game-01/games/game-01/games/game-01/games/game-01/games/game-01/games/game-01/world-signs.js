function createWorldSign(
    scene,
    x,
    y,
    text
) {

    const sign =
        scene.add.text(
            x,
            y,
            text,
            {
                fontSize: "14px",
                color: "#aaaaaa",
                backgroundColor: "#111111",
                padding: {
                    left: 10,
                    right: 10,
                    top: 6,
                    bottom: 6
                }
            }
        );

    makeInteractable(
        sign,
        () => {

            showWorldMessage(
                scene,
                text
            );
        }
    );

    return sign;
}


function showWorldMessage(
    scene,
    message
) {

    const text =
        scene.add.text(
            450,
            520,
            message,
            {
                fontSize: "18px",
                color: "#ffffff",
                backgroundColor: "#111111",
                padding: {
                    left: 18,
                    right: 18,
                    top: 10,
                    bottom: 10
                }
            }
        ).setOrigin(0.5);

    scene.tweens.add({

        targets: text,

        alpha: 0,

        duration: 2200,

        delay: 700,

        onComplete: () => {
            text.destroy();
        }
    });
}
