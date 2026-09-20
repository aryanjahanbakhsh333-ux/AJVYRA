function createMovingPlatform(
    scene,
    group,
    x,
    y,
    width,
    height,
    distance,
    duration
) {

    const platform =
        buildPlatform(
            scene,
            group,
            x,
            y,
            width,
            height
        );

    platform.originalX = x;

    platform.originalY = y;

    scene.tweens.add({

        targets: platform,

        x: x + distance,

        duration,

        yoyo: true,

        repeat: -1,

        ease: "Sine.easeInOut"
    });

    return platform;
}
