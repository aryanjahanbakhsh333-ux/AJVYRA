(() => {
    "use strict";

    function AJVYRA_BootBrowserRuntime(options = {}) {
        const runtime =
            new AJVYRA_BrowserRuntime(options);

        const renderer =
            new AJVYRA_BrowserRenderer(runtime);

        const input =
            new AJVYRA_BrowserInput();

        const audio =
            new AJVYRA_BrowserAudio();

        const loader =
            new AJVYRA_BrowserLoader();

        const resize =
            new AJVYRA_BrowserResize(runtime);

        const storage =
            new AJVYRA_BrowserStorage();

        const errors =
            new AJVYRA_BrowserErrors(runtime);

        runtime.attachSystems({
            renderer,
            input,
            audio,
            loader,
            resize,
            storage,
            errors
        });

        window.AJVYRA_BROWSER = {
            runtime,
            renderer,
            input,
            audio,
            loader,
            resize,
            storage,
            errors
        };

        return window.AJVYRA_BROWSER;
    }

    window.AJVYRA_BootBrowserRuntime =
        AJVYRA_BootBrowserRuntime;

    document.addEventListener(
        "DOMContentLoaded",
        () => {
            const canvas =
                document.querySelector("#gameCanvas");

            if (!canvas) return;

            AJVYRA_BootBrowserRuntime({
                canvas
            });

            console.log(
                "AJVYRA Browser Runtime: ONLINE"
            );
        }
    );
})();
