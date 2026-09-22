(function (global) {
    "use strict";

    class AJVYRAWebGameSiteReleaseGate {
        constructor(options = {}) {
            this.audit =
                options.audit ||
                new global.AJVYRAWeb30GameReleaseAudit();

            this.status = {
                checked: false,
                approved: false,
                report: null
            };
        }

        run() {
            const report =
                this.audit.auditAll();

            this.status = {
                checked: true,
                approved:
                    report.releaseReady,
                report
            };

            return this.status;
        }

        assert() {
            if (
                !this.status.checked
            ) {
                this.run();
            }

            if (
                !this.status.approved
            ) {
                this.audit.assertReleaseReady();
            }

            return true;
        }

        getPlayableGames() {
            if (
                !this.status.checked
            ) {
                this.run();
            }

            return this.status.report
                .failures
                .length === 0
                ? this.status.report.playable
                : 0;
        }

        getReport() {
            return this.status;
        }
    }

    global.AJVYRAWebGameSiteReleaseGate =
        AJVYRAWebGameSiteReleaseGate;

})(window);
