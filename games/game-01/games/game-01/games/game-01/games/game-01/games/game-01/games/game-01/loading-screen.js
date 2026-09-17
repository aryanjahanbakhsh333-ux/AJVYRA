function createLoadingScreen(scene) {

    const background =
        scene.add.rectangle(
            450,
            300,
            900,
            600,
            0x050505
        );

    const title =
        scene.add.text(
            450,
            250,
            "AJVYRA",
            {
                fontSize: "48px",
                fontStyle: "bold",
                color: "#ffffff"
            }
        ).setOrigin(0.5);

    const loading =
        scene.add.text(
            450,
            320,
            "LOADING...",
            {
                fontSize: "16px",
                color: "#777777"
            }
        ).setOrigin(0.5);

    return {
        background,
        title,
        loading
    };
}
