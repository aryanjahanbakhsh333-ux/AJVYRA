function createBackgroundLayer(scene) {

    const width =
        WORLD_CONFIG.width;


    const layer =
        scene.add.container(0, 0);


    const skylineY = 520;


    for (
        let x = 0;
        x < width;
        x += 140
    ) {

        const buildingHeight =
            Phaser.Math.Between(
                80,
                220
            );


        const building =
            scene.add.rectangle(
                x,
                skylineY - buildingHeight / 2,
                Phaser.Math.Between(
                    70,
                    120
                ),
                buildingHeight,
                0x0d0d0d
            );


        layer.add(building);
    }


    layer.setDepth(-10);


    return layer;
}
