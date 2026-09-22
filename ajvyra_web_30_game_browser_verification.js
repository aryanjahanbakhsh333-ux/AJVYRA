(function (global) {
  "use strict";

  class AJVYRA30BrowserVerification {
    constructor(gameIds) {
      this.gameIds = [...gameIds];
      this.results = new Map();
    }

    begin(gameId) {
      if (!this.gameIds.includes(gameId)) {
        throw new Error(
          "Unknown game: " + gameId
        );
      }

      this.results.set(gameId, {
        gameId,
        launched: false,
        controlsResponded: false,
        gameplayRan: false,
        winConditionTested: false,
        loseConditionTested: false,
        landscapeTested: false,
        verified: false
      });

      return this.results.get(gameId);
    }

    record(gameId, patch) {
      const current =
        this.results.get(gameId) ||
        this.begin(gameId);

      Object.assign(current, patch);

      current.verified =
        current.launched &&
        current.controlsResponded &&
        current.gameplayRan &&
        current.winConditionTested &&
        current.loseConditionTested &&
        current.landscapeTested;

      this.results.set(gameId, current);

      return { ...current };
    }

    getReport() {
      const games = [...this.results.values()];

      return {
        total: this.gameIds.length,
        verified: games.filter(
          (game) => game.verified
        ).length,
        pending:
          this.gameIds.length -
          games.filter(
            (game) => game.verified
          ).length,
        complete:
          games.length === this.gameIds.length &&
          games.every(
            (game) => game.verified
          ),
        games
      };
    }
  }

  global.AJVYRA30BrowserVerification =
    AJVYRA30BrowserVerification;

})(window);
