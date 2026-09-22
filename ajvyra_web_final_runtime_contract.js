(function (global) {
  "use strict";

  class AJVYRAFinalRuntimeContract {
    static resolve(root = global) {
      const candidates = [
        root.AJVYRAProfessionalGameRuntime,
        root.AJVYRAActualGameMountBridge,
        root.AJVYRAWebProfessionalGameEngine,
        root.AJVYRAWebPlayableGameEngine
      ];

      for (const candidate of candidates) {
        if (typeof candidate === "function") {
          return candidate;
        }
      }

      return null;
    }

    static create(gameId, options = {}) {
      const Runtime = this.resolve();

      if (!Runtime) {
        throw new Error("AJVYRA runtime engine was not loaded.");
      }

      const config = {
        gameId,
        canvas: options.canvas || null,
        width: options.width || 1280,
        height: options.height || 720,
        ...options
      };

      let instance;

      try {
        instance = new Runtime(config);
      } catch (firstError) {
        try {
          instance = new Runtime(gameId, config);
        } catch (secondError) {
          throw new Error(
            `Runtime creation failed for ${gameId}: ${firstError.message} | ${secondError.message}`
          );
        }
      }

      if (!instance) {
        throw new Error(`Runtime returned no instance for ${gameId}.`);
      }

      return instance;
    }

    static start(instance) {
      if (!instance) {
        throw new Error("Cannot start empty runtime.");
      }

      if (typeof instance.start === "function") {
        instance.start();
        return true;
      }

      if (typeof instance.run === "function") {
        instance.run();
        return true;
      }

      if (typeof instance.play === "function") {
        instance.play();
        return true;
      }

      return false;
    }

    static update(instance, dt = 1 / 60) {
      if (!instance) return false;

      if (typeof instance.update === "function") {
        instance.update(dt);
        return true;
      }

      return false;
    }

    static render(instance, ctx) {
      if (!instance) return false;

      if (typeof instance.render === "function") {
        instance.render(ctx);
        return true;
      }

      if (typeof instance.draw === "function") {
        instance.draw(ctx);
        return true;
      }

      return false;
    }

    static stop(instance) {
      if (!instance) return;

      if (typeof instance.stop === "function") {
        instance.stop();
      } else if (typeof instance.destroy === "function") {
        instance.destroy();
      }
    }
  }

  global.AJVYRAFinalRuntimeContract = AJVYRAFinalRuntimeContract;
})(window);
