const GAME_FLOW = {

    phase: "menu",

    phases: [
        "menu",
        "playing",
        "boss",
        "complete",
        "game-over"
    ]
};


function setGamePhase(
    phase
) {

    if (
        !GAME_FLOW.phases.includes(
            phase
        )
    ) {
        return false;
    }

    GAME_FLOW.phase =
        phase;

    return true;
}


function beginGameplay() {

    setGamePhase(
        "playing"
    );

    GAME_STATE.started =
        true;

    startRuntime();
}


function beginBossPhase(
    scene
) {

    setGamePhase(
        "boss"
    );

    notifyPlayer(
        scene,
        "THE SHADOW HAS ARRIVED"
    );
}


function finishGameplay() {

    setGamePhase(
        "complete"
    );
}


function failGameplay() {

    setGamePhase(
        "game-over"
    );
}
