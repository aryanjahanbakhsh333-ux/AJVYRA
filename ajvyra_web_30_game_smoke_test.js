class AJVYRAWeb30GameSmokeTest {
    static run() {
        const errors = [];

        const fakeInput = {
            update() {},
            enable() {},
            disable() {},

            getMovement() {
                return {
                    x: 0,
                    y: 0
                };
            },

            wasPressed() {
                return false;
            }
        };

        for (
            const game
            of AJVYRAWeb30PlayableGames.list
        ) {
            try {
                const engine =
                    new AJVYRAWebPlayableGameEngine({
                        input: fakeInput
                    });

                engine.load(game);

                engine.state.status =
                    "playing";

                engine.update(0.016);

                if (
                    !engine.state ||
                    !engine.state.player
                ) {
                    throw new Error(
                        "Runtime state missing."
                    );
                }
            } catch (error) {
                errors.push({
                    id: game.id,
                    error: error.message
                });
            }
        }

        return {
            passed: errors.length === 0,
            tested: 30,
            errors
        };
    }
}

window.AJVYRAWeb30GameSmokeTest =
    AJVYRAWeb30GameSmokeTest;
