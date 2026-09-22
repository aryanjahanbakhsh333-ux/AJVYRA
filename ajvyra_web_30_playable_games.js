class AJVYRAWeb30PlayableGames {
    static get list() {
        const raw = [
            ["shadow-runner", "Shadow Runner", "action", "action", 18],
            ["neon-drift", "Neon Drift", "racing", "racing", 6],
            ["void-arena", "Void Arena", "combat", "fighting", 12],
            ["lost-realm", "Lost Realm", "rpg", "rpg", 10],
            ["night-hunt", "Night Hunt", "survival", "survival", 30],
            ["cyber-strike", "Cyber Strike", "shooter", "shooter", 15],
            ["frostbound", "Frostbound", "survival", "survival", 25],
            ["sky-raiders", "Sky Raiders", "action", "action", 14],
            ["dungeon-zero", "Dungeon Zero", "rpg", "rpg", 12],
            ["pulse-breaker", "Pulse Breaker", "arcade", "action", 20],
            ["shadow-duel", "Shadow Duel", "fighting", "fighting", 10],
            ["crystal-quest", "Crystal Quest", "adventure", "adventure", 9],
            ["iron-frontier", "Iron Frontier", "strategy", "strategy", 8],
            ["ghost-signal", "Ghost Signal", "horror", "horror", 8],
            ["bladefall", "Bladefall", "action", "action", 16],
            ["orbit-zero", "Orbit Zero", "shooter", "shooter", 18],
            ["wildfire", "Wildfire", "survival", "survival", 35],
            ["rune-knight", "Rune Knight", "rpg", "rpg", 14],
            ["dark-circuit", "Dark Circuit", "racing", "racing", 7],
            ["titan-core", "Titan Core", "boss", "boss", 6],
            ["moonfall", "Moonfall", "adventure", "adventure", 11],
            ["last-fortress", "Last Fortress", "strategy", "strategy", 10],
            ["phantom-chase", "Phantom Chase", "racing", "racing", 8],
            ["abyss-walker", "Abyss Walker", "horror", "horror", 9],
            ["starbreaker", "Starbreaker", "shooter", "shooter", 20],
            ["kingdom-ashes", "Kingdom Ashes", "rpg", "rpg", 15],
            ["zero-hour", "Zero Hour", "action", "action", 20],
            ["echo-maze", "Echo Maze", "puzzle", "puzzle", 7],
            ["final-horizon", "Final Horizon", "adventure", "adventure", 12],
            ["ajvyra-genesis", "AJVYRA: Genesis", "rpg", "rpg", 18]
        ];

        return raw.map(item => {
            const [
                id,
                title,
                genre,
                mode,
                objectiveTotal
            ] = item;

            const isBoss = mode === "boss";
            const isPuzzle = mode === "puzzle";
            const isRacing = mode === "racing";
            const isSurvival = mode === "survival";

            return {
                id,
                title,
                genre,
                mode,

                objectiveTotal,

                enemies: isPuzzle
                    ? 0
                    : isBoss
                        ? 6
                        : 4,

                enemyHp: isBoss
                    ? 180
                    : 30,

                enemySpeed: isRacing
                    ? 0.02
                    : 0.07,

                pickups: isSurvival
                    ? 5
                    : 3,

                targets: isPuzzle
                    ? objectiveTotal
                    : 0,

                obstacles: isRacing
                    ? 8
                    : 3,

                playerSpeed: isRacing
                    ? 0.62
                    : 0.45,

                damage: mode === "shooter"
                    ? 28
                    : 20,

                killScore: isBoss
                    ? 250
                    : 100,

                timeLimit: isSurvival
                    ? objectiveTotal
                    : null,

                lapTime: isRacing
                    ? 3.5
                    : null,

                jump:
                    mode === "action" ||
                    mode === "adventure"
                        ? 0.7
                        : null,

                specialCost: 20,
                specialDamage: isBoss
                    ? 80
                    : 50,

                specialRange: isBoss
                    ? 0.38
                    : 0.28,

                lives: mode === "horror"
                    ? 2
                    : 3,

                background: "#080808"
            };
        });
    }

    static byId(id) {
        return this.list.find(
            game => game.id === id
        ) || null;
    }

    static validate() {
        const games = this.list;

        if (games.length !== 30) {
            throw new Error(
                "AJVYRA requires exactly 30 games."
            );
        }

        const ids =
            new Set(games.map(game => game.id));

        if (ids.size !== 30) {
            throw new Error(
                "Duplicate game IDs detected."
            );
        }

        return {
            valid: true,
            count: games.length
        };
    }
}

window.AJVYRAWeb30PlayableGames =
    AJVYRAWeb30PlayableGames;
