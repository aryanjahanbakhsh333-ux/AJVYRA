/* AJVYRA — Final 30 Game Content Manifest
 * New file.
 */

class AJVYRA30GameContentManifestFinal {

    static REQUIRED = [
        "shadow-runner",
        "neon-drift",
        "void-arena",
        "lost-realm",
        "night-hunt",
        "cyber-strike",
        "frostbound",
        "sky-raiders",
        "dungeon-zero",
        "pulse-breaker",
        "shadow-duel",
        "crystal-quest",
        "iron-frontier",
        "ghost-signal",
        "bladefall",
        "orbit-zero",
        "wildfire",
        "rune-knight",
        "dark-circuit",
        "titan-core",
        "moonfall",
        "last-fortress",
        "phantom-chase",
        "abyss-walker",
        "starbreaker",
        "kingdom-ashes",
        "zero-hour",
        "echo-maze",
        "final-horizon",
        "ajvyra-genesis"
    ];

    static validate() {
        const registry =
            globalThis.AJVYRA30GameExperienceRegistry;

        const story =
            globalThis.AJVYRA30GameStoryDatabase;

        const missingRegistry = [];
        const missingStory = [];

        for (const gameId of this.REQUIRED) {
            if (!registry?.has?.(gameId)) {
                missingRegistry.push(gameId);
            }

            if (!story?.has?.(gameId)) {
                missingStory.push(gameId);
            }
        }

        const valid =
            missingRegistry.length === 0 &&
            missingStory.length === 0;

        return {
            valid,
            total: this.REQUIRED.length,
            registryReady:
                missingRegistry.length === 0,
            storyReady:
                missingStory.length === 0,
            missingRegistry,
            missingStory
        };
    }

    static assertReady() {
        const result = this.validate();

        if (!result.valid) {
            throw new Error(
                [
                    "AJVYRA 30-game content manifest failed.",
                    `Missing registry: ${result.missingRegistry.join(", ") || "none"}`,
                    `Missing story: ${result.missingStory.join(", ") || "none"}`
                ].join("\n")
            );
        }

        return result;
    }

    static list() {
        return [...this.REQUIRED];
    }

    static count() {
        return this.REQUIRED.length;
    }
}

globalThis.AJVYRA30GameContentManifestFinal =
    AJVYRA30GameContentManifestFinal;
