(function (global) {
  "use strict";

  class AJVYRAAdventureGameplay {
    constructor(core, player) {
      this.core = core;
      this.player = player;

      this.relics = [];
      this.discovered = 0;

      this.locations = [
        {
          id: "ruins",
          title: "The Forgotten Ruins",
          x: core.width * 0.4,
          y: core.height * 0.5
        },
        {
          id: "forest",
          title: "The Silent Forest",
          x: core.width * 1.2,
          y: core.height * 0.4
        },
        {
          id: "lake",
          title: "The Black Lake",
          x: core.width * 1.6,
          y: core.height * 1.1
        },
        {
          id: "tower",
          title: "The Broken Tower",
          x: core.width * 0.8,
          y: core.height * 1.6
        },
        {
          id: "gate",
          title: "The Final Gate",
          x: core.width * 1.7,
          y: core.height * 1.7
        }
      ];

      this.discoveredLocations =
        new Set();
    }

    update() {
      const player =
        this.player.entity;

      for (const location of this.locations) {
        if (
          this.discoveredLocations.has(
            location.id
          )
        ) {
          continue;
        }

        const distance =
          Math.hypot(
            player.x - location.x,
            player.y - location.y
          );

        if (distance < 100) {
          this.discover(location);
        }
      }
    }

    discover(location) {
      this.discoveredLocations.add(
        location.id
      );

      this.discovered++;

      this.core.addScore(200);

      this.core.notify(
        `DISCOVERED: ${location.title}`
      );

      if (
        this.discovered >=
        this.locations.length
      ) {
        this.core.win(
          "You discovered the final truth."
        );
      }
    }

    render(ctx, worldToScreen) {
      for (const location of this.locations) {
        if (
          this.discoveredLocations.has(
            location.id
          )
        ) {
          continue;
        }

        const p =
          worldToScreen(
            location.x,
            location.y
          );

        ctx.beginPath();

        ctx.arc(
          p.x,
          p.y,
          18,
          0,
          Math.PI * 2
        );

        ctx.strokeStyle =
          "#b7a9bd";

        ctx.lineWidth = 2;

        ctx.stroke();
      }
    }
  }

  global.AJVYRAAdventureGameplay =
    AJVYRAAdventureGameplay;

})(window);
