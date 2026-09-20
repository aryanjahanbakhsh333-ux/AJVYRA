function bootstrapBlackRun(scene) {

    initializeRuntime(scene);

    loadAchievements();

    loadDifficulty();

    loadPreferences();

    resetPlayerStats();

    resetLevelProgress();

    resetKeyState();

    createMainMenuUI(scene);

    createPauseUI(scene);

    createQuestUI(scene);

    createHealthBar(scene);

    createPerformanceMonitor(
        scene
    );

    setupInteractInput(scene);

    createWorldEvents(scene);

    startMission(
        "THE FIRST SIGNAL",
        "Collect the energy cores and find the exit."
    );

    createQuest(
        "first-signal",
        "THE FIRST SIGNAL",
        "Collect the energy cores.",
        7
    );
}
