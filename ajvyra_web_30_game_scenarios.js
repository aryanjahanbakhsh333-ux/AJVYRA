class AJVYRAWeb30GameScenarios {

    static build() {
        return {

            "shadow-runner": {
                mode: "action",
                objective: "Defeat the hunters",
                mechanic: "dash-combat",
                waves: 3
            },

            "neon-drift": {
                mode: "racing",
                objective: "Pass every checkpoint",
                mechanic: "checkpoint-racing",
                checkpoints: 7
            },

            "void-arena": {
                mode: "fighting",
                objective: "Win the arena",
                mechanic: "combo-combat",
                waves: 4
            },

            "lost-realm": {
                mode: "rpg",
                objective: "Clear the realm",
                mechanic: "rpg-combat",
                waves: 3
            },

            "night-hunt": {
                mode: "survival",
                objective: "Survive every wave",
                mechanic: "wave-survival",
                waves: 5
            },

            "cyber-strike": {
                mode: "shooter",
                objective: "Destroy hostile units",
                mechanic: "ranged-combat",
                waves: 4
            },

            "frostbound": {
                mode: "survival",
                objective: "Survive the frozen night",
                mechanic: "wave-survival",
                waves: 5
            },

            "sky-raiders": {
                mode: "action",
                objective: "Destroy the raiders",
                mechanic: "air-combat",
                waves: 3
            },

            "dungeon-zero": {
                mode: "rpg",
                objective: "Escape the dungeon",
                mechanic: "dungeon-combat",
                waves: 4
            },

            "pulse-breaker": {
                mode: "action",
                objective: "Break the pulse core",
                mechanic: "score-attack",
                waves: 3
            },

            "shadow-duel": {
                mode: "fighting",
                objective: "Defeat every rival",
                mechanic: "duel-combat",
                waves: 3
            },

            "crystal-quest": {
                mode: "adventure",
                objective: "Recover the crystals",
                mechanic: "collection",
                waves: 3
            },

            "iron-frontier": {
                mode: "strategy",
                objective: "Destroy enemy bases",
                mechanic: "base-control",
                enemyBases: 3
            },

            "ghost-signal": {
                mode: "horror",
                objective: "Survive the signal",
                mechanic: "stalker-survival",
                waves: 4
            },

            "bladefall": {
                mode: "action",
                objective: "Clear the battlefield",
                mechanic: "melee-combat",
                waves: 4
            },

            "orbit-zero": {
                mode: "shooter",
                objective: "Destroy orbital enemies",
                mechanic: "space-shooter",
                waves: 5
            },

            "wildfire": {
                mode: "survival",
                objective: "Outlast the wildfire",
                mechanic: "timed-survival",
                waves: 6
            },

            "rune-knight": {
                mode: "rpg",
                objective: "Defeat rune guardians",
                mechanic: "magic-combat",
                waves: 4
            },

            "dark-circuit": {
                mode: "racing",
                objective: "Complete the circuit",
                mechanic: "checkpoint-racing",
                checkpoints: 8
            },

            "titan-core": {
                mode: "boss",
                objective: "Defeat Titan Core",
                mechanic: "boss-battle",
                bossHp: 700
            },

            "moonfall": {
                mode: "adventure",
                objective: "Reach the moon gate",
                mechanic: "exploration",
                waves: 3
            },

            "last-fortress": {
                mode: "strategy",
                objective: "Destroy every base",
                mechanic: "base-control",
                enemyBases: 4
            },

            "phantom-chase": {
                mode: "racing",
                objective: "Escape the phantoms",
                mechanic: "chase-racing",
                checkpoints: 9
            },

            "abyss-walker": {
                mode: "horror",
                objective: "Escape the abyss",
                mechanic: "stalker-survival",
                waves: 5
            },

            "starbreaker": {
                mode: "shooter",
                objective: "Break the star fleet",
                mechanic: "space-shooter",
                waves: 6
            },

            "kingdom-ashes": {
                mode: "rpg",
                objective: "Reclaim the kingdom",
                mechanic: "rpg-combat",
                waves: 5
            },

            "zero-hour": {
                mode: "action",
                objective: "Finish before time expires",
                mechanic: "timed-action",
                waves: 4
            },

            "echo-maze": {
                mode: "puzzle",
                objective: "Solve the echo sequence",
                mechanic: "sequence-puzzle",
                puzzleLength: 7
            },

            "final-horizon": {
                mode: "adventure",
                objective: "Reach the final horizon",
                mechanic: "exploration",
                waves: 4
            },

            "ajvyra-genesis": {
                mode: "rpg",
                objective: "Complete the Genesis trial",
                mechanic: "full-rpg",
                waves: 6
            }
        };
    }

    static get(id) {
        return this.build()[id] || null;
    }

    static assertComplete() {
        const scenarios =
            Object.keys(this.build());

        if (scenarios.length !== 30) {
            throw new Error(
                `Expected 30 scenarios, found ${scenarios.length}.`
            );
        }

        return true;
    }
}

window.AJVYRAWeb30GameScenarios =
    AJVYRAWeb30GameScenarios;
