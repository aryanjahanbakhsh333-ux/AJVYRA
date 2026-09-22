(function (global) {
  "use strict";

  class AJVYRATrueGameReleaseGate {
    constructor(options = {}) {
      this.options = options;

      this.gameIds =
        options.gameIds ||
        global.AJVYRAWeb30GameIds ||
        [];

      this.matrix =
        options.matrix ||
        global.AJVYRAWeb30GamePlayabilityMatrix ||
        {};
    }

    verifyGame(id, probeResult) {
      const contract = this.matrix[id];

      if (!contract) {
        return {
          id,
          releaseReady: false,
          reason: "Missing playability matrix entry."
        };
      }

      if (!probeResult) {
        return {
          id,
          releaseReady: false,
          reason: "Runtime probe did not run."
        };
      }

      if (!probeResult.ok) {
        return {
          id,
          releaseReady: false,
          reason:
            probeResult.error ||
            "Runtime probe failed."
        };
      }

      return {
        id,
        releaseReady: false,
        structuralReady: true,
        manualVerified: false,
        reason:
          "Structural runtime passed, but real browser playability has not been manually verified."
      };
    }

    run(probeResults = []) {
      const byId = new Map(
        probeResults.map((item) => [item.gameId, item])
      );

      const games = this.gameIds.map((id) =>
        this.verifyGame(id, byId.get(id))
      );

      const structuralReady = games.filter(
        (game) => game.structuralReady
      ).length;

      const manualVerified = games.filter(
        (game) => game.manualVerified
      ).length;

      const releaseReady =
        games.length === this.gameIds.length &&
        games.every((game) => game.releaseReady);

      return {
        ok: releaseReady,
        releaseReady,
        total: games.length,
        structuralReady,
        manualVerified,
        blocked: games.length - manualVerified,
        games
      };
    }
  }

  global.AJVYRATrueGameReleaseGate =
    AJVYRATrueGameReleaseGate;
})(window);
