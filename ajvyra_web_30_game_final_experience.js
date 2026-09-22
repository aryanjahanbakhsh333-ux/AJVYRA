(function (global) {
    "use strict";

    class AJVYRA30GameFinalExperience {
        constructor(runtime, gameId) {
            if (!runtime) {
                throw new Error(
                    "Runtime is required."
                );
            }

            if (
                !global.AJVYRA30GameExperienceRegistry
            ) {
                throw new Error(
                    "Game experience registry unavailable."
                );
            }

            const profile =
                global.AJVYRA30GameExperienceRegistry
                    .get(gameId);

            if (!profile) {
                throw new Error(
                    `Unknown AJVYRA game: ${gameId}`
                );
            }

            this.runtime = runtime;
            this.gameId = gameId;
            this.profile = profile;

            this.stageRuntime = null;
            this.mechanics = null;
            this.story = null;
            this.started = false;

            this.originalUpdate =
                runtime.update;

            this.originalRender =
                runtime.render;
        }

        initialize() {
            this.createStageRuntime();
            this.createMechanics();
            this.createStory();

            this.installRuntimeHooks();

            return this;
        }

        createStageRuntime() {
            if (
                !global.AJVYRAWebGameStageRuntime
            ) {
                return;
            }

            this.stageRuntime =
                new global.AJVYRAWebGameStageRuntime(
                    this.runtime,
                    this.profile
                );
        }

        createMechanics() {
            if (
                !global.AJVYRA30GameUniqueMechanics
            ) {
                return;
            }

            this.mechanics =
                global.AJVYRA30GameUniqueMechanics
                    .create(
                        this.runtime,
                        this.profile
                    );
        }

        createStory() {
            const Database =
                global.AJVYRA30GameStoryDatabase;

            const StoryRuntime =
                global.AJVYRAStoryChoiceRuntime;

            if (
                !Database ||
                !StoryRuntime
            ) {
                return;
            }

            const story =
                Database.get(
                    this.gameId
                );

            if (!story) {
                return;
            }

            this.story =
                new StoryRuntime(
                    this.runtime,
                    story
                );
        }

        installRuntimeHooks() {
            const self = this;

            this.runtime.update =
                function (dt) {
                    if (
                        typeof self.originalUpdate ===
                        "function"
                    ) {
                        self.originalUpdate.call(
                            this,
                            dt
                        );
                    }

                    self.update(dt);
                };

            this.runtime.render =
                function () {
                    if (
                        typeof self.originalRender ===
                        "function"
                    ) {
                        self.originalRender.call(
                            this
                        );
                    }

                    self.render();
                };

            this.runtime.finalExperience =
                this;
        }

        start() {
            if (this.started) {
                return false;
            }

            this.started = true;

            if (this.stageRuntime) {
                this.stageRuntime.start();
            }

            if (this.story) {
                this.story.start();
            }

            const core =
                this.runtime.core;

            if (core) {
                core.state =
                    core.state === "lost"
                        ? "playing"
                        : core.state || "playing";

                core.gameId =
                    this.gameId;

                core.gameTitle =
                    this.profile.title;

                core.gameGenre =
                    [...this.profile.genre];

                core.gameObjective =
                    this.profile.objective;
            }

            return true;
        }

        update(dt) {
            if (!this.started) {
                return;
            }

            this.stageRuntime?.update(dt);
            this.mechanics?.update(dt);

            const core =
                this.runtime.core;

            if (!core) {
                return;
            }

            if (
                core.state === "won" &&
                this.stageRuntime
            ) {
                const completed =
                    this.stageRuntime.completeStage({
                        score:
                            core.score || 0
                    });

                if (
                    completed &&
                    !core.campaignFinished
                ) {
                    core.state =
                        "playing";
                }
            }
        }

        render() {
            const ctx =
                this.runtime.renderer?.ctx ||
                this.runtime.ctx ||
                null;

            if (!ctx) {
                return;
            }

            this.drawIdentity(ctx);

            this.stageRuntime?.render(ctx);
            this.mechanics?.render(ctx);
        }

        drawIdentity(ctx) {
            const width =
                ctx.canvas.width;

            ctx.save();

            ctx.fillStyle =
                "rgba(0,0,0,.72)";

            ctx.fillRect(
                width - 350,
                18,
                330,
                48
            );

            ctx.fillStyle =
                "#ffffff";

            ctx.font =
                "bold 15px Arial";

            ctx.textAlign =
                "right";

            ctx.fillText(
                this.profile.title,
                width - 35,
                39
            );

            ctx.font =
                "11px Arial";

            ctx.fillText(
                this.profile.genre
                    .join(" / ")
                    .toUpperCase(),
                width - 35,
                56
            );

            ctx.restore();
        }

        action(action, payload = {}) {
            if (
                this.mechanics?.action(
                    action,
                    payload
                )
            ) {
                return true;
            }

            if (
                action === "storyChoice" &&
                this.story
            ) {
                return this.story.choose(
                    payload.index
                );
            }

            if (
                action === "completeStage" &&
                this.stageRuntime
            ) {
                return this.stageRuntime.completeStage(
                    payload
                );
            }

            return false;
        }

        getState() {
            return {
                id: this.gameId,
                profile: this.profile,

                stage:
                    this.stageRuntime
                        ?.getState() || null,

                mechanics:
                    this.mechanics
                        ?.getState() || null,

                story:
                    this.story
                        ?.getState() || null
            };
        }
    }

    global.AJVYRA30GameFinalExperience =
        AJVYRA30GameFinalExperience;

})(window);
