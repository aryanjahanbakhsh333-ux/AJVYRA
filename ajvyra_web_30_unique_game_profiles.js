(function (global) {
    "use strict";

    const profiles = {
        "shadow-runner": {
            title: "Shadow Runner",
            story:
                "A courier crosses a collapsing midnight city while a shadow network hunts every signal he carries.",
            objective:
                "Reach the extraction point before the shadow hunters surround you.",
            controls: {
                primary: "Dash",
                secondary: "Strike",
                utility: "Slide",
                movement: "Virtual Stick"
            },
            mechanics: [
                "dash",
                "wall-slide",
                "shadow-combo"
            ],
            victory: "Reach extraction",
            defeat: "Lose all health"
        },

        "neon-drift": {
            title: "Neon Drift",
            story:
                "An illegal night race becomes a desperate escape through a city controlled by automated racers.",
            objective:
                "Complete three laps and pass every checkpoint.",
            controls: {
                primary: "Accelerate",
                secondary: "Brake",
                utility: "Nitro",
                movement: "Steering"
            },
            mechanics: [
                "drift",
                "nitro",
                "checkpoint"
            ],
            victory: "Finish the race",
            defeat: "Crash or timeout"
        },

        "void-arena": {
            title: "Void Arena",
            story:
                "A fighter trapped inside a gravityless arena must defeat opponents to earn freedom.",
            objective:
                "Defeat the arena champion.",
            controls: {
                primary: "Light Attack",
                secondary: "Heavy Attack",
                utility: "Dodge",
                movement: "Move"
            },
            mechanics: [
                "combo",
                "dodge",
                "counter"
            ],
            victory: "Defeat champion",
            defeat: "Health reaches zero"
        },

        "lost-realm": {
            title: "Lost Realm",
            story:
                "A forgotten kingdom wakes beneath the ruins and calls its last traveler back home.",
            objective:
                "Complete the kingdom quest chain.",
            controls: {
                primary: "Interact",
                secondary: "Attack",
                utility: "Inventory",
                movement: "Move"
            },
            mechanics: [
                "quest",
                "inventory",
                "level-up"
            ],
            victory: "Complete the final quest",
            defeat: "Player falls"
        },

        "night-hunt": {
            title: "Night Hunt",
            story:
                "Something hunts between the trees. You have one night to survive.",
            objective:
                "Survive ten escalating hunting waves.",
            controls: {
                primary: "Fire",
                secondary: "Reload",
                utility: "Flashlight",
                movement: "Move"
            },
            mechanics: [
                "waves",
                "stealth",
                "limited-ammo"
            ],
            victory: "Survive wave ten",
            defeat: "Hunted down"
        },

        "cyber-strike": {
            title: "Cyber Strike",
            story:
                "A lone operative breaches a hostile machine district before the city network is erased.",
            objective:
                "Destroy every hostile target.",
            controls: {
                primary: "Shoot",
                secondary: "Aim",
                utility: "Grenade",
                movement: "Move"
            },
            mechanics: [
                "aim",
                "cover",
                "projectiles"
            ],
            victory: "Destroy all targets",
            defeat: "Health reaches zero"
        },

        "frostbound": {
            title: "Frostbound",
            story:
                "The temperature is falling unnaturally. Find the frozen beacon before the storm consumes the valley.",
            objective:
                "Keep moving and reach the beacon.",
            controls: {
                primary: "Torch",
                secondary: "Strike",
                utility: "Warmth",
                movement: "Move"
            },
            mechanics: [
                "temperature",
                "exploration",
                "survival"
            ],
            victory: "Activate beacon",
            defeat: "Freeze"
        },

        "sky-raiders": {
            title: "Sky Raiders",
            story:
                "Air pirates attack from above while your damaged craft searches for a safe route home.",
            objective:
                "Survive the aerial assault.",
            controls: {
                primary: "Fire",
                secondary: "Boost",
                utility: "Roll",
                movement: "Flight"
            },
            mechanics: [
                "air-control",
                "boost",
                "enemy-aircraft"
            ],
            victory: "Reach the safe zone",
            defeat: "Aircraft destroyed"
        },

        "dungeon-zero": {
            title: "Dungeon Zero",
            story:
                "Every door in the dungeon leads deeper. The first room was never the beginning.",
            objective:
                "Find the hidden exit.",
            controls: {
                primary: "Attack",
                secondary: "Interact",
                utility: "Map",
                movement: "Move"
            },
            mechanics: [
                "rooms",
                "loot",
                "keys"
            ],
            victory: "Escape dungeon",
            defeat: "Party defeated"
        },

        "pulse-breaker": {
            title: "Pulse Breaker",
            story:
                "A city reactor pulses faster every second. Break the rhythm before it reaches critical overload.",
            objective:
                "Destroy targets according to the pulse rhythm.",
            controls: {
                primary: "Pulse",
                secondary: "Chain",
                utility: "Overdrive",
                movement: "Lane Switch"
            },
            mechanics: [
                "rhythm",
                "combo",
                "score"
            ],
            victory: "Break the reactor",
            defeat: "Overload"
        },

        "shadow-duel": {
            title: "Shadow Duel",
            story:
                "Two fighters enter a silent arena where every attack can become the final one.",
            objective:
                "Win the duel.",
            controls: {
                primary: "Attack",
                secondary: "Guard",
                utility: "Counter",
                movement: "Step"
            },
            mechanics: [
                "timing",
                "guard",
                "counter"
            ],
            victory: "Opponent defeated",
            defeat: "Player defeated"
        },

        "crystal-quest": {
            title: "Crystal Quest",
            story:
                "Crystals are disappearing from an ancient world and leaving entire regions powerless.",
            objective:
                "Recover every crystal.",
            controls: {
                primary: "Collect",
                secondary: "Interact",
                utility: "Scan",
                movement: "Move"
            },
            mechanics: [
                "collection",
                "scanning",
                "exploration"
            ],
            victory: "Recover all crystals",
            defeat: "Player falls"
        },

        "iron-frontier": {
            title: "Iron Frontier",
            story:
                "Two frontier settlements fight for the final energy source.",
            objective:
                "Capture the enemy command base.",
            controls: {
                primary: "Deploy",
                secondary: "Attack",
                utility: "Build",
                movement: "Select"
            },
            mechanics: [
                "resources",
                "bases",
                "deployment"
            ],
            victory: "Destroy enemy base",
            defeat: "Base destroyed"
        },

        "ghost-signal": {
            title: "Ghost Signal",
            story:
                "A radio signal repeats your name from an abandoned facility.",
            objective:
                "Trace the signal without being detected.",
            controls: {
                primary: "Scan",
                secondary: "Flash",
                utility: "Hide",
                movement: "Move"
            },
            mechanics: [
                "stealth",
                "signal-tracing",
                "fear"
            ],
            victory: "Find the source",
            defeat: "Detected"
        },

        "bladefall": {
            title: "Bladefall",
            story:
                "A warrior enters a ruined city where blades fall from the sky.",
            objective:
                "Cross the blade zone and defeat its guardian.",
            controls: {
                primary: "Slash",
                secondary: "Block",
                utility: "Dash",
                movement: "Move"
            },
            mechanics: [
                "timed-attacks",
                "blocking",
                "falling-blades"
            ],
            victory: "Defeat guardian",
            defeat: "Health reaches zero"
        },

        "orbit-zero": {
            title: "Orbit Zero",
            story:
                "Your ship wakes outside a dead planet with unknown objects approaching.",
            objective:
                "Destroy hostile objects and escape orbit.",
            controls: {
                primary: "Fire",
                secondary: "Rotate",
                utility: "Boost",
                movement: "Orbit"
            },
            mechanics: [
                "orbital-motion",
                "targeting",
                "boost"
            ],
            victory: "Escape orbit",
            defeat: "Ship destroyed"
        },

        "wildfire": {
            title: "Wildfire",
            story:
                "A fireline moves across the valley while survivors wait for evacuation.",
            objective:
                "Reach the evacuation zone before time expires.",
            controls: {
                primary: "Sprint",
                secondary: "Rescue",
                utility: "Extinguish",
                movement: "Move"
            },
            mechanics: [
                "timer",
                "rescue",
                "fire-spread"
            ],
            victory: "Evacuation complete",
            defeat: "Time expires"
        },

        "rune-knight": {
            title: "Rune Knight",
            story:
                "An ancient rune awakens inside a knight who must decide which power to trust.",
            objective:
                "Defeat the rune guardian.",
            controls: {
                primary: "Sword",
                secondary: "Shield",
                utility: "Rune",
                movement: "Move"
            },
            mechanics: [
                "magic",
                "sword-combat",
                "rune-selection"
            ],
            victory: "Guardian defeated",
            defeat: "Health reaches zero"
        },

        "dark-circuit": {
            title: "Dark Circuit",
            story:
                "The final street race begins after the city's power grid shuts down.",
            objective:
                "Win the underground race.",
            controls: {
                primary: "Accelerate",
                secondary: "Brake",
                utility: "Drift",
                movement: "Steering"
            },
            mechanics: [
                "drifting",
                "traffic",
                "shortcut"
            ],
            victory: "Cross finish line first",
            defeat: "Vehicle destroyed"
        },

        "titan-core": {
            title: "Titan Core",
            story:
                "A mechanical titan powers itself from a core that cannot be destroyed by ordinary attacks.",
            objective:
                "Break all three Titan phases.",
            controls: {
                primary: "Attack",
                secondary: "Dodge",
                utility: "Target Core",
                movement: "Move"
            },
            mechanics: [
                "boss-phases",
                "weak-points",
                "rage"
            ],
            victory: "Destroy Titan",
            defeat: "Player defeated"
        },

        "moonfall": {
            title: "Moonfall",
            story:
                "Fragments of the moon begin falling toward a world that has forgotten the sky.",
            objective:
                "Reach the ancient observatory.",
            controls: {
                primary: "Interact",
                secondary: "Jump",
                utility: "Compass",
                movement: "Move"
            },
            mechanics: [
                "exploration",
                "platforming",
                "navigation"
            ],
            victory: "Reach observatory",
            defeat: "Fall"
        },

        "last-fortress": {
            title: "Last Fortress",
            story:
                "One fortress remains between the invading army and the last surviving city.",
            objective:
                "Defend the fortress through every wave.",
            controls: {
                primary: "Build",
                secondary: "Repair",
                utility: "Command",
                movement: "Select"
            },
            mechanics: [
                "tower-defense",
                "resources",
                "waves"
            ],
            victory: "Survive all waves",
            defeat: "Fortress destroyed"
        },

        "phantom-chase": {
            title: "Phantom Chase",
            story:
                "A phantom vehicle appears only in reflections and challenges you to follow it.",
            objective:
                "Catch the phantom before it disappears.",
            controls: {
                primary: "Accelerate",
                secondary: "Brake",
                utility: "Boost",
                movement: "Steering"
            },
            mechanics: [
                "chase",
                "boost",
                "shortcut"
            ],
            victory: "Catch phantom",
            defeat: "Phantom escapes"
        },

        "abyss-walker": {
            title: "Abyss Walker",
            story:
                "The deeper you walk into the abyss, the less certain it becomes that you are alone.",
            objective:
                "Reach the deepest chamber.",
            controls: {
                primary: "Light",
                secondary: "Listen",
                utility: "Hide",
                movement: "Move"
            },
            mechanics: [
                "horror",
                "sound",
                "stealth"
            ],
            victory: "Reach chamber",
            defeat: "Caught"
        },

        "starbreaker": {
            title: "Starbreaker",
            story:
                "A fleet approaches a dying star. One pilot must break through before the star collapses.",
            objective:
                "Destroy the fleet commander.",
            controls: {
                primary: "Fire",
                secondary: "Missile",
                utility: "Shield",
                movement: "Flight"
            },
            mechanics: [
                "space-combat",
                "shield",
                "missiles"
            ],
            victory: "Commander destroyed",
            defeat: "Ship destroyed"
        },

        "kingdom-ashes": {
            title: "Kingdom Ashes",
            story:
                "A fallen prince returns to a kingdom built over its own ruins.",
            objective:
                "Complete the restoration quest.",
            controls: {
                primary: "Attack",
                secondary: "Interact",
                utility: "Inventory",
                movement: "Move"
            },
            mechanics: [
                "rpg",
                "quests",
                "equipment"
            ],
            victory: "Restore kingdom",
            defeat: "Party defeated"
        },

        "zero-hour": {
            title: "Zero Hour",
            story:
                "A countdown has begun and nobody knows who started it.",
            objective:
                "Complete every emergency objective before zero.",
            controls: {
                primary: "Interact",
                secondary: "Sprint",
                utility: "Scanner",
                movement: "Move"
            },
            mechanics: [
                "countdown",
                "objectives",
                "speed"
            ],
            victory: "Complete objectives",
            defeat: "Countdown reaches zero"
        },

        "echo-maze": {
            title: "Echo Maze",
            story:
                "The maze changes whenever you make a sound.",
            objective:
                "Solve the maze's sequence and find the exit.",
            controls: {
                primary: "Choose",
                secondary: "Listen",
                utility: "Remember",
                movement: "Navigate"
            },
            mechanics: [
                "sequence",
                "memory",
                "dynamic-maze"
            ],
            victory: "Solve maze",
            defeat: "Wrong sequence"
        },

        "final-horizon": {
            title: "Final Horizon",
            story:
                "At the edge of the world, a traveler finds a horizon that should not exist.",
            objective:
                "Reach the final horizon.",
            controls: {
                primary: "Interact",
                secondary: "Jump",
                utility: "Compass",
                movement: "Move"
            },
            mechanics: [
                "exploration",
                "platforming",
                "environment"
            ],
            victory: "Reach horizon",
            defeat: "Fall"
        },

        "ajvyra-genesis": {
            title: "AJVYRA: Genesis",
            story:
                "The first world of AJVYRA is waking. Its future depends on the choices of one player.",
            objective:
                "Complete the Genesis campaign.",
            controls: {
                primary: "Attack",
                secondary: "Interact",
                utility: "Ability",
                movement: "Move"
            },
            mechanics: [
                "rpg",
                "quest",
                "combat",
                "progression"
            ],
            victory: "Complete Genesis",
            defeat: "Campaign defeat"
        }
    };

    class AJVYRAWeb30UniqueGameProfiles {
        static get(id) {
            return profiles[String(id)] || null;
        }

        static all() {
            return Object.entries(profiles).map(
                ([id, profile]) => ({
                    id,
                    ...profile
                })
            );
        }

        static has(id) {
            return Boolean(
                profiles[String(id)]
            );
        }

        static validate(id) {
            const profile =
                profiles[String(id)];

            if (!profile) {
                return {
                    valid: false,
                    errors: ["Missing profile"]
                };
            }

            const errors = [];

            if (!profile.story) {
                errors.push("Missing story");
            }

            if (!profile.objective) {
                errors.push("Missing objective");
            }

            if (!profile.controls) {
                errors.push("Missing controls");
            }

            if (
                !Array.isArray(
                    profile.mechanics
                ) ||
                profile.mechanics.length === 0
            ) {
                errors.push(
                    "Missing unique mechanics"
                );
            }

            return {
                valid: errors.length === 0,
                errors
            };
        }
    }

    global.AJVYRAWeb30UniqueGameProfiles =
        AJVYRAWeb30UniqueGameProfiles;

})(window);
