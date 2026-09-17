function createWorldDecor(scene) {

    const width =
        WORLD_CONFIG.width;

    const height =
        WORLD_CONFIG.height;


    scene.add.rectangle(
        width / 2,
        height / 2,
        width,
        height,
        WORLD_CONFIG.background
    );


    for (
        let x = 100;
        x < width;
        x += 180
    ) {

        scene.add.rectangle(
            x,
            610,
            2,
            120,
            0x111111
        );
    }


    for (
        let x = 80;
        x < width;
        x += 260
    ) {

        scene.add.circle(
            x,
            120,
            2,
            0x777777,
            0.5
        );
    }
}
