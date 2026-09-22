(function (global) {
    "use strict";

    const STORIES = {

        "shadow-runner": {
            title: "Shadow Runner",
            chapters: [
                {
                    speaker: "Unknown",
                    text: "The city forgot your name. The shadows didn't.",
                    choices: [
                        {
                            id: "run",
                            text: "Keep running.",
                            score: 10,
                            nextChapter: 1
                        },
                        {
                            id: "turn",
                            text: "Turn around.",
                            setFlag: "faced_past",
                            nextChapter: 1
                        }
                    ]
                },
                {
                    speaker: "Unknown",
                    text: "Something is following you through the ruined district.",
                    choices: [
                        {
                            id: "fight",
                            text: "Face it.",
                            setFlag: "faced_enemy",
                            nextChapter: 2
                        },
                        {
                            id: "escape",
                            text: "Disappear into the city.",
                            nextChapter: 2
                        }
                    ]
                },
                {
                    speaker: "System",
                    text: "The final gate is ahead. What you became decides how you cross it.",
                    choices: [
                        {
                            id: "finish",
                            text: "Enter the darkness.",
                            score: 100
                        }
                    ]
                }
            ]
        },

        "neon-drift": {
            title: "Neon Drift",
            chapters: [
                {
                    speaker: "Radio",
                    text: "The last race begins beneath a city that never sleeps.",
                    choices: [
                        {
                            id: "risk",
                            text: "Take the dangerous route.",
                            setFlag: "risk_taker",
                            score: 25
                        },
                        {
                            id: "safe",
                            text: "Stay on the clean line.",
                            score: 10
                        }
                    ]
                }
            ]
        },

        "void-arena": {
            title: "Void Arena",
            chapters: [
                {
                    speaker: "Announcer",
                    text: "Only one fighter leaves the Void Arena.",
                    choices: [
                        {
                            id: "honor",
                            text: "Fight with honor.",
                            setFlag: "honor"
                        },
                        {
                            id: "rage",
                            text: "Fight without mercy.",
                            setFlag: "rage"
                        }
                    ]
                }
            ]
        },

        "lost-realm": {
            title: "Lost Realm",
            chapters: [
                {
                    speaker: "Guide",
                    text: "The kingdom disappeared overnight. Its people left one message behind.",
                    choices: [
                        {
                            id: "search",
                            text: "Search the ruins.",
                            setFlag: "searched_ruins"
                        },
                        {
                            id: "follow",
                            text: "Follow the old road.",
                            setFlag: "followed_road"
                        }
                    ]
                }
            ]
        },

        "night-hunt": {
            title: "Night Hunt",
            chapters: [
                {
                    speaker: "Radio",
                    text: "The sun went down three hours ago. Something just answered your signal.",
                    choices: [
                        {
                            id: "signal",
                            text: "Answer the signal.",
                            setFlag: "answered_signal"
                        },
                        {
                            id: "hide",
                            text: "Kill the radio.",
                            setFlag: "silent"
                        }
                    ]
                }
            ]
        },

        "cyber-strike": {
            title: "Cyber Strike",
            chapters: [
                {
                    speaker: "Operator",
                    text: "The corporation owns the city. Tonight, you enter its core.",
                    choices: [
                        {
                            id: "hack",
                            text: "Break their system.",
                            setFlag: "hacker"
                        },
                        {
                            id: "assault",
                            text: "Attack directly.",
                            setFlag: "assault"
                        }
                    ]
                }
            ]
        },

        "frostbound": {
            title: "Frostbound",
            chapters: [
                {
                    speaker: "Survivor",
                    text: "The cold isn't the thing we should fear.",
                    choices: [
                        {
                            id: "shelter",
                            text: "Build shelter.",
                            setFlag: "shelter"
                        },
                        {
                            id: "search",
                            text: "Search the frozen city.",
                            setFlag: "search"
                        }
                    ]
                }
            ]
        },

        "sky-raiders": {
            title: "Sky Raiders",
            chapters: [
                {
                    speaker: "Captain",
                    text: "The enemy fleet is above the clouds.",
                    choices: [
                        {
                            id: "attack",
                            text: "Attack from above.",
                            setFlag: "air_attack"
                        },
                        {
                            id: "ambush",
                            text: "Wait for them.",
                            setFlag: "ambush"
                        }
                    ]
                }
            ]
        },

        "dungeon-zero": {
            title: "Dungeon Zero",
            chapters: [
                {
                    speaker: "Unknown",
                    text: "Every dungeon has an entrance. This one has no exit.",
                    choices: [
                        {
                            id: "enter",
                            text: "Enter anyway.",
                            setFlag: "entered"
                        }
                    ]
                }
            ]
        },

        "pulse-breaker": {
            title: "Pulse Breaker",
            chapters: [
                {
                    speaker: "System",
                    text: "The city runs on one pulse. Break it and everything changes.",
                    choices: [
                        {
                            id: "break",
                            text: "Break the pulse.",
                            score: 50
                        }
                    ]
                }
            ]
        },

        "shadow-duel": {
            title: "Shadow Duel",
            chapters: [
                {
                    speaker: "Opponent",
                    text: "I have waited years for this fight.",
                    choices: [
                        {
                            id: "accept",
                            text: "Draw your blade.",
                            setFlag: "duel"
                        }
                    ]
                }
            ]
        },

        "crystal-quest": {
            title: "Crystal Quest",
            chapters: [
                {
                    speaker: "Archivist",
                    text: "Five crystals. Five forgotten places. One truth.",
                    choices: [
                        {
                            id: "quest",
                            text: "Begin the search.",
                            setFlag: "quest_started"
                        }
                    ]
                }
            ]
        },

        "iron-frontier": {
            title: "Iron Frontier",
            chapters: [
                {
                    speaker: "Commander",
                    text: "The frontier is yours only if you can hold it.",
                    choices: [
                        {
                            id: "expand",
                            text: "Expand the base.",
                            setFlag: "expansion"
                        },
                        {
                            id: "defend",
                            text: "Fortify the base.",
                            setFlag: "defense"
                        }
                    ]
                }
            ]
        },

        "ghost-signal": {
            title: "Ghost Signal",
            chapters: [
                {
                    speaker: "Radio",
                    text: "A voice from a dead frequency is calling your name.",
                    choices: [
                        {
                            id: "answer",
                            text: "Answer.",
                            setFlag: "answered"
                        },
                        {
                            id: "leave",
                            text: "Leave the station.",
                            setFlag: "escaped"
                        }
                    ]
                }
            ]
        },

        "bladefall": {
            title: "Bladefall",
            chapters: [
                {
                    speaker: "Master",
                    text: "A warrior isn't measured by how many enemies fall.",
                    choices: [
                        {
                            id: "listen",
                            text: "Listen.",
                            setFlag: "discipline"
                        }
                    ]
                }
            ]
        },

        "orbit-zero": {
            title: "Orbit Zero",
            chapters: [
                {
                    speaker: "AI",
                    text: "Earth is below you. The signal is coming from beyond the moon.",
                    choices: [
                        {
                            id: "signal",
                            text: "Follow the signal.",
                            setFlag: "deep_space"
                        }
                    ]
                }
            ]
        },

        "wildfire": {
            title: "Wildfire",
            chapters: [
                {
                    speaker: "Emergency Radio",
                    text: "The fire crossed the river. You have one night.",
                    choices: [
                        {
                            id: "rescue",
                            text: "Save the people.",
                            setFlag: "rescuer"
                        },
                        {
                            id: "supplies",
                            text: "Secure supplies.",
                            setFlag: "survivor"
                        }
                    ]
                }
            ]
        },

        "rune-knight": {
            title: "Rune Knight",
            chapters: [
                {
                    speaker: "Elder",
                    text: "The final rune was never meant to be awakened.",
                    choices: [
                        {
                            id: "awaken",
                            text: "Awaken it.",
                            setFlag: "rune_awakened"
                        },
                        {
                            id: "seal",
                            text: "Seal it forever.",
                            setFlag: "rune_sealed"
                        }
                    ]
                }
            ]
        },

        "dark-circuit": {
            title: "Dark Circuit",
            chapters: [
                {
                    speaker: "Radio",
                    text: "One final race. No rules. No second chance.",
                    choices: [
                        {
                            id: "race",
                            text: "Start the engine.",
                            setFlag: "race"
                        }
                    ]
                }
            ]
        },

        "titan-core": {
            title: "Titan Core",
            chapters: [
                {
                    speaker: "System",
                    text: "The machine woke after a thousand years.",
                    choices: [
                        {
                            id: "challenge",
                            text: "Challenge the Titan.",
                            setFlag: "boss"
                        }
                    ]
                }
            ]
        },

        "moonfall": {
            title: "Moonfall",
            chapters: [
                {
                    speaker: "Explorer",
                    text: "The moon isn't falling. Something is pulling it.",
                    choices: [
                        {
                            id: "investigate",
                            text: "Investigate.",
                            setFlag: "investigate"
                        }
                    ]
                }
            ]
        },

        "last-fortress": {
            title: "Last Fortress",
            chapters: [
                {
                    speaker: "Commander",
                    text: "This is the last wall between them and everyone you love.",
                    choices: [
                        {
                            id: "defend",
                            text: "Hold the fortress.",
                            setFlag: "defender"
                        }
                    ]
                }
            ]
        },

        "phantom-chase": {
            title: "Phantom Chase",
            chapters: [
                {
                    speaker: "Radio",
                    text: "The car ahead doesn't appear on any camera.",
                    choices: [
                        {
                            id: "chase",
                            text: "Follow it.",
                            setFlag: "chase"
                        }
                    ]
                }
            ]
        },

        "abyss-walker": {
            title: "Abyss Walker",
            chapters: [
                {
                    speaker: "Unknown",
                    text: "The deeper you walk, the quieter the world becomes.",
                    choices: [
                        {
                            id: "descend",
                            text: "Descend.",
                            setFlag: "descent"
                        }
                    ]
                }
            ]
        },

        "starbreaker": {
            title: "Starbreaker",
            chapters: [
                {
                    speaker: "Commander",
                    text: "The fleet is behind you. The enemy is ahead.",
                    choices: [
                        {
                            id: "attack",
                            text: "Fire everything.",
                            setFlag: "attack"
                        }
                    ]
                }
            ]
        },

        "kingdom-ashes": {
            title: "Kingdom Ashes",
            chapters: [
                {
                    speaker: "King",
                    text: "A kingdom can be rebuilt. Trust cannot.",
                    choices: [
                        {
                            id: "rebuild",
                            text: "Rebuild.",
                            setFlag: "builder"
                        },
                        {
                            id: "revenge",
                            text: "Take revenge.",
                            setFlag: "revenge"
                        }
                    ]
                }
            ]
        },

        "zero-hour": {
            title: "Zero Hour",
            chapters: [
                {
                    speaker: "System",
                    text: "The countdown started before you woke up.",
                    choices: [
                        {
                            id: "move",
                            text: "Move now.",
                            setFlag: "fast"
                        }
                    ]
                }
            ]
        },

        "echo-maze": {
            title: "Echo Maze",
            chapters: [
                {
                    speaker: "Voice",
                    text: "Every wrong turn creates another version of you.",
                    choices: [
                        {
                            id: "listen",
                            text: "Follow the echo.",
                            setFlag: "echo"
                        },
                        {
                            id: "silence",
                            text: "Trust yourself.",
                            setFlag: "self"
                        }
                    ]
                }
            ]
        },

        "final-horizon": {
            title: "Final Horizon",
            chapters: [
                {
                    speaker: "Traveler",
                    text: "Beyond the horizon is the place everyone said didn't exist.",
                    choices: [
                        {
                            id: "continue",
                            text: "Keep going.",
                            setFlag: "journey"
                        }
                    ]
                }
            ]
        },

        "ajvyra-genesis": {
            title: "AJVYRA: Genesis",
            chapters: [
                {
                    speaker: "Unknown",
                    text: "Every world begins with a choice. This one begins with yours.",
                    choices: [
                        {
                            id: "create",
                            text: "Create a new world.",
                            setFlag: "creator"
                        },
                        {
                            id: "remember",
                            text: "Remember the old one.",
                            setFlag: "memory"
                        }
                    ]
                }
            ]
        }
    };

    class AJVYRA30GameStoryDatabase {
        static get(gameId) {
            return STORIES[gameId] || null;
        }

        static has(gameId) {
            return !!STORIES[gameId];
        }

        static list() {
            return Object.keys(STORIES);
        }

        static count() {
            return Object.keys(STORIES).length;
        }
    }

    global.AJVYRA30GameStoryDatabase =
        AJVYRA30GameStoryDatabase;

})(window);
