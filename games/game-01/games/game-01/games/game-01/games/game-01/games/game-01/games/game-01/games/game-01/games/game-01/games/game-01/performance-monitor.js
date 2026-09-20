let performanceText;

function createPerformanceMonitor(scene) {

    performanceText =
        scene.add.text(
            760,
            565,
            "",
            {
                fontSize: "12px",
                color: "#555555"
            }
        );

    performanceText.setScrollFactor(0);
}

function updatePerformanceMonitor(
    scene
) {

    if (!performanceText) {
        return;
    }

    const fps =
        Math.round(
            scene.game.loop.actualFps
        );

    performanceText.setText(
        "FPS: " + fps
    );
}
