(function (global) {
  "use strict";

  const GAME_IDS = [
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

  const REQUIRED_CAPABILITIES = {
    "shadow-runner": ["movement", "dash", "combat"],
    "neon-drift": ["steering", "boost", "drift"],
    "void-arena": ["movement", "combat", "combo"],
    "lost-realm": ["movement", "combat", "quest"],
    "night-hunt": ["movement", "combat", "survival"],
    "cyber-strike": ["movement", "shooting", "reload"],
    "frostbound": ["movement", "combat", "survival"],
    "sky-raiders": ["movement", "shooting", "boost"],
    "dungeon-zero": ["movement", "combat", "interaction"],
    "pulse-breaker": ["movement", "pulse", "combo"],
    "shadow-duel": ["combat", "parry", "dodge"],
    "crystal-quest": ["movement", "collection", "interaction"],
    "iron-frontier": ["strategy", "building", "base-combat"],
    "ghost-signal": ["movement", "scanning", "stealth"],
    "bladefall": ["movement", "melee", "dodge"],
    "orbit-zero": ["movement", "shooting", "targeting"],
    "wildfire": ["movement", "combat", "timed-survival"],
    "rune-knight": ["movement", "combat", "magic"],
    "dark-circuit": ["steering", "boost", "drift"],
    "titan-core": ["movement", "boss-combat", "targeting"],
    "moonfall": ["exploration", "collection", "interaction"],
    "last-fortress": ["strategy", "building", "defense"],
    "phantom-chase": ["steering", "braking", "boost"],
    "abyss-walker": ["movement", "scanning", "stealth"],
    "starbreaker": ["movement", "shooting", "missiles"],
    "kingdom-ashes": ["movement", "combat", "quest"],
    "zero-hour": ["movement", "combat", "timed-objective"],
    "echo-maze": ["puzzle", "choice", "reset"],
    "final-horizon": ["exploration", "collection", "interaction"],
    "ajvyra-genesis": ["movement", "combat", "quest"]
  };

  const MATRIX = {};

  GAME_IDS.forEach((id) => {
    MATRIX[id] = {
      id,
      capabilities: [
        ...(REQUIRED_CAPABILITIES[id] || [])
      ],
      runtimeRequired: true,
      canvasRequired: true,
      touchRequired: true,
      landscapePreferred: true,
      manualVerificationRequired: true
    };
  });

  global.AJVYRAWeb30GamePlayabilityMatrix = MATRIX;
  global.AJVYRAWeb30GameIds = GAME_IDS;
})(window);
