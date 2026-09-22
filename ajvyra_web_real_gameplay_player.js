(function (global) {
  "use strict";

  class AJVYRARealPlayerController {
    constructor(core, config = {}) {
      this.core = core;

      this.entity =
        new global.AJVYRARealEntity({
          id: "player",
          type: "player",
          x: config.x || core.width / 2,
          y: config.y || core.height / 2,
          width: config.width || 34,
          height: config.height || 48,
          speed: config.speed || 230,
          maxHealth: config.maxHealth || 100,
          damage: config.damage || 20,
          tags: ["player"]
        });

      this.core.addEntity(this.entity);

      this.keys = new Set();

      this.pointer = {
        active: false,
        x: 0,
        y: 0
      };

      this.actions = {
        attack: false,
        dodge: false,
        interact: false,
        ability: false
      };

      this.cooldowns = {
        attack: 0,
        dodge: 0,
        ability: 0
      };

      this.attackRange =
        Number(config.attackRange || 78);

      this.attackCooldown =
        Number(config.attackCooldown || 0.42);

      this.attackDamage =
        Number(config.attackDamage || 20);

      this.bindInput();
    }

    bindInput() {
      this.onKeyDown = event => {
        this.keys.add(
          String(event.key).toLowerCase()
        );

        this.readActionKey(
          String(event.key).toLowerCase()
        );
      };

      this.onKeyUp = event => {
        this.keys.delete(
          String(event.key).toLowerCase()
        );
      };

      global.addEventListener(
        "keydown",
        this.onKeyDown
      );

      global.addEventListener(
        "keyup",
        this.onKeyUp
      );
    }

    readActionKey(key) {
      if (
        key === " " ||
        key === "j" ||
        key === "z"
      ) {
        this.actions.attack = true;
      }

      if (
        key === "shift" ||
        key === "k"
      ) {
        this.actions.dodge = true;
      }

      if (
        key === "e"
      ) {
        this.actions.interact = true;
      }

      if (
        key === "q" ||
        key === "x"
      ) {
        this.actions.ability = true;
      }
    }

    attachPointer(canvas) {
      if (!canvas) return;

      this.canvas = canvas;

      this.onPointerDown = event => {
        this.pointer.active = true;

        const rect =
          canvas.getBoundingClientRect();

        this.pointer.x =
          event.clientX - rect.left;

        this.pointer.y =
          event.clientY - rect.top;

        this.actions.attack = true;
      };

      this.onPointerMove = event => {
        const rect =
          canvas.getBoundingClientRect();

        this.pointer.x =
          event.clientX - rect.left;

        this.pointer.y =
          event.clientY - rect.top;
      };

      this.onPointerUp = () => {
        this.pointer.active = false;
      };

      canvas.addEventListener(
        "pointerdown",
        this.onPointerDown
      );

      canvas.addEventListener(
        "pointermove",
        this.onPointerMove
      );

      canvas.addEventListener(
        "pointerup",
        this.onPointerUp
      );

      canvas.addEventListener(
        "pointercancel",
        this.onPointerUp
      );
    }

    movement() {
      let x = 0;
      let y = 0;

      if (
        this.keys.has("w") ||
        this.keys.has("arrowup")
      ) {
        y -= 1;
      }

      if (
        this.keys.has("s") ||
        this.keys.has("arrowdown")
      ) {
        y += 1;
      }

      if (
        this.keys.has("a") ||
        this.keys.has("arrowleft")
      ) {
        x -= 1;
      }

      if (
        this.keys.has("d") ||
        this.keys.has("arrowright")
      ) {
        x += 1;
      }

      const length =
        Math.hypot(x, y);

      if (length > 0) {
        x /= length;
        y /= length;
      }

      return { x, y };
    }

    attack() {
      if (
        this.cooldowns.attack > 0 ||
        !this.entity.active
      ) {
        return;
      }

      this.cooldowns.attack =
        this.attackCooldown;

      const enemies =
        this.core.getEnemies();

      let target = null;
      let nearest = Infinity;

      for (const enemy of enemies) {
        const distance =
          this.entity.distanceTo(enemy);

        if (
          distance <= this.attackRange &&
          distance < nearest
        ) {
          nearest = distance;
          target = enemy;
        }
      }

      if (target) {
        target.damageEntity(
          this.attackDamage
        );

        this.core.addScore(
          target.active ? 5 : 100
        );

        if (!target.active) {
          this.core.advanceObjective(1);
          this.core.notify(
            "+100  Enemy defeated"
          );
        }
      }
    }

    dodge() {
      if (
        this.cooldowns.dodge > 0 ||
        !this.entity.active
      ) {
        return;
      }

      this.cooldowns.dodge = 0.8;

      const direction =
        this.movement();

      let x = direction.x;
      let y = direction.y;

      if (x === 0 && y === 0) {
        x = 1;
      }

      this.entity.x += x * 95;
      this.entity.y += y * 95;

      this.entity.invulnerable = 0.25;
    }

    update(dt) {
      if (!this.entity.active) return;

      for (const key of Object.keys(
        this.cooldowns
      )) {
        this.cooldowns[key] =
          Math.max(
            0,
            this.cooldowns[key] - dt
          );
      }

      const direction =
        this.movement();

      this.entity.vx =
        direction.x * this.entity.speed;

      this.entity.vy =
        direction.y * this.entity.speed;

      if (this.actions.attack) {
        this.attack();
      }

      if (this.actions.dodge) {
        this.dodge();
      }

      this.actions.attack = false;
      this.actions.dodge = false;
      this.actions.interact = false;
      this.actions.ability = false;
    }

    destroy() {
      global.removeEventListener(
        "keydown",
        this.onKeyDown
      );

      global.removeEventListener(
        "keyup",
        this.onKeyUp
      );

      if (this.canvas) {
        this.canvas.removeEventListener(
          "pointerdown",
          this.onPointerDown
        );

        this.canvas.removeEventListener(
          "pointermove",
          this.onPointerMove
        );

        this.canvas.removeEventListener(
          "pointerup",
          this.onPointerUp
        );

        this.canvas.removeEventListener(
          "pointercancel",
          this.onPointerUp
        );
      }
    }
  }

  global.AJVYRARealPlayerController =
    AJVYRARealPlayerController;

})(window);
