(function (global) {
  "use strict";

  class AJVYRA30GameReleaseCertificate {
    constructor(options = {}) {
      this.gameIds =
        options.gameIds ||
        global.AJVYRAWeb30GameIds ||
        [];

      this.results = [];
    }

    certify(probeReport) {
      this.results = [];

      for (const id of this.gameIds) {
        const result =
          (probeReport.results || []).find(
            (item) => item.gameId === id
          );

        const certified =
          Boolean(result && result.ok);

        this.results.push({
          id,
          runtimeConstructed:
            Boolean(result && result.runtimeConstructed),
          updateExecuted:
            Boolean(result && result.updateExecuted),
          renderExecuted:
            Boolean(result && result.renderExecuted),
          structuralCertified: certified,

          /*
           * This remains false until a real browser
           * gameplay verification report is supplied.
           */
          humanPlayableCertified: false,

          releaseCertified: false
        });
      }

      const structuralCount =
        this.results.filter(
          (item) => item.structuralCertified
        ).length;

      return {
        total: this.results.length,
        structuralCertified: structuralCount,
        humanPlayableCertified: 0,
        releaseCertified: 0,

        /*
         * Deliberately false until the 30-game
         * browser verification stage passes.
         */
        finalRelease: false,

        games: this.results
      };
    }
  }

  global.AJVYRA30GameReleaseCertificate =
    AJVYRA30GameReleaseCertificate;

})(window);
