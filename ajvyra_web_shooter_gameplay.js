(function (global) {
  "use strict";

  class AJVYRAShooterGameplay {
    constructor(core, player, mechanics) {
      this.core = core;
      this.player = player;
      this.mechanics = mechanics;

      this.ammo = 30;
      this.maxAmmo = 30;
      this.reloadTime = 1.4;
      this.reloadTimer = 0;

      this.fireCooldown = 0;
      this.fireRate = 0.16;

      this.projectiles = [];
      this.kills = 0;
    }

    update(dt) {
      if (this.reloadTimer > 0) {
        this.reloadTimer =
          Math.max(0, this.reloadTimer - dt);

        if (this.reloadTimer === 0) {
          this.ammo = this.maxAmmo;
        }
      }

      this.fireCooldown =
        Math.max(0, this.fireCooldown - dt);

      this.updateProjectiles(dt);
    }

    fire(targetX, targetY) {
      if (
        this.fireCooldown > 0 ||
        this.reloadTimer > 0 ||
        this.ammo <= 0
      ) {
        return false;
      }

      this.fireCooldown = this.fireRate;
      this.ammo--;

      const player = this.player.entity;

      const dx = targetX - player.x;
      const dy = targetY - player.y;
      const distance = Math.max(1, Math.hypot(dx, dy));

      this.projectiles.push({
        x: player.x,
        y: player.y,
        vx: (dx / distance) * 720,
        vy: (dy / distance) * 720,
        damage: 25,
        life: 1.4,
        radius: 5
      });

      return true;
    }

    reload() {
      if (
        this.reloadTimer > 0 ||
        this.ammo >= this.maxAmmo
      ) {
        return;
      }

      this.reloadTimer = this.reloadTime;

      this.core.notify("RELOADING...");
    }

    updateProjectiles(dt) {
      for (const projectile of this.projectiles) {
        projectile.x += projectile.vx * dt;
        projectile.y += projectile.vy * dt;
        projectile.life -= dt;

        if (projectile.life <= 0) {
          projectile.dead = true;
          continue;
        }

        for (const enemy of this.core.getEnemies()) {
          if (!enemy.active) continue;

          const distance = Math.hypot(
            projectile.x - enemy.x,
            projectile.y - enemy.y
          );

          if (distance < enemy.width / 2 + projectile.radius) {
            enemy.damageEntity(projectile.damage);
            projectile.dead = true;

            if (!enemy.active) {
              this.kills++;
              this.mechanics.gainExperience?.(75);
              this.core.advanceObjective(1);
              this.core.addScore(150);
            }

            break;
          }
        }
      }

      this.projectiles =
        this.projectiles.filter(
          projectile => !projectile.dead
        );
    }

    render(ctx, worldToScreen) {
      for (const projectile of this.projectiles) {
        const p = worldToScreen(
          projectile.x,
          projectile.y
        );

        ctx.beginPath();
        ctx.arc(
          p.x,
          p.y,
          projectile.radius,
          0,
          Math.PI * 2
        );

        ctx.fillStyle = "#e8e1ee";
        ctx.fill();
      }
    }
  }

  global.AJVYRAShooterGameplay =
    AJVYRAShooterGameplay;

})(window);
