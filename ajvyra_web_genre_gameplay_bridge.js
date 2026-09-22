(function (global) {
  "use strict";

  class AJVYRAGenreGameplayBridge {
    constructor(runtime) {
      this.runtime = runtime;

      this.core = runtime.core;
      this.player = runtime.player;

      this.director =
        new global.AJVYRADGenreGameDirector(
          this.core,
          runtime.gameId
        );

      this.director.configure();

      this.mechanics =
        new global.AJVYRAGenreMechanicsEngine(
          this.core,
          this.player,
          this.director
        );

      this.systems = {};

      this.createGenreSystems();
    }

    createGenreSystems() {
      const genres =
        this.director.genres;

      if (genres.includes("racing")) {
        this.systems.racing =
          new global.AJVYRARacingGameplay(
            this.core,
            this.player,
            this.mechanics
          );
      }

      if (genres.includes("rpg")) {
        this.systems.rpg =
          new global.AJVYRARPGGameplay(
            this.core,
            this.player,
            this.mechanics
          );
      }

      if (genres.includes("puzzle")) {
        this.systems.puzzle =
          new global.AJVYRAPuzzleGameplay(
            this.core,
            this.mechanics
          );
      }

      if (
        genres.includes("shooter") ||
        genres.includes("space")
      ) {
        this.systems.shooter =
          new global.AJVYRAShooterGameplay(
            this.core,
            this.player,
            this.mechanics
          );
      }

      if (genres.includes("horror")) {
        this.systems.horror =
          new global.AJVYRAHorrorGameplay(
            this.core,
            this.player
          );
      }

      if (genres.includes("strategy")) {
        this.systems.strategy =
          new global.AJVYRAStrategyGameplay(
            this.core
          );
      }

      if (genres.includes("adventure")) {
        this.systems.adventure =
          new global.AJVYRAAdventureGameplay(
            this.core,
            this.player
          );
      }
    }

    update(dt) {
      this.director.update(dt);
      this.mechanics.update(dt);

      for (const system of Object.values(
        this.systems
      )) {
        if (
          typeof system.update === "function"
        ) {
          system.update(dt);
        }
      }
    }

    render(ctx) {
      const worldToScreen =
        this.runtime.renderer.worldToScreen.bind(
          this.runtime.renderer
        );

      for (const system of Object.values(
        this.systems
      )) {
        if (
          typeof system.render === "function"
        ) {
          system.render(
            ctx,
            worldToScreen
          );
        }
      }

      if (this.systems.horror) {
        this.systems.horror.renderOverlay(
          ctx,
          this.runtime.renderer.viewWidth,
          this.runtime.renderer.viewHeight
        );
      }
    }

    action(action, payload = {}) {
      switch (action) {
        case "shoot":
          return this.systems.shooter?.fire(
            payload.x,
            payload.y
          );

        case "reload":
          return this.systems.shooter?.reload();

        case "checkpoint":
          return this.mechanics.passCheckpoint();

        case "capture":
          return this.systems.strategy?.captureBase(
            payload.id
          );

        case "build":
          return this.systems.strategy?.createUnit(
            payload.type
          );

        case "puzzle":
          return this.systems.puzzle?.input(
            payload.value
          );

        case "quest":
          return this.systems.rpg?.completeCurrentQuest();

        default:
          return false;
      }
    }
  }

  global.AJVYRAGenreGameplayBridge =
    AJVYRAGenreGameplayBridge;

})(window);
