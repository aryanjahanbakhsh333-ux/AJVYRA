(function (global) {
    "use strict";

    const ids = [
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

    class AJVYRAWeb30GameReleaseManifest {
        static all() {
            return ids.slice();
        }

        static count() {
            return ids.length;
        }

        static has(id) {
            return ids.includes(
                String(id)
            );
        }

        static buildContract(id) {
            return {
                id: String(id),
                required: [
                    "story",
                    "objective",
                    "controls",
                    "mechanics",
                    "renderer",
                    "runtime",
                    "mobile",
                    "landscape",
                    "win-condition",
                    "lose-condition"
                ]
            };
        }
    }

    global.AJVYRAWeb30GameReleaseManifest =
        AJVYRAWeb30GameReleaseManifest;

})(window);
