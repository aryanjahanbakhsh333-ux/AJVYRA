const AJVYRA_RUNTIME = {

    initialized: false,

    started: false,

    lastUpdate: 0,

    frameCount: 0,

    fps: 0
};


function initializeRuntime(scene) {

    AJVYRA_RUNTIME.initialized =
        true;

    AJVYRA_RUNTIME.started =
        false;

    AJVYRA_RUNTIME.lastUpdate =
        performance.now();

    AJVYRA_RUNTIME.frameCount =
        0;

    window.AJVYRA_SCENE =
        scene;
}


function updateRuntime(scene) {

    if (
        !AJVYRA_RUNTIME.initialized
    ) {
        initializeRuntime(scene);
    }

    AJVYRA_RUNTIME.frameCount++;

    const now =
        performance.now();

    const elapsed =
        now -
        AJVYRA_RUNTIME.lastUpdate;

    if (elapsed >= 1000) {

        AJVYRA_RUNTIME.fps =
            AJVYRA_RUNTIME.frameCount;

        AJVYRA_RUNTIME.frameCount = 0;

        AJVYRA_RUNTIME.lastUpdate =
            now;
    }

    updateGameSession();
}


function startRuntime() {

    AJVYRA_RUNTIME.started =
        true;

    startGameSession();
}
