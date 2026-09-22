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

  class AJVYRA30GameRuntimeConnector {
    constructor() {
      this.registry = new Map();
    }

    register(id, factory) {
      if (!GAME_IDS.includes(id)) {
        throw new Error(
          "Unknown AJVYRA game id: " + id
        );
      }

      this.registry.set(id, factory);
    }

    registerAll() {
      for (const id of GAME_IDS) {
        this.register(id, (options = {}) => {
          if (!global.AJVYRAActualGameMountBridge) {
            throw new Error(
              "Actual game mount bridge unavailable."
            );
          }

          return new global.AJVYRAActualGameMountBridge({
            ...options,
            gameId: id
          });
        });
      }

      return this;
    }

    has(id) {
      return this.registry.has(id);
    }

    create(id, options = {}) {
      const factory = this.registry.get(id);

      if (!factory) {
        throw new Error(
          "No runtime connector for " + id
        );
      }

      return factory(options);
    }

    audit() {
      return GAME_IDS.map((id) => ({
        id,
        connected: this.has(id)
      }));
    }
  }

  const connector =
    new AJVYRA30GameRuntimeConnector();

  connector.registerAll();

  global.AJVYRA30GameRuntimeConnector =
    connector;

  global.AJVYRA30ConnectedGameIds =
    GAME_IDS.slice();

})(window);
