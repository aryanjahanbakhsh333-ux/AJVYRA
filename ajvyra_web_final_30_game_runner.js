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

  class AJVYRAFinal30GameRunner {
    constructor(options = {}) {
      this.options = options;
      this.results = new Map();
      this.running = false;
    }

    createCanvas() {
      const canvas = document.createElement("canvas");

      canvas.width = this.options.width || 1280;
      canvas.height = this.options.height || 720;

      canvas.style.width = "100%";
      canvas.style.maxWidth = "1280px";
      canvas.style.display = "block";

      return canvas;
    }

    async testGame(gameId) {
      const result = {
        gameId,
        runtimeCreated: false,
        started: false,
        updated: false,
        rendered: false,
        controlsAvailable: false,
        passed: false,
        error: null
      };

      let runtime = null;

      try {
        const canvas = this.createCanvas();
        const ctx = canvas.getContext("2d");

        if (!ctx) {
          throw new Error("Canvas 2D context unavailable.");
        }

        if (!global.AJVYRAFinalRuntimeContract) {
          throw new Error("Final runtime contract is not loaded.");
        }

        runtime =
          global.AJVYRAFinalRuntimeContract.create(gameId, {
            canvas
          });

        result.runtimeCreated = !!runtime;

        result.started =
          global.AJVYRAFinalRuntimeContract.start(runtime) || false;

        result.updated =
          global.AJVYRAFinalRuntimeContract.update(
            runtime,
            1 / 60
          ) || false;

        result.rendered =
          global.AJVYRAFinalRuntimeContract.render(
            runtime,
            ctx
          ) || false;

        result.controlsAvailable =
          typeof global.AJVYRAUniqueActionAdapter === "function" ||
          typeof global.AJVYRAWebUniversalInput === "function";

        result.passed =
          result.runtimeCreated &&
          result.started &&
          result.updated &&
          result.rendered;

      } catch (error) {
        result.error = error instanceof Error
          ? error.message
          : String(error);
      } finally {
        if (runtime && global.AJVYRAFinalRuntimeContract) {
          global.AJVYRAFinalRuntimeContract.stop(runtime);
        }
      }

      this.results.set(gameId, result);
      return result;
    }

    async runAll() {
      this.running = true;

      for (const gameId of GAME_IDS) {
        await this.testGame(gameId);
      }

      this.running = false;

      return this.report();
    }

    report() {
      const results = GAME_IDS.map(
        id => this.results.get(id) || {
          gameId: id,
          passed: false,
          error: "Not tested."
        }
      );

      const passed = results.filter(
        item => item.passed
      ).length;

      return {
        total: GAME_IDS.length,
        passed,
        failed: GAME_IDS.length - passed,
        complete: passed === GAME_IDS.length,
        results
      };
    }
  }

  global.AJVYRAFinal30GameRunner =
    AJVYRAFinal30GameRunner;

  global.AJVYRA_FINAL_GAME_IDS = GAME_IDS;
})(window);
