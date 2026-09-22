(function (global) {
  "use strict";

  class AJVYRAStrategyGameplay {
    constructor(core) {
      this.core = core;

      this.resources = {
        energy: 100,
        metal: 80,
        food: 100
      };

      this.bases = [];
      this.units = [];

      this.wave = 1;
      this.enemyPressure = 0;

      this.generateBases();
    }

    generateBases() {
      this.bases = [
        {
          id: "alpha",
          x: this.core.width * 0.25,
          y: this.core.height * 0.35,
          owner: "player",
          health: 100
        },
        {
          id: "beta",
          x: this.core.width * 1.35,
          y: this.core.height * 0.55,
          owner: "neutral",
          health: 100
        },
        {
          id: "gamma",
          x: this.core.width * 1.7,
          y: this.core.height * 1.35,
          owner: "enemy",
          health: 100
        }
      ];
    }

    update(dt) {
      this.resources.energy =
        Math.min(
          200,
          this.resources.energy + dt * 2
        );

      this.resources.food =
        Math.max(
          0,
          this.resources.food - dt * 0.35
        );

      this.enemyPressure += dt;

      if (this.enemyPressure > 15) {
        this.enemyPressure = 0;
        this.spawnEnemyWave();
      }

      this.updateUnits(dt);
    }

    spawnEnemyWave() {
      this.wave++;

      this.core.notify(
        `ENEMY WAVE ${this.wave}`
      );

      for (let i = 0; i < this.wave; i++) {
        this.units.push({
          id: `enemy-unit-${Date.now()}-${i}`,
          x: this.core.width * 1.65,
          y: this.core.height * 1.2,
          vx: -30 - i * 3,
          vy: 0,
          owner: "enemy",
          health: 40
        });
      }
    }

    createUnit(type = "scout") {
      const costs = {
        scout: 15,
        soldier: 25,
        tank: 50
      };

      const cost =
        costs[type] || costs.scout;

      if (this.resources.energy < cost) {
        this.core.notify("Not enough energy.");
        return false;
      }

      this.resources.energy -= cost;

      this.units.push({
        id:
          `player-${type}-${Date.now()}`,
        x: this.core.width * 0.25,
        y: this.core.height * 0.35,
        vx: 20,
        vy: 0,
        owner: "player",
        type,
        health:
          type === "tank" ? 140 : 70
      });

      return true;
    }

    captureBase(id) {
      const base =
        this.bases.find(
          item => item.id === id
        );

      if (!base) return false;

      if (base.owner === "player") {
        return true;
      }

      base.owner = "player";

      this.core.addScore(300);
      this.core.notify(
        `BASE ${id.toUpperCase()} CAPTURED`
      );

      const playerBases =
        this.bases.filter(
          item => item.owner === "player"
        ).length;

      if (playerBases >= 3) {
        this.core.win(
          "The frontier belongs to you."
        );
      }

      return true;
    }

    updateUnits(dt) {
      for (const unit of this.units) {
        unit.x += unit.vx * dt;
        unit.y += unit.vy * dt;

        if (unit.owner === "enemy") {
          const base =
            this.bases.find(
              item => item.owner === "player"
            );

          if (base) {
            const dx = base.x - unit.x;
            const dy = base.y - unit.y;
            const d = Math.max(
              1,
              Math.hypot(dx, dy)
            );

            unit.vx =
              (dx / d) * 35;

            unit.vy =
              (dy / d) * 35;
          }
        }
      }
    }

    render(ctx, worldToScreen) {
      for (const base of this.bases) {
        const p =
          worldToScreen(
            base.x,
            base.y
          );

        ctx.beginPath();
        ctx.arc(
          p.x,
          p.y,
          38,
          0,
          Math.PI * 2
        );

        ctx.fillStyle =
          base.owner === "player"
            ? "#8fa99d"
            : base.owner === "enemy"
              ? "#704e5a"
              : "#77727d";

        ctx.fill();

        ctx.strokeStyle = "#ddd";
        ctx.lineWidth = 2;
        ctx.stroke();
      }
    }
  }

  global.AJVYRAStrategyGameplay =
    AJVYRAStrategyGameplay;

})(window);
