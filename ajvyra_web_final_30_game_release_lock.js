(function (global) {
  "use strict";

  class AJVYRAFinal30GameReleaseLock {
    constructor(gameIds) {
      this.gameIds = [...gameIds];
    }

    evaluate(browserReport) {
      const games =
        browserReport.games || [];

      const verified =
        games.filter(
          (game) => game.verified === true
        );

      const missing =
        this.gameIds.filter(
          (id) =>
            !games.some(
              (game) =>
                game.gameId === id &&
                game.verified === true
            )
        );

      const unlocked =
        this.gameIds.length === 30 &&
        verified.length === 30 &&
        missing.length === 0;

      const result = {
        totalGames: this.gameIds.length,
        verifiedGames: verified.length,
        missingGames: missing.length,
        missing,
        releaseUnlocked: unlocked,

        badge: unlocked
          ? "AJVYRA 30/30 PLAYABLE"
          : "AJVYRA RELEASE LOCKED"
      };

      if (!unlocked) {
        window.dispatchEvent(
          new CustomEvent(
            "ajvyra:30-game-release-blocked",
            { detail: result }
          )
        );
      } else {
        window.dispatchEvent(
          new CustomEvent(
            "ajvyra:30-game-release-approved",
            { detail: result }
          )
        );
      }

      return result;
    }
  }

  global.AJVYRAFinal30GameReleaseLock =
    AJVYRAFinal30GameReleaseLock;

})(window);
