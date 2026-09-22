(function (global) {
    "use strict";

    const GAMES = {
        "shadow-runner": {
            title: "Shadow Runner",
            genre: ["action"],
            objective: "Reach the final gate while surviving the shadow pursuit.",
            stages: ["escape", "district", "pursuit", "gate", "finale"],
            player: "runner",
            enemy: "shadow",
            win: "reach_gate",
            controls: ["move", "attack", "dash", "ability", "interact"]
        },

        "neon-drift": {
            title: "Neon Drift",
            genre: ["racing"],
            objective: "Win the illegal night race through the neon city.",
            stages: ["grid", "tunnel", "rooftop", "expressway", "finish"],
            player: "driver",
            enemy: "rival_driver",
            win: "finish_first",
            controls: ["accelerate", "brake", "steer", "boost", "drift"]
        },

        "void-arena": {
            title: "Void Arena",
            genre: ["fighting"],
            objective: "Defeat the arena champion through three rounds.",
            stages: ["qualifier", "duel", "champion", "final"],
            player: "fighter",
            enemy: "void_champion",
            win: "win_two_rounds",
            controls: ["attack", "heavyAttack", "block", "parry", "dodge"]
        },

        "lost-realm": {
            title: "Lost Realm",
            genre: ["rpg", "adventure"],
            objective: "Discover what happened to the vanished kingdom.",
            stages: ["village", "forest", "ruins", "castle", "truth"],
            player: "wanderer",
            enemy: "fallen_guard",
            win: "discover_truth",
            controls: ["move", "attack", "interact", "ability", "inventory"]
        },

        "night-hunt": {
            title: "Night Hunt",
            genre: ["survival", "horror"],
            objective: "Survive eight nights and uncover the signal.",
            stages: ["camp", "woods", "station", "deep_night", "dawn"],
            player: "survivor",
            enemy: "hunter",
            win: "survive_nights",
            controls: ["move", "attack", "scavenge", "medicine", "interact"]
        },

        "cyber-strike": {
            title: "Cyber Strike",
            genre: ["shooter"],
            objective: "Break into the corporate core and destroy the central server.",
            stages: ["street", "security", "labs", "core", "escape"],
            player: "operative",
            enemy: "security_unit",
            win: "destroy_core",
            controls: ["move", "shoot", "reload", "ability", "interact"]
        },

        "frostbound": {
            title: "Frostbound",
            genre: ["survival", "adventure"],
            objective: "Cross the frozen city before the storm consumes it.",
            stages: ["shelter", "outskirts", "frozen_city", "tower", "storm"],
            player: "survivor",
            enemy: "frost_creature",
            win: "reach_tower",
            controls: ["move", "attack", "scavenge", "medicine", "interact"]
        },

        "sky-raiders": {
            title: "Sky Raiders",
            genre: ["action", "shooter"],
            objective: "Destroy the enemy fleet above the clouds.",
            stages: ["takeoff", "clouds", "fleet", "carrier", "final_battle"],
            player: "raider",
            enemy: "air_fleet",
            win: "destroy_carrier",
            controls: ["move", "shoot", "dash", "ability", "interact"]
        },

        "dungeon-zero": {
            title: "Dungeon Zero",
            genre: ["rpg", "dungeon"],
            objective: "Reach the impossible dungeon's final chamber.",
            stages: ["entrance", "crypt", "depths", "guardian", "zero"],
            player: "delver",
            enemy: "dungeon_guardian",
            win: "reach_zero",
            controls: ["move", "attack", "ability", "interact", "inventory"]
        },

        "pulse-breaker": {
            title: "Pulse Breaker",
            genre: ["arcade", "action"],
            objective: "Destroy the pulse network before the city shuts down.",
            stages: ["street", "node_one", "node_two", "core", "collapse"],
            player: "breaker",
            enemy: "pulse_unit",
            win: "break_core",
            controls: ["move", "attack", "dash", "ability", "interact"]
        },

        "shadow-duel": {
            title: "Shadow Duel",
            genre: ["fighting"],
            objective: "Survive a duel against the warrior who knows your past.",
            stages: ["arrival", "first_round", "second_round", "final_round"],
            player: "duelist",
            enemy: "shadow_duelist",
            win: "win_duel",
            controls: ["attack", "heavyAttack", "block", "parry", "dodge"]
        },

        "crystal-quest": {
            title: "Crystal Quest",
            genre: ["adventure", "puzzle"],
            objective: "Find the five crystals and unlock the ancient archive.",
            stages: ["village", "cave", "temple", "archive", "awakening"],
            player: "seeker",
            enemy: "crystal_guardian",
            win: "collect_crystals",
            controls: ["move", "interact", "attack", "puzzle", "inventory"]
        },

        "iron-frontier": {
            title: "Iron Frontier",
            genre: ["strategy"],
            objective: "Build and defend a frontier base against enemy waves.",
            stages: ["landing", "base", "expansion", "siege", "counterattack"],
            player: "commander",
            enemy: "frontier_army",
            win: "hold_frontier",
            controls: ["select", "build", "capture", "deploy", "upgrade"]
        },

        "ghost-signal": {
            title: "Ghost Signal",
            genre: ["horror"],
            objective: "Trace a dead radio signal without becoming its next victim.",
            stages: ["station", "basement", "forest", "tower", "signal"],
            player: "investigator",
            enemy: "signal_entity",
            win: "decode_signal",
            controls: ["move", "interact", "hide", "flashlight", "escape"]
        },

        "bladefall": {
            title: "Bladefall",
            genre: ["action", "fighting"],
            objective: "Climb the fallen fortress and defeat its master.",
            stages: ["gate", "courtyard", "tower", "sanctum", "master"],
            player: "warrior",
            enemy: "blade_master",
            win: "defeat_master",
            controls: ["move", "attack", "heavyAttack", "dodge", "ability"]
        },

        "orbit-zero": {
            title: "Orbit Zero",
            genre: ["shooter", "space"],
            objective: "Follow an impossible signal beyond the moon.",
            stages: ["orbit", "moon", "debris", "signal", "unknown"],
            player: "pilot",
            enemy: "drone",
            win: "reach_signal",
            controls: ["move", "shoot", "boost", "missile", "interact"]
        },

        "wildfire": {
            title: "Wildfire",
            genre: ["survival"],
            objective: "Rescue survivors before the fire reaches the final district.",
            stages: ["suburb", "river", "hospital", "evacuation", "escape"],
            player: "rescuer",
            enemy: "fire",
            win: "rescue_survivors",
            controls: ["move", "interact", "rescue", "scavenge", "dash"]
        },

        "rune-knight": {
            title: "Rune Knight",
            genre: ["rpg", "action"],
            objective: "Choose whether the final rune should be awakened or sealed.",
            stages: ["village", "ruins", "temple", "rune_chamber", "decision"],
            player: "rune_knight",
            enemy: "rune_guardian",
            win: "resolve_rune",
            controls: ["move", "attack", "ability", "interact", "inventory"]
        },

        "dark-circuit": {
            title: "Dark Circuit",
            genre: ["racing"],
            objective: "Win the underground race with no second chance.",
            stages: ["start", "industrial", "tunnel", "nightway", "finish"],
            player: "driver",
            enemy: "rival",
            win: "finish_first",
            controls: ["accelerate", "brake", "steer", "boost", "drift"]
        },

        "titan-core": {
            title: "Titan Core",
            genre: ["boss"],
            objective: "Defeat the ancient machine before it awakens completely.",
            stages: ["awakening", "phase_two", "phase_three", "enrage", "core"],
            player: "fighter",
            enemy: "titan",
            win: "destroy_titan",
            controls: ["move", "attack", "dodge", "ability", "bossDamage"]
        },

        "moonfall": {
            title: "Moonfall",
            genre: ["adventure"],
            objective: "Discover what is pulling the moon toward Earth.",
            stages: ["observatory", "coast", "facility", "orbit", "truth"],
            player: "explorer",
            enemy: "anomaly",
            win: "discover_cause",
            controls: ["move", "interact", "attack", "scan", "ability"]
        },

        "last-fortress": {
            title: "Last Fortress",
            genre: ["strategy", "survival"],
            objective: "Hold the final fortress through the enemy siege.",
            stages: ["preparation", "wall", "siege", "breach", "last_stand"],
            player: "commander",
            enemy: "siege_army",
            win: "hold_fortress",
            controls: ["select", "build", "capture", "deploy", "upgrade"]
        },

        "phantom-chase": {
            title: "Phantom Chase",
            genre: ["racing", "action"],
            objective: "Catch a vehicle that doesn't appear on any camera.",
            stages: ["city", "highway", "tunnel", "rooftops", "phantom"],
            player: "driver",
            enemy: "phantom_driver",
            win: "catch_phantom",
            controls: ["accelerate", "brake", "steer", "boost", "drift"]
        },

        "abyss-walker": {
            title: "Abyss Walker",
            genre: ["horror", "adventure"],
            objective: "Descend into the abyss and discover what is waiting below.",
            stages: ["entrance", "cavern", "depth", "abyss", "awakening"],
            player: "walker",
            enemy: "abyss_entity",
            win: "reach_abyss",
            controls: ["move", "interact", "hide", "flashlight", "escape"]
        },

        "starbreaker": {
            title: "Starbreaker",
            genre: ["shooter", "space"],
            objective: "Break through the enemy fleet and destroy its flagship.",
            stages: ["orbit", "fleet", "escort", "flagship", "breakthrough"],
            player: "pilot",
            enemy: "star_fleet",
            win: "destroy_flagship",
            controls: ["move", "shoot", "boost", "missile", "ability"]
        },

        "kingdom-ashes": {
            title: "Kingdom Ashes",
            genre: ["rpg", "strategy"],
            objective: "Rebuild a destroyed kingdom or choose revenge.",
            stages: ["ashes", "village", "army", "capital", "throne"],
            player: "heir",
            enemy: "invaders",
            win: "restore_kingdom",
            controls: ["move", "attack", "interact", "build", "ability"]
        },

        "zero-hour": {
            title: "Zero Hour",
            genre: ["action", "survival"],
            objective: "Stop the countdown before the city reaches zero.",
            stages: ["awakening", "street", "facility", "countdown", "zero"],
            player: "operative",
            enemy: "strike_force",
            win: "stop_countdown",
            controls: ["move", "attack", "dash", "ability", "interact"]
        },

        "echo-maze": {
            title: "Echo Maze",
            genre: ["puzzle"],
            objective: "Escape a maze where every mistake creates another path.",
            stages: ["echo", "mirror", "memory", "loop", "exit"],
            player: "wanderer",
            enemy: "echo",
            win: "solve_maze",
            controls: ["move", "puzzle", "interact", "observe"]
        },

        "final-horizon": {
            title: "Final Horizon",
            genre: ["adventure"],
            objective: "Reach the place beyond the horizon that should not exist.",
            stages: ["road", "valley", "mountain", "horizon", "beyond"],
            player: "traveler",
            enemy: "guardian",
            win: "reach_horizon",
            controls: ["move", "interact", "attack", "ability", "observe"]
        },

        "ajvyra-genesis": {
            title: "AJVYRA: Genesis",
            genre: ["rpg", "adventure", "action"],
            objective: "Create the fate of a world that has no predetermined ending.",
            stages: ["awakening", "origin", "conflict", "choice", "genesis"],
            player: "creator",
            enemy: "void",
            win: "create_ending",
            controls: ["move", "attack", "ability", "interact", "choice"]
        }
    };

    class AJVYRA30GameExperienceRegistry {
        static get(id) {
            return GAMES[id] || null;
        }

        static has(id) {
            return Object.prototype.hasOwnProperty.call(
                GAMES,
                id
            );
        }

        static list() {
            return Object.keys(GAMES);
        }

        static count() {
            return Object.keys(GAMES).length;
        }

        static byGenre(genre) {
            return Object.entries(GAMES)
                .filter(([, game]) =>
                    game.genre.includes(genre)
                )
                .map(([id, game]) => ({
                    id,
                    ...game
                }));
        }
    }

    global.AJVYRA30GameExperienceRegistry =
        AJVYRA30GameExperienceRegistry;

})(window);
