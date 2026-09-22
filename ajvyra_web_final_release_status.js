(function (global) {
  "use strict";

  class AJVYRAFinalReleaseStatus {
    constructor(root = document.body) {
      this.root = root;
      this.badge = null;
      this.handleApproved =
        this.handleApproved.bind(this);
      this.handleBlocked =
        this.handleBlocked.bind(this);

      global.addEventListener(
        "ajvyra:final-release-approved",
        this.handleApproved
      );

      global.addEventListener(
        "ajvyra:final-release-blocked",
        this.handleBlocked
      );
    }

    mount() {
      const badge = document.createElement("div");

      badge.dataset.ajvyraReleaseStatus = "true";

      badge.style.cssText = [
        "position:relative",
        "display:inline-flex",
        "align-items:center",
        "gap:8px",
        "padding:8px 12px",
        "border:1px solid currentColor",
        "border-radius:999px",
        "font:600 12px/1 system-ui,sans-serif",
        "letter-spacing:.04em"
      ].join(";");

      badge.textContent =
        "AJVYRA • RELEASE LOCKED";

      this.root.appendChild(badge);
      this.badge = badge;

      return badge;
    }

    handleApproved(event) {
      if (!this.badge) return;

      const certificate =
        event.detail?.certificate;

      if (
        certificate?.releaseReady === true &&
        certificate.games?.verified === 30
      ) {
        this.badge.textContent =
          "AJVYRA • 30/30 PLAYABLE • FINAL";
      }
    }

    handleBlocked(event) {
      if (!this.badge) return;

      const verified =
        event.detail?.certificate?.games?.verified ?? 0;

      this.badge.textContent =
        `AJVYRA • RELEASE LOCKED • ${verified}/30`;
    }

    destroy() {
      global.removeEventListener(
        "ajvyra:final-release-approved",
        this.handleApproved
      );

      global.removeEventListener(
        "ajvyra:final-release-blocked",
        this.handleBlocked
      );

      this.badge?.remove();
      this.badge = null;
    }
  }

  global.AJVYRAFinalReleaseStatus =
    AJVYRAFinalReleaseStatus;
})(window);
