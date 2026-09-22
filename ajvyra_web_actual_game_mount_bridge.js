(function (global) {
  "use strict";

  class AJVYRAActualGameMountBridge {
    constructor(options = {}) {
      this.options = options;
      this.root = options.root || document.body;
      this.canvas = null;
      this.runtime = null;
      this.gameId = null;
      this.scenario = null;
      this.running = false;
      this.errors = [];
    }

    resolveGameId() {
      return (
        this.options.gameId ||
        document.body.dataset.gameId ||
        new URLSearchParams(window.location.search).get("game") ||
        null
      );
    }

    resolveScenario(gameId) {
      const scenarios = global.AJVYRAWeb30GameScenarios;

      if (!scenarios) {
        throw new Error("AJVYRAWeb30GameScenarios is unavailable.");
      }

      if (typeof scenarios.get === "function") {
        return scenarios.get(gameId);
      }

      if (scenarios[gameId]) {
        return scenarios[gameId];
      }

      throw new Error("No scenario registered for game: " + gameId);
    }

    createCanvas() {
      if (this.options.canvas instanceof HTMLCanvasElement) {
        this.canvas = this.options.canvas;
        return this.canvas;
      }

      const canvas = document.createElement("canvas");

      canvas.id = "ajvyra-game-canvas";
      canvas.setAttribute("aria-label", "AJVYRA game canvas");

      canvas.style.display = "block";
      canvas.style.width = "100%";
      canvas.style.height = "100%";
      canvas.style.touchAction = "none";

      this.root.appendChild(canvas);

      this.canvas = canvas;

      this.resizeCanvas();

      window.addEventListener("resize", () => {
        this.resizeCanvas();
      });

      window.addEventListener("orientationchange", () => {
        setTimeout(() => this.resizeCanvas(), 100);
      });

      return canvas;
    }

    resizeCanvas() {
      if (!this.canvas) {
        return;
      }

      const rect = this.canvas.getBoundingClientRect();

      const width = Math.max(320, Math.floor(rect.width || window.innerWidth));
      const height = Math.max(180, Math.floor(rect.height || window.innerHeight));

      const ratio = Math.max(
        1,
        Math.min(3, window.devicePixelRatio || 1)
      );

      this.canvas.width = Math.floor(width * ratio);
      this.canvas.height = Math.floor(height * ratio);

      const ctx = this.canvas.getContext("2d");

      if (ctx) {
        ctx.setTransform(ratio, 0, 0, ratio, 0, 0);
      }
    }

    createRuntime() {
      const Runtime =
        global.AJVYRAProfessionalGameRuntime ||
        global.AJVYRAWebProfessionalGameEngine;

      if (!Runtime) {
        throw new Error(
          "Professional game runtime is unavailable."
        );
      }

      const runtimeOptions = {
        canvas: this.canvas,
        scenario: this.scenario,
        gameId: this.gameId,
        profile: this.options.profile || null
      };

      this.runtime = new Runtime(runtimeOptions);

      return this.runtime;
    }

    startRuntime() {
      if (!this.runtime) {
        throw new Error("Runtime has not been created.");
      }

      if (typeof this.runtime.startProfessionalLoop === "function") {
        this.runtime.startProfessionalLoop();
        this.running = true;
        return;
      }

      if (typeof this.runtime.start === "function") {
        this.runtime.start();
        this.running = true;
        return;
      }

      if (typeof this.runtime.run === "function") {
        this.runtime.run();
        this.running = true;
        return;
      }

      throw new Error(
        "Runtime does not expose a supported start method."
      );
    }

    stopRuntime() {
      if (!this.runtime) {
        return;
      }

      const stopMethods = [
        "stopProfessionalLoop",
        "stop",
        "destroy",
        "dispose"
      ];

      for (const method of stopMethods) {
        if (typeof this.runtime[method] === "function") {
          try {
            this.runtime[method]();
          } catch (error) {
            this.errors.push(error);
          }
        }
      }

      this.running = false;
    }

    mount() {
      try {
        this.gameId = this.resolveGameId();

        if (!this.gameId) {
          throw new Error("No game ID was provided.");
        }

        this.scenario = this.resolveScenario(this.gameId);

        if (!this.scenario) {
          throw new Error(
            "Scenario resolution returned an empty result."
          );
        }

        this.createCanvas();
        this.createRuntime();
        this.startRuntime();

        const result = {
          ok: true,
          gameId: this.gameId,
          running: this.running,
          canvasReady: Boolean(this.canvas),
          runtimeReady: Boolean(this.runtime)
        };

        window.dispatchEvent(
          new CustomEvent("ajvyra:actual-game-mounted", {
            detail: result
          })
        );

        return result;
      } catch (error) {
        this.errors.push(error);

        const result = {
          ok: false,
          gameId: this.gameId,
          running: false,
          error: error.message,
          errors: this.errors.map((item) => item.message)
        };

        window.dispatchEvent(
          new CustomEvent("ajvyra:actual-game-mount-failed", {
            detail: result
          })
        );

        return result;
      }
    }

    destroy() {
      this.stopRuntime();

      if (
        this.canvas &&
        this.canvas.parentNode &&
        this.options.keepCanvas !== true
      ) {
        this.canvas.parentNode.removeChild(this.canvas);
      }

      this.canvas = null;
      this.runtime = null;
      this.scenario = null;
      this.running = false;
    }
  }

  global.AJVYRAActualGameMountBridge =
    AJVYRAActualGameMountBridge;
})(window);
