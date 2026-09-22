(function (global) {
  "use strict";

  class AJVYRARealGameLauncherBridge {
    constructor(options = {}) {
      this.options = options;
      this.mount = null;
      this.adapter = null;
      this.gameId = null;
      this.started = false;
    }

    resolveGameId() {
      return (
        this.options.gameId ||
        document.body.dataset.gameId ||
        new URLSearchParams(location.search).get("game")
      );
    }

    start() {
      this.gameId = this.resolveGameId();

      if (!this.gameId) {
        throw new Error("AJVYRA: game id missing.");
      }

      if (!global.AJVYRAActualGameMountBridge) {
        throw new Error(
          "AJVYRAActualGameMountBridge is not loaded."
        );
      }

      this.mount = new global.AJVYRAActualGameMountBridge({
        gameId: this.gameId,
        root:
          this.options.root ||
          document.getElementById("ajvyra-game-root") ||
          document.body
      });

      const result = this.mount.mount();

      if (!result.ok) {
        throw new Error(
          result.error ||
          "AJVYRA game runtime failed to mount."
        );
      }

      if (
        !this.mount.runtime ||
        !this.mount.canvas
      ) {
        throw new Error(
          "AJVYRA game runtime did not produce a playable surface."
        );
      }

      if (global.AJVYRAUniqueActionAdapter) {
        this.adapter =
          new global.AJVYRAUniqueActionAdapter(
            this.mount.runtime,
            this.gameId
          );

        this.adapter.bind(
          this.options.controlRoot ||
          document.body
        );
      }

      this.started = true;

      window.dispatchEvent(
        new CustomEvent(
          "ajvyra:real-game-started",
          {
            detail: {
              gameId: this.gameId,
              runtime: this.mount.runtime,
              canvas: this.mount.canvas
            }
          }
        )
      );

      return {
        ok: true,
        gameId: this.gameId,
        runtimeReady: true,
        canvasReady: true,
        actionsReady: Boolean(this.adapter)
      };
    }

    stop() {
      if (this.mount) {
        this.mount.destroy();
      }

      this.started = false;
    }
  }

  global.AJVYRARealGameLauncherBridge =
    AJVYRARealGameLauncherBridge;

})(window);
