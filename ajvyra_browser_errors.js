(() => {
    "use strict";

    class AJVYRA_BrowserErrors {
        constructor(runtime) {
            this.runtime = runtime;
            this.lastError = null;
            this.errorCount = 0;

            window.addEventListener(
                "error",
                event => {
                    this.handle(
                        event.error ||
                        new Error(event.message),
                        "window"
                    );
                }
            );

            window.addEventListener(
                "unhandledrejection",
                event => {
                    this.handle(
                        event.reason ||
                        new Error("Unhandled rejection"),
                        "promise"
                    );
                }
            );
        }

        handle(error, source = "unknown") {
            this.lastError = {
                error,
                source,
                time: Date.now()
            };

            this.errorCount++;

            console.error(
                `[AJVYRA ${source}]`,
                error
            );

            if (
                this.errorCount >= 10 &&
                this.runtime
            ) {
                this.runtime.pause();
            }
        }

        reset() {
            this.lastError = null;
            this.errorCount = 0;
        }
    }

    window.AJVYRA_BrowserErrors =
        AJVYRA_BrowserErrors;
})();
