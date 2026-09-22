(function (global) {
  "use strict";

  class AJVYRARealWorld {
    constructor(core, config = {}) {
      this.core = core;

      this.theme =
        config.theme || "dark";

      this.width =
        Number(config.width || core.width * 2);

      this.height =
        Number(config.height || core.height * 2);

      this.obstacles = [];
      this.pickups = [];
      this.decorations = [];

      this.generate(config);
    }

    generate(config = {}) {
      const seed =
        Number(config.seed || 7);

      const random = this.seededRandom(seed);

      this.obstacles = [];
      this.pickups = [];
      this.decorations = [];

      const obstacleCount =
        Math.max(
          8,
          Number(config.obstacleCount || 18)
        );

      for (
        let i = 0;
        i < obstacleCount;
        i++
      ) {
        const width =
          50 + random() * 130;

        const height =
          40 + random() * 100;

        this.obstacles.push({
          x:
            100 +
            random() *
            Math.max(100, this.width - 200),

          y:
            100 +
            random() *
            Math.max(100, this.height - 200),

          width,
          height
        });
      }

      const pickupCount =
        Number(config.pickupCount || 12);

      for (
        let i = 0;
        i < pickupCount;
        i++
      ) {
        this.pickups.push({
          id: `pickup-${i}`,
          x:
            100 +
            random() *
            Math.max(100, this.width - 200),

          y:
            100 +
            random() *
            Math.max(100, this.height - 200),

          radius: 10,
          type:
            i % 3 === 0
              ? "health"
              : "energy",

          active: true
        });
      }

      for (
        let i = 0;
        i < 80;
        i++
      ) {
        this.decorations.push({
          x: random() * this.width,
          y: random() * this.height,
          size: 8 + random() * 20,
          rotation: random() * Math.PI * 2
        });
      }
    }

    seededRandom(seed) {
      let value = seed >>> 0;

      return function () {
        value += 0x6D2B79F5;

        let t = value;

        t =
          Math.imul(
            t ^ (t >>> 15),
            t | 1
          );

        t ^=
          t +
          Math.imul(
            t ^ (t >>> 7),
            t | 61
          );

        return (
          ((t ^ (t >>> 14)) >>> 0) /
          4294967296
        );
      };
    }

    collides(entity) {
      const halfW =
        entity.width / 2;

      const halfH =
        entity.height / 2;

      const left =
        entity.x - halfW;

      const right =
        entity.x + halfW;

      const top =
        entity.y - halfH;

      const bottom =
        entity.y + halfH;

      for (const obstacle of this.obstacles) {
        if (
          right > obstacle.x &&
          left <
            obstacle.x + obstacle.width &&
          bottom > obstacle.y &&
          top <
            obstacle.y + obstacle.height
        ) {
          return obstacle;
        }
      }

      return null;
    }

    collectPickups(player) {
      for (const pickup of this.pickups) {
        if (!pickup.active) continue;

        const distance =
          Math.hypot(
            player.x - pickup.x,
            player.y - pickup.y
          );

        if (distance < 35) {
          pickup.active = false;

          if (
            pickup.type === "health"
          ) {
            player.heal(25);
            this.core.notify(
              "+25 HP"
            );
          } else {
            this.core.addScore(25);
            this.core.notify(
              "+25 Energy"
            );
          }
        }
      }
    }

    update() {
      if (!this.core.player) return;

      this.collectPickups(
        this.core.player
      );

      const obstacle =
        this.collides(
          this.core.player
        );

      if (obstacle) {
        this.core.player.x -=
          this.core.player.vx * 0.016;

        this.core.player.y -=
          this.core.player.vy * 0.016;
      }
    }
  }

  global.AJVYRARealWorld =
    AJVYRARealWorld;

})(window);
