const WAVE_STATE = {

    current: 0,

    total: 3,

    activeEnemies: 0,

    completed: false
};


function startNextWave(
    scene,
    group
) {

    if (
        WAVE_STATE.current >=
        WAVE_STATE.total
    ) {

        WAVE_STATE.completed = true;

        notifyPlayer(
            scene,
            "ALL WAVES COMPLETE"
        );

        return;
    }

    WAVE_STATE.current++;

    const count =
        WAVE_STATE.current + 1;

    for (
        let i = 0;
        i < count;
        i++
    ) {

        const enemy =
            createEnemy(
                scene,
                1000 + i * 70,
                400,
                900,
                1300
            );

        group.add(enemy);

        WAVE_STATE.activeEnemies++;
    }

    notifyPlayer(
        scene,
        "WAVE " +
        WAVE_STATE.current
    );
}


function updateWaveState(
    scene,
    group
) {

    const active =
        group.countActive(true);

    WAVE_STATE.activeEnemies =
        active;

    if (
        active === 0 &&
        !WAVE_STATE.completed
    ) {

        scene.time.delayedCall(
            1200,
            () => {

                startNextWave(
                    scene,
                    group
                );
            }
        );
    }
}
