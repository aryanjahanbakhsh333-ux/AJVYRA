(function (global) {
  "use strict";

  class AJVYRARealGameplayRenderer {
    constructor(canvas, core, world) {
      this.canvas = canvas;
      this.ctx =
        canvas.getContext("2d");

      this.core = core;
      this.world = world;

      this.particles = [];

      this.resize();
    }

    resize() {
      const ratio =
        Math.min(
          2,
          global.devicePixelRatio || 1
        );

      const rect =
        this.canvas.getBoundingClientRect();

      const width =
        Math.max(
          320,
          Math.floor(rect.width || 1280)
        );

      const height =
        Math.max(
          180,
          Math.floor(rect.height || 720)
        );

      this.canvas.width =
        width * ratio;

      this.canvas.height =
        height * ratio;

      this.ctx.setTransform(
        ratio,
        0,
        0,
        ratio,
        0,
        0
      );

      this.viewWidth = width;
      this.viewHeight = height;
    }

    worldToScreen(x, y) {
      return {
        x:
          x -
          this.core.camera.x +
          this.viewWidth / 2,

        y:
          y -
          this.core.camera.y +
          this.viewHeight / 2
      };
    }

    render() {
      if (!this.ctx) return;

      this.drawBackground();
      this.drawWorld();
      this.drawEntities();
      this.drawParticles();
      this.drawHud();
    }

    drawBackground() {
      const ctx = this.ctx;

      const gradient =
        ctx.createLinearGradient(
          0,
          0,
          0,
          this.viewHeight
        );

      gradient.addColorStop(
        0,
        "#08080c"
      );

      gradient.addColorStop(
        1,
        "#17131b"
      );

      ctx.fillStyle = gradient;

      ctx.fillRect(
        0,
        0,
        this.viewWidth,
        this.viewHeight
      );
    }

    drawWorld() {
      const ctx = this.ctx;

      ctx.save();

      for (
        const decoration
        of this.world.decorations
      ) {
        const p =
          this.worldToScreen(
            decoration.x,
            decoration.y
          );

        if (
          p.x < -50 ||
          p.x > this.viewWidth + 50 ||
          p.y < -50 ||
          p.y > this.viewHeight + 50
        ) {
          continue;
        }

        ctx.save();

        ctx.translate(
          p.x,
          p.y
        );

        ctx.rotate(
          decoration.rotation
        );

        ctx.globalAlpha = 0.18;

        ctx.fillStyle =
          "#d9d0e5";

        ctx.fillRect(
          -decoration.size / 2,
          -decoration.size / 2,
          decoration.size,
          decoration.size
        );

        ctx.restore();
      }

      for (
        const obstacle
        of this.world.obstacles
      ) {
        const p =
          this.worldToScreen(
            obstacle.x,
            obstacle.y
          );

        ctx.fillStyle =
          "#211d27";

        ctx.strokeStyle =
          "#4c4354";

        ctx.lineWidth = 2;

        ctx.fillRect(
          p.x,
          p.y,
          obstacle.width,
          obstacle.height
        );

        ctx.strokeRect(
          p.x,
          p.y,
          obstacle.width,
          obstacle.height
        );
      }

      for (
        const pickup
        of this.world.pickups
      ) {
        if (!pickup.active) continue;

        const p =
          this.worldToScreen(
            pickup.x,
            pickup.y
          );

        ctx.beginPath();

        ctx.arc(
          p.x,
          p.y,
          pickup.radius,
          0,
          Math.PI * 2
        );

        ctx.fillStyle =
          pickup.type === "health"
            ? "#e7b8c8"
            : "#9db9d9";

        ctx.globalAlpha = 0.9;

        ctx.fill();

        ctx.globalAlpha = 1;
      }

      ctx.restore();
    }

    drawEntities() {
      for (
        const entity
        of this.core.getActiveEntities()
      ) {
        const p =
          this.worldToScreen(
            entity.x,
            entity.y
          );

        const ctx = this.ctx;

        ctx.save();

        ctx.translate(
          p.x,
          p.y
        );

        if (entity.flash > 0) {
          ctx.globalAlpha = 0.55;
        }

        if (
          entity.type === "player"
        ) {
          this.drawPlayer(entity);
        } else if (
          entity.type === "boss"
        ) {
          this.drawBoss(entity);
        } else if (
          entity.type === "enemy"
        ) {
          this.drawEnemy(entity);
        } else {
          this.drawNeutral(entity);
        }

        ctx.restore();
      }
    }

    drawPlayer(entity) {
      const ctx = this.ctx;

      ctx.fillStyle =
        "#d9d9df";

      ctx.beginPath();

      ctx.roundRect(
        -entity.width / 2,
        -entity.height / 2,
        entity.width,
        entity.height,
        9
      );

      ctx.fill();

      ctx.fillStyle =
        "#111116";

      ctx.beginPath();

      ctx.arc(
        0,
        -8,
        7,
        0,
        Math.PI * 2
      );

      ctx.fill();

      ctx.fillStyle =
        "#a991b4";

      ctx.fillRect(
        -4,
        3,
        8,
        16
      );
    }

    drawEnemy(entity) {
      const ctx = this.ctx;

      ctx.fillStyle =
        "#6f5665";

      ctx.beginPath();

      ctx.arc(
        0,
        0,
        Math.max(
          13,
          entity.width / 2
        ),
        0,
        Math.PI * 2
      );

      ctx.fill();

      ctx.fillStyle =
        "#e0cbd4";

      ctx.beginPath();

      ctx.arc(
        -5,
        -2,
        2,
        0,
        Math.PI * 2
      );

      ctx.arc(
        5,
        -2,
        2,
        0,
        Math.PI * 2
      );

      ctx.fill();
    }

    drawBoss(entity) {
      const ctx = this.ctx;

      const radius =
        Math.max(
          28,
          entity.width / 2
        );

      ctx.fillStyle =
        "#302637";

      ctx.beginPath();

      ctx.arc(
        0,
        0,
        radius,
        0,
        Math.PI * 2
      );

      ctx.fill();

      ctx.strokeStyle =
        "#bca8c6";

      ctx.lineWidth = 3;

      ctx.stroke();

      ctx.fillStyle =
        "#f0d9e3";

      ctx.beginPath();

      ctx.arc(
        -9,
        -5,
        4,
        0,
        Math.PI * 2
      );

      ctx.arc(
        9,
        -5,
        4,
        0,
        Math.PI * 2
      );

      ctx.fill();
    }

    drawNeutral(entity) {
      const ctx = this.ctx;

      ctx.fillStyle =
        "#77717c";

      ctx.fillRect(
        -entity.width / 2,
        -entity.height / 2,
        entity.width,
        entity.height
      );
    }

    drawParticles() {
      const ctx = this.ctx;

      for (
        const particle
        of this.particles
      ) {
        const p =
          this.worldToScreen(
            particle.x,
            particle.y
          );

        ctx.globalAlpha =
          Math.max(
            0,
            particle.life
          );

        ctx.fillStyle =
          particle.color ||
          "#d8c7dc";

        ctx.beginPath();

        ctx.arc(
          p.x,
          p.y,
          particle.size,
          0,
          Math.PI * 2
        );

        ctx.fill();
      }

      ctx.globalAlpha = 1;
    }

    drawHud() {
      const ctx = this.ctx;

      const player =
        this.core.player;

      if (!player) return;

      ctx.fillStyle =
        "rgba(0,0,0,.65)";

      ctx.fillRect(
        20,
        20,
        260,
        86
      );

      ctx.fillStyle =
        "#eee";

      ctx.font =
        "600 15px system-ui";

      ctx.fillText(
        this.core.gameId,
        34,
        43
      );

      ctx.fillStyle =
        "#342d39";

      ctx.fillRect(
        34,
        57,
        220,
        12
      );

      ctx.fillStyle =
        "#c99cab";

      ctx.fillRect(
        34,
        57,
        220 *
          (player.health /
            player.maxHealth),
        12
      );

      ctx.fillStyle =
        "#ddd";

      ctx.font =
        "12px system-ui";

      ctx.fillText(
        `HP ${Math.ceil(player.health)} / ${player.maxHealth}`,
        34,
        88
      );

      ctx.fillText(
        `SCORE ${this.core.score}`,
        170,
        88
      );

      const objective =
        this.core.objective;

      ctx.fillStyle =
        "rgba(0,0,0,.68)";

      ctx.fillRect(
        this.viewWidth - 300,
        20,
        270,
        68
      );

      ctx.fillStyle =
        "#eee";

      ctx.font =
        "600 13px system-ui";

      ctx.fillText(
        objective.title,
        this.viewWidth - 280,
        45
      );

      ctx.font =
        "12px system-ui";

      ctx.fillText(
        `${objective.progress} / ${objective.target}`,
        this.viewWidth - 280,
        68
      );

      if (
        this.core.state === "victory" ||
        this.core.state === "defeat"
      ) {
        this.drawEndScreen();
      }
    }

    drawEndScreen() {
      const ctx = this.ctx;

      ctx.fillStyle =
        "rgba(0,0,0,.76)";

      ctx.fillRect(
        0,
        0,
        this.viewWidth,
        this.viewHeight
      );

      ctx.textAlign = "center";

      ctx.fillStyle =
        "#f2eaf2";

      ctx.font =
        "700 42px system-ui";

      ctx.fillText(
        this.core.won
          ? "MISSION COMPLETE"
          : "YOU WERE DEFEATED",
        this.viewWidth / 2,
        this.viewHeight / 2 - 20
      );

      ctx.font =
        "16px system-ui";

      ctx.fillStyle =
        "#c8becb";

      ctx.fillText(
        `Score: ${this.core.score}`,
        this.viewWidth / 2,
        this.viewHeight / 2 + 22
      );

      ctx.textAlign = "left";
    }
  }

  global.AJVYRARealGameplayRenderer =
    AJVYRARealGameplayRenderer;

})(window);
