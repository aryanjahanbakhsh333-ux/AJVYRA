(function (global) {
  "use strict";

  class AJVYRAFinalReleaseCertificate {
    static create(report) {
      const total = Number(report?.total || 0);
      const passed = Number(report?.passed || 0);

      const browserRuntimeVerified =
        total === 30 &&
        passed === 30 &&
        report?.complete === true;

      return Object.freeze({
        product: "AJVYRA",
        release: "FINAL",
        games: {
          required: 30,
          verified: passed,
          browserRuntimeVerified
        },
        releaseReady: browserRuntimeVerified,
        generatedAt: new Date().toISOString()
      });
    }

    static assert(report) {
      const certificate =
        AJVYRAFinalReleaseCertificate.create(report);

      if (!certificate.releaseReady) {
        throw new Error(
          `AJVYRA FINAL RELEASE BLOCKED: ${certificate.games.verified}/30 runtime verified.`
        );
      }

      return certificate;
    }
  }

  global.AJVYRAFinalReleaseCertificate =
    AJVYRAFinalReleaseCertificate;
})(window);
