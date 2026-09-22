class AJVYRAWebGamesReleaseAudit {
    static run() {
        const errors = [];

        try {
            AJVYRAWeb30PlayableGames.validate();

            AJVYRAWebGameplayTemplates
                .validateAll(
                    AJVYRAWeb30PlayableGames.list
                );
        } catch (error) {
            errors.push(error.message);
        }

        try {
            const smoke =
                AJVYRAWeb30GameSmokeTest.run();

            if (!smoke.passed) {
                errors.push(
                    ...smoke.errors.map(
                        item =>
                            `${item.id}: ${item.error}`
                    )
                );
            }
        } catch (error) {
            errors.push(error.message);
        }

        const required =
            [
                "AJVYRAWebPlayableGameEngine",
                "AJVYRAWebPlayableGameHost",
                "AJVYRAWeb30PlayableGames",
                "AJVYRAWebGameInputBridge",
                "AJVYRAWebGameHUD",
                "AJVYRAWebGameStateScreen"
            ];

        for (const name of required) {
            if (
                typeof window[name] !==
                "function"
            ) {
                errors.push(
                    `Missing runtime component: ${name}`
                );
            }
        }

        return {
            passed:
                errors.length === 0,

            gameCount:
                AJVYRAWeb30PlayableGames
                    .list.length,

            errors
        };
    }
}

window.AJVYRAWebGamesReleaseAudit =
    AJVYRAWebGamesReleaseAudit;
