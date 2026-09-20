const AJVYRA_GAME_REGISTRY = {

    id: "game-01",

    title: "Black Run",

    version: "1.0.0",

    engine: "Phaser 3.90.0",

    genre: "Arcade Platformer",

    platform: [
        "desktop",
        "mobile"
    ],

    status: "development",

    systems: [
        "movement",
        "combat",
        "enemies",
        "collectibles",
        "missions",
        "quests",
        "checkpoints",
        "levels",
        "achievements",
        "rewards",
        "save-system",
        "difficulty",
        "mobile-input"
    ]
};


function getGameRegistry() {

    return {
        ...AJVYRA_GAME_REGISTRY
    };
}
