function setupCamera(
    scene,
    player
) {

    const camera =
        scene.cameras.main;


    camera.setBounds(
        0,
        0,
        1800,
        600
    );


    camera.startFollow(
        player,
        true,
        0.08,
        0.08
    );


    camera.setDeadzone(
        250,
        150
    );


    return camera;
}
