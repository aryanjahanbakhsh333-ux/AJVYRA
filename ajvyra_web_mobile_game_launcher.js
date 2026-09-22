(function (global) {
    "use strict";

    class AJVYRAMobileGameLauncher {
        constructor(options = {}) {
            this.mount =
                options.mount || document.body;

            this.catalog =
                options.catalog ||
                global.AJVYRAWeb30GameCatalog;

            this.active = null;
        }

        resolve(id) {
            if (
                global.AJVYRAWeb30UniqueGameProfiles
            ) {
                const profile =
                    global.AJVYRAWeb30UniqueGameProfiles
                        .get(id);

                if (!profile) {
                    return null;
                }

                return profile;
            }

            return null;
        }

        async launch(id) {
            const profile =
                this.resolve(id);

            if (!profile) {
                throw new Error(
                    `Game ${id} has no unique profile.`
                );
            }

            const root =
                document.createElement("div");

            root.className =
                "ajvyra-mobile-game-runtime";

            root.style.position =
                "relative";

            root.style.width =
                "100%";

            root.style.minHeight =
                "100%";

            root.style.background =
                "#050507";

            this.mount.appendChild(root);

            const shell =
                new global.AJVYRALandscapeGameShell({
                    root
                });

            await shell.prepare();

            const storyHost =
                document.createElement("div");

            root.appendChild(
                storyHost
            );

            const controlHost =
                document.createElement("div");

            controlHost.style.position =
                "absolute";

            controlHost.style.left =
                "20px";

            controlHost.style.right =
                "20px";

            controlHost.style.bottom =
                "20px";

            controlHost.style.display =
                "flex";

            controlHost.style.flexWrap =
                "wrap";

            controlHost.style.gap =
                "10px";

            controlHost.style.justifyContent =
                "center";

            root.appendChild(
                controlHost
            );

            const story =
                new global.AJVYRAWebGameStoryRuntime(
                    profile,
                    storyHost
                );

            const controls =
                new global.AJVYRAUniqueGameControls(
                    profile,
                    controlHost
                );

            const bridge =
                new global.AJVYRAUniqueGameRuntimeBridge({
                    gameId: id,
                    controls,
                    story
                });

            story.start();

            this.active = {
                id,
                profile,
                root,
                shell,
                story,
                controls,
                bridge
            };

            return this.active;
        }

        async close() {
            if (!this.active) {
                return;
            }

            await this.active.shell.exit();

            this.active.controls.destroy();
            this.active.shell.destroy();

            this.active.root.remove();

            this.active = null;
        }
    }

    global.AJVYRAMobileGameLauncher =
        AJVYRAMobileGameLauncher;

})(window);
