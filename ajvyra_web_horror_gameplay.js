(function (global) {
  "use strict";

  class AJVYRAHorrorGameplay {
    constructor(core, player) {
      this.core = core;
      this.player = player;

      this.tension = 0;
      this.maxTension = 100;

      this.darkness = 0.72;
      this.chaseActive = false;

      this.events = [
        "footsteps",
        "whisper",
        "shadow",
        "false_memory",
        "silence"
      ];

      this.eventTimer = 7;
      this.eventIndex = 0;
    }

    update(dt) {
      this.eventTimer -= dt;

      if (this.eventTimer <= 0) {
        this.triggerEvent();
        this.eventTimer =
          6 + Math.random() * 8;
      }

      const nearbyEnemy =
        this.core.getEnemies().some(enemy =>
          enemy.active &&
          enemy.distanceTo(this.player.entity) < 260
        );

      if (nearbyEnemy) {
        this.chaseActive = true;
        this.tension += dt * 18;
      } else {
        this.chaseActive = false;
        this.tension -= dt * 8;
      }

      this.tension = Math.max(
        0,
        Math.min(
          this.maxTension,
          this.tension
        )
      );

      if (this.tension >= 100) {
        this.core.notify(
          "CONTROL YOUR FEAR"
        );

        this.player.entity.invulnerable = 0.2;
        this.tension = 70;
      }
    }

    triggerEvent() {
      const event =
        this.events[
          this.eventIndex %
          this.events.length
        ];

      this.eventIndex++;

      switch (event) {
        case "footsteps":
          this.core.notify(
            "Something is walking behind you."
          );
          break;

        case "whisper":
          this.core.notify(
            "You hear your name."
          );
          break;

        case "shadow":
          this.core.notify(
            "Something moved in the dark."
          );
          break;

        case "false_memory":
          this.core.notify(
            "You remember a place you have never seen."
          );
          break;

        case "silence":
          this.core.notify(
            "Everything suddenly goes quiet."
          );
          break;
      }
    }

    renderOverlay(ctx, width, height) {
      const gradient =
        ctx.createRadialGradient(
          width / 2,
          height / 2,
          80,
          width / 2,
          height / 2,
          Math.max(width, height) * 0.72
        );

      gradient.addColorStop(
        0,
        "rgba(0,0,0,0)"
      );

      gradient.addColorStop(
        1,
        `rgba(0,0,0,${this.darkness})`
      );

      ctx.fillStyle = gradient;
      ctx.fillRect(
        0,
        0,
        width,
        height
      );

      if (this.chaseActive) {
        ctx.fillStyle =
          "rgba(130,30,55,0.08)";

        ctx.fillRect(
          0,
          0,
          width,
          height
        );
      }
    }
  }

  global.AJVYRAHorrorGameplay =
    AJVYRAHorrorGameplay;

})(window);
