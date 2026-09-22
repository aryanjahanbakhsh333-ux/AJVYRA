(function (global) {
  "use strict";

  class AJVYRAActualGamePlayabilityProbe {
    constructor(options = {}) {
      this.options = options;
      this.results = [];
    }

    createCanvas() {
      const canvas = document.createElement("canvas");

      canvas.width = 960;
      canvas.height = 540;

      canvas.style.display = "none";

      document.body.appendChild(canvas);

      return canvas;
    }

    resolveScenario(gameId) {
      const registry = global.AJVYRAWeb30GameScenarios;

      if (!registry) {
        throw new Error("Scenario registry unavailable.");
      }

      if (typeof registry.get === "function") {
        return registry.get(gameId);
      }

      return registry[gameId] || null;
    }

    resolveRuntime() {
      return (
        global.AJVYRAProfessionalGameRuntime ||
        global.AJVYRAWebProfessionalGameEngine ||
        null
      );
    }

    inspectRuntime(runtime) {
      const update =
        typeof runtime.update === "function";

      const render =
        typeof runtime.render === "function" ||
        typeof runtime.draw === "function";

      const action =
        typeof runtime.handleAction === "function" ||
        typeof runtime.dispatchAction === "function" ||
        typeof runtime.emitAction === "function";

      return {
        update,
        render,
        action,
        runtimeContract: update && render
      };
    }

    probeGame(gameId) {
      const started = performance.now();

      let canvas = null;
      let runtime = null;

      try {
        const Runtime = this.resolveRuntime();

        if (!Runtime) {
          throw new Error(
            "No professional runtime constructor found."
          );
        }

        const scenario = this.resolveScenario(gameId);

        if (!scenario) {
          throw new Error(
            "Scenario not found for " + gameId
          );
        }

        canvas = this.createCanvas();

        runtime = new Runtime({
          canvas,
          scenario,
          gameId
        });

        const contract = this.inspectRuntime(runtime);

        if (!contract.runtimeContract) {
          throw new Error(
            "Runtime lacks update/render contract."
          );
        }

        const dt = 1 / 60;

        for (let i = 0; i < 3; i += 1) {
          runtime.update(dt);
        }

        if (typeof runtime.render === "function") {
          runtime.render();
        } else {
          runtime.draw();
        }

        const result = {
          gameId,
          ok: true,
          runtimeConstructed: true,
          updateExecuted: true,
          renderExecuted: true,
          actionContract: contract.action,
          elapsedMs: Math.round(performance.now() - started)
        };

        this.results.push(result);

        return result;
      } catch (error) {
        const result = {
          gameId,
          ok: false,
          runtimeConstructed: Boolean(runtime),
          error: error.message,
          elapsedMs: Math.round(performance.now() - started)
        };

        this.results.push(result);

        return result;
      } finally {
        if (canvas && canvas.parentNode) {
          canvas.parentNode.removeChild(canvas);
        }

        if (runtime) {
          for (const method of [
            "stop",
            "destroy",
            "dispose"
          ]) {
            if (typeof runtime[method] === "function") {
              try {
                runtime[method]();
              } catch (_) {
                // Cleanup must not break the probe.
              }
            }
          }
        }
      }
    }

    probeAll(gameIds) {
      this.results = [];

      for (const gameId of gameIds) {
        this.probeGame(gameId);
      }

      const passed = this.results.filter(
        (result) => result.ok
      ).length;

      return {
        total: this.results.length,
        passed,
        failed: this.results.length - passed,
        results: [...this.results],
        ok:
          this.results.length > 0 &&
          passed === this.results.length
      };
    }
  }

  global.AJVYRAActualGamePlayabilityProbe =
    AJVYRAActualGamePlayabilityProbe;
})(window);
