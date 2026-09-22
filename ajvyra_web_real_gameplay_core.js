(function (global) {
  "use strict";

  class AJVYRARealEntity {
    constructor(config = {}) {
      this.id = config.id || `entity-${Math.random().toString(36).slice(2)}`;
      this.type = config.type || "neutral";

      this.x = Number(config.x || 0);
      this.y = Number(config.y || 0);

      this.width = Number(config.width || 32);
      this.height = Number(config.height || 32);

      this.vx = 0;
      this.vy = 0;

      this.speed = Number(config.speed || 180);

      this.maxHealth = Number(config.maxHealth || 100);
      this.health = this.maxHealth;

      this.damage = Number(config.damage || 10);

      this.active = true;
      this.invulnerable = 0;
      this.flash = 0;
      this.age = 0;

      this.tags = new Set(config.tags || []);
    }

    update(dt) {
      if (!this.active) return;

      this.x += this.vx * dt;
      this.y += this.vy * dt;

      this.age += dt;

      if (this.invulnerable > 0) {
        this.invulnerable = Math.max(0, this.invulnerable - dt);
      }

      if (this.flash > 0) {
        this.flash = Math.max(0, this.flash - dt);
      }
    }

    damageEntity(amount) {
      if (!this.active || this.invulnerable > 0) {
        return false;
      }

      const value = Math.max(0, Number(amount || 0));

      this.health = Math.max(
        0,
        this.health - value
      );

      this.flash = 0.12;

      if (this.health <= 0) {
        this.active = false;
      }

      return true;
    }

    heal(amount) {
      if (!this.active) return;

      this.health = Math.min(
        this.maxHealth,
        this.health + Math.max(0, Number(amount || 0))
      );
    }

    distanceTo(other) {
      if (!other) return Infinity;

      return Math.hypot(
        this.x - other.x,
        this.y - other.y
      );
    }

    bounds() {
      return {
        left: this.x - this.width / 2,
        right: this.x + this.width / 2,
        top: this.y - this.height / 2,
        bottom: this.y + this.height / 2
      };
    }
  }

  class AJVYRARealGameplayCore {
    constructor(config = {}) {
      this.gameId = config.gameId || "unknown";

      this.width = Number(config.width || 1280);
      this.height = Number(config.height || 720);

      this.entities = new Map();

      this.player = null;

      this.state = "loading";

      this.score = 0;
      this.stage = 1;
      this.time = 0;

      this.objective = {
        id: "survive",
        title: "Survive",
        progress: 0,
        target: 1,
        completed: false
      };

      this.messages = [];

      this.camera = {
        x: 0,
        y: 0,
        zoom: 1
      };

      this.world = {
        width: this.width * 2,
        height: this.height * 2
      };

      this.started = false;
      this.finished = false;
      this.won = false;
    }

    start() {
      if (this.started) return;

      this.started = true;
      this.finished = false;
      this.won = false;
      this.state = "playing";
    }

    stop() {
      this.state = "stopped";
      this.started = false;
    }

    addEntity(entity) {
      if (!entity) return;

      this.entities.set(entity.id, entity);

      if (entity.type === "player") {
        this.player = entity;
      }
    }

    removeEntity(id) {
      this.entities.delete(id);

      if (
        this.player &&
        this.player.id === id
      ) {
        this.player = null;
      }
    }

    setObjective(config = {}) {
      this.objective = {
        id: config.id || "objective",
        title: config.title || "Complete the objective",
        progress: Number(config.progress || 0),
        target: Math.max(
          1,
          Number(config.target || 1)
        ),
        completed: false
      };
    }

    advanceObjective(amount = 1) {
      if (this.objective.completed) return;

      this.objective.progress = Math.min(
        this.objective.target,
        this.objective.progress + amount
      );

      if (
        this.objective.progress >=
        this.objective.target
      ) {
        this.objective.completed = true;
      }
    }

    addScore(amount) {
      this.score += Math.max(
        0,
        Number(amount || 0)
      );
    }

    notify(text, duration = 3) {
      this.messages.push({
        text: String(text),
        time: duration
      });

      if (this.messages.length > 5) {
        this.messages.shift();
      }
    }

    clampEntity(entity) {
      const halfW = entity.width / 2;
      const halfH = entity.height / 2;

      entity.x = Math.max(
        halfW,
        Math.min(
          this.world.width - halfW,
          entity.x
        )
      );

      entity.y = Math.max(
        halfH,
        Math.min(
          this.world.height - halfH,
          entity.y
        )
      );
    }

    update(dt) {
      if (!this.started) return;

      if (
        this.state !== "playing" &&
        this.state !== "boss"
      ) {
        return;
      }

      const delta = Math.min(
        0.05,
        Math.max(0, Number(dt || 0))
      );

      this.time += delta;

      for (const entity of this.entities.values()) {
        entity.update(delta);

        if (entity.type !== "projectile") {
          this.clampEntity(entity);
        }
      }

      for (const message of this.messages) {
        message.time -= delta;
      }

      this.messages =
        this.messages.filter(
          message => message.time > 0
        );

      if (
        this.player &&
        !this.player.active
      ) {
        this.lose("You were defeated.");
      }

      this.updateCamera();
    }

    updateCamera() {
      if (!this.player) return;

      const targetX = this.player.x;
      const targetY = this.player.y;

      this.camera.x +=
        (targetX - this.camera.x) * 0.12;

      this.camera.y +=
        (targetY - this.camera.y) * 0.12;
    }

    win(message = "Mission complete.") {
      if (this.finished) return;

      this.finished = true;
      this.won = true;
      this.state = "victory";

      this.notify(message, 8);

      global.dispatchEvent(
        new CustomEvent(
          "ajvyra:game-victory",
          {
            detail: {
              gameId: this.gameId,
              score: this.score,
              stage: this.stage
            }
          }
        )
      );
    }

    lose(message = "Game over.") {
      if (this.finished) return;

      this.finished = true;
      this.won = false;
      this.state = "defeat";

      this.notify(message, 8);

      global.dispatchEvent(
        new CustomEvent(
          "ajvyra:game-defeat",
          {
            detail: {
              gameId: this.gameId,
              score: this.score,
              stage: this.stage
            }
          }
        )
      );
    }

    getActiveEntities() {
      return Array.from(
        this.entities.values()
      ).filter(entity => entity.active);
    }

    getEnemies() {
      return this.getActiveEntities().filter(
        entity => entity.type === "enemy" ||
          entity.type === "boss"
      );
    }
  }

  global.AJVYRARealEntity =
    AJVYRARealEntity;

  global.AJVYRARealGameplayCore =
    AJVYRARealGameplayCore;

})(window);
