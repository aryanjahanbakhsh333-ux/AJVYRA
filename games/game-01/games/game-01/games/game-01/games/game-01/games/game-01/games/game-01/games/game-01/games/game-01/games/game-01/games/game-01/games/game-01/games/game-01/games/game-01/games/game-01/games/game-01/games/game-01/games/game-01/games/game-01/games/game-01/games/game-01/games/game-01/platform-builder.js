function buildPlatform(
    scene,
    group,
    x,
    y,
    width,
    height,
    color = 0x252525
) {
    const platform = scene.add.rectangle(
        x,
        y,
        width,
        height,
        color
    );

    scene.physics.add.existing(
        platform,
        true
    );

    group.add(platform);

    return platform;
}


function buildPlatformsFromData(
    scene,
    group,
    platformData
) {
    platformData.forEach(platform => {

        buildPlatform(
            scene,
            group,
            platform.x,
            platform.y,
            platform.width,
            platform.height,
            platform.color
        );

    });
}
