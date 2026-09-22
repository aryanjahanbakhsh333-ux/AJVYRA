(function (global) {
    "use strict";

    class AJVYRAWeb30GameReleaseAudit {
        constructor() {
            this.results = [];
        }

        auditGame(id) {
            const gameId =
                String(id);

            const errors = [];

            const profiles =
                global.AJVYRAWeb30UniqueGameProfiles;

            if (!profiles) {
                errors.push(
                    "Unique profile registry missing"
                );
            }

            const profile =
                profiles?.get(gameId);

            if (!profile) {
                errors.push(
                    "Unique game profile missing"
                );
            }

            if (profile) {
                if (!profile.story) {
                    errors.push(
                        "Story missing"
                    );
                }

                if (!profile.objective) {
                    errors.push(
                        "Objective missing"
                    );
                }

                if (
                    !profile.controls ||
                    Object.keys(
                        profile.controls
                    ).length < 4
                ) {
                    errors.push(
                        "Unique control set missing"
                    );
                }

                if (
                    !Array.isArray(
                        profile.mechanics
                    ) ||
                    profile.mechanics.length < 2
                ) {
                    errors.push(
                        "Unique mechanics missing"
                    );
                }

                if (!profile.victory) {
                    errors.push(
                        "Victory condition missing"
                    );
                }

                if (!profile.defeat) {
                    errors.push(
                        "Defeat condition missing"
                    );
                }
            }

            const result = {
                id: gameId,
                playable: errors.length === 0,
                errors
            };

            this.results.push(result);

            return result;
        }

        auditAll() {
            this.results = [];

            const manifest =
                global.AJVYRAWeb30GameReleaseManifest;

            if (!manifest) {
                throw new Error(
                    "Release manifest missing."
                );
            }

            for (
                const id of manifest.all()
            ) {
                this.auditGame(id);
            }

            return this.summary();
        }

        summary() {
            const total =
                this.results.length;

            const playable =
                this.results.filter(
                    (item) => item.playable
                ).length;

            const failed =
                this.results.filter(
                    (item) => !item.playable
                );

            return {
                total,
                playable,
                failed:
                    failed.length,
                releaseReady:
                    total === 30 &&
                    playable === 30,
                failures: failed
            };
        }

        assertReleaseReady() {
            const result =
                this.summary();

            if (
                !result.releaseReady
            ) {
                const details =
                    result.failures
                        .map(
                            (item) =>
                                `${item.id}: ${item.errors.join(
                                    ", "
                                )}`
                        )
                        .join("\n");

                throw new Error(
                    "AJVYRA GAME RELEASE BLOCKED.\n" +
                    details
                );
            }

            return true;
        }
    }

    global.AJVYRAWeb30GameReleaseAudit =
        AJVYRAWeb30GameReleaseAudit;

})(window);
