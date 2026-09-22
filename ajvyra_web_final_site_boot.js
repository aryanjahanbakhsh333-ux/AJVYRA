(function (global) {
  "use strict";

  async function bootAJVYRAFinalSite(options = {}) {
    if (
      typeof global.AJVYRAFinal30GameRunner !== "function"
    ) {
      throw new Error(
        "AJVYRAFinal30GameRunner is missing."
      );
    }

    const runner =
      new global.AJVYRAFinal30GameRunner(options);

    const report = await runner.runAll();

    if (
      typeof global.AJVYRAFinalReleaseCertificate !==
      "function"
    ) {
      throw new Error(
        "AJVYRAFinalReleaseCertificate is missing."
      );
    }

    const certificate =
      global.AJVYRAFinalReleaseCertificate.create(
        report
      );

    if (!certificate.releaseReady) {
      global.dispatchEvent(
        new CustomEvent(
          "ajvyra:final-release-blocked",
          {
            detail: {
              report,
              certificate
            }
          }
        )
      );

      return {
        released: false,
        report,
        certificate
      };
    }

    global.dispatchEvent(
      new CustomEvent(
        "ajvyra:final-release-approved",
        {
          detail: {
            report,
            certificate
          }
        }
      )
    );

    return {
      released: true,
      report,
      certificate
    };
  }

  global.bootAJVYRAFinalSite =
    bootAJVYRAFinalSite;
})(window);
