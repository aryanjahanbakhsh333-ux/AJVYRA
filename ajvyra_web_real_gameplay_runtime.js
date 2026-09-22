(function (global) {
  "use strict";

  class AJVYRARealGameplayRuntime {
    constructor(config = {}) {
      this.gameId =
        config.gameId || "shadow-runner";

      this.canvas =
        config.canvas ||
        document.createElement("canvas");

      this.canvas.width =
        config.width || 1280;

      this.canvas.height =
        config.height || 720;

      this.canvas.style.width = "100%";
      this.canvas.style.maxWidth = "1280px";
      this.canvas.style.aspectRatio = "16 / 9";
      this.canvas.style.display = "block";

      this.core =
        new global.AJVYRARealGameplayCore({
          gameId: this.gameId,
          width: this.canvas.width,
          height: this.canvas.height
        });

      this.world =
        new global.AJVYRARealWorld(
          this.core,
          {
            seed:
              this.hashGameId(this.gameId),
            width:
              this.canvas.width * 2,
            height:
              this.canvas.height * 2
          }
        );

      this.player =
        new global.AJVYRARealPlayerController(
          this.core,
          {}
        );

      this.player.attachPointer(
        this.canvas
      );

      this.renderer =
        new global.AJVYRARealGameplayRenderer(
          this.canvas,
          this.core,
          this.world
        );

      this.running = false;
      this.frame = 0;
      this.lastTime = 0;

      this.setupGame();
    }

    hashGameId(value) {
      let hash = 2166136261;

      for (
        let i = 0;
        i < value.length;
        i++
      ) {
        hash ^= value.charCodeAt(i);
        hash +=
          (hash << 1) +
          (hash << 4) +
          (hash << 7) +
          (hash << 8) +
          (hash << 24);
      }

      return Math.abs(hash >>> 0);
    }

    setupGame() {
      this.core.setObjective({
        id: "enemies",
        title: "Clear the threat",
        target: 8
      });

      const enemyCount = 8;

      for (
        let i = 0;
        i < enemyCount;
        i++
      ) {
        const angle =
          (Math.PI * 2 * i) /
          enemyCount;

        const radius =
          280 + (i % 3) * 100;

        const enemy =
          new global.AJVYRARealEntity({
            id: `enemy-${i}`,
            type:
              i === enemyCount - 1
                ? "boss"
                : "enemy",
            x:
              this.canvas.width +
              Math.cos(angle) *
              radius,

            y:
              this.canvas.height +
              Math.sin(angle) *
              radius,

            width:
              i === enemyCount - 1
                ? 76
                : 34,

            height:
              i === enemyCount - 1
                ? 76
                : 42,

            maxHealth:
              i === enemyCount - 1
                ? 240
                : 55,

            damage:
              i === enemyCount - 1
                ? 25
                : 10
          });

        this.core.addEntity(enemy);
      }

      this.core.notify(
        this.storyIntro(),
        7
      );
    }

    storyIntro() {
      const stories = {
        "shadow-runner":
          "The city forgot your name. Tonight, you return for the truth.",

        "neon-drift":
          "The last checkpoint is beyond the dead district. Do not stop.",

        "void-arena":
          "Only one fighter leaves the arena. The Void is watching.",

        "lost-realm":
          "The kingdom disappeared overnight. Something beneath it survived.",

        "night-hunt":
          "When the lights die, the hunters wake.",

        "cyber-strike":
          "The enemy network has one weakness. You are standing inside it.",

        "frostbound":
          "The cold is not the only thing moving through the snow.",

        "sky-raiders":
          "Above the clouds, the war has already begun.",

        "dungeon-zero":
          "Every door leads deeper. Nobody has returned from the final room.",

        "pulse-breaker":
          "The city beats like a machine. Break its rhythm.",

        "shadow-duel":
          "Your opponent knows every move you have not made yet.",

        "crystal-quest":
          "The final crystal remembers a world that no longer exists.",

        "iron-frontier":
          "Build before the horizon fills with enemy banners.",

        "ghost-signal":
          "The transmission has your voice in it.",

        "bladefall":
          "The old warriors are gone. Your blade is all that remains.",

        "orbit-zero":
          "Something is moving outside the station. It should not be alive.",

        "wildfire":
          "The fire is spreading. Every second changes the map.",

        "rune-knight":
          "The last rune chose you. The ancient gate is opening.",

        "dark-circuit":
          "The track has no finish line. Only survivors.",

        "titan-core":
          "The machine was built to protect humanity. It no longer recognizes humanity.",

        "moonfall":
          "The moon is falling, and the old ruins are waking.",

        "last-fortress":
          "One fortress remains between the survivors and the dark.",

        "phantom-chase":
          "You are chasing something that may not exist.",

        "abyss-walker":
          "The deeper you walk, the quieter the world becomes.",

        "starbreaker":
          "The enemy fleet has arrived. Your ship is the last signal.",

        "kingdom-ashes":
          "Your kingdom burned. The crown survived.",

        "zero-hour":
          "The clock has started. There is no second attempt.",

        "echo-maze":
          "Every sound creates a path. Choose the right echo.",

        "final-horizon":
          "At the horizon waits the answer to everything you lost.",

        "ajvyra-genesis":
          "This is where every AJVYRA story begins."
      };

      return (
        stories[this.gameId] ||
        "Your story begins now."
      );
    }

    start() {
      if (this.running) return;

      this.running = true;

      this.core.start();

      this.lastTime =
        performance.now();

      this.loopId =
        global.requestAnimationFrame(
          this.loop.bind(this)
        );
    }

    loop(timestamp) {
      if (!this.running) return;

      const dt =
        Math.min(
          0.05,
          Math.max(
            0,
            (timestamp - this.lastTime) /
              1000
          )
        );

      this.lastTime = timestamp;

      this.update(dt);
      this.render();

      this.loopId =
        global.requestAnimationFrame(
          this.loop.bind(this)
        );
    }

    update(dt) {
      this.player.update(dt);

      this.updateEnemies(dt);

      this.world.update();

      this.core.update(dt);

      if (
        this.core.objective.completed &&
        this.core.state === "playing"
      ) {
        this.core.win(
          "The threat has been eliminated."
        );
      }
    }

    updateEnemies(dt) {
      if (!this.core.player) return;

      const player =
        this.core.player;

      for (
        const enemy
        of this.core.getEnemies()
      ) {
        if (!enemy.active) continue;

        const dx =
          player.x - enemy.x;

        const dy =
          player.y - enemy.y;

        const distance =
          Math.hypot(dx, dy);

        if (
          distance > 45
        ) {
          enemy.vx =
            (dx / Math.max(1, distance)) *
            enemy.speed *
            0.45;

          enemy.vy =
            (dy / Math.max(1, distance)) *
            enemy.speed *
            0.45;
        } else {
          enemy.vx = 0;
          enemy.vy = 0;

          if (
            enemy.age %
              1.2 <
            dt
          ) {
            player.damageEntity(
              enemy.damage
            );
          }
        }
      }
    }

    render() {
      this.renderer.render();
    }

    stop() {
      this.running = false;

      if (this.loopId) {
        global.cancelAnimationFrame(
          this.loopId
        );
      }

      this.player.destroy();

      this.core.stop();
    }

    destroy() {
      this.stop();
      this.canvas.remove();
    }
  }

  global.AJVYRARealGameplayRuntime =
    AJVYRARealGameplayRuntime;

})(window);
