function createLighting(scene) {

    const width =
        WORLD_CONFIG.width;


    const height =
        WORLD_CONFIG.height;


    const light =
        scene.add.rectangle(
            width / 2,
            height / 2,
            width,
            height,
            0x000000,
            0.12
        );


    light.setDepth(20);


    return light;
}
