class AJVYRAWebFinalGameReleaseGate {
    static run() {
        const audit =
            AJVYRAWebGamesReleaseAudit.run();

        if (!audit.passed) {
            throw new Error(
                "AJVYRA GAME RELEASE BLOCKED: " +
                audit.errors.join(" | ")
            );
        }

        if (audit.gameCount !== 30) {
            throw new Error(
                "AJVYRA GAME RELEASE BLOCKED: " +
                "expected exactly 30 games."
            );
        }

        return {
            released: true,
            gameCount: 30,
            checkedAt:
                new Date().toISOString()
        };
    }
}

window.AJVYRAWebFinalGameReleaseGate =
    AJVYRAWebFinalGameReleaseGate;
