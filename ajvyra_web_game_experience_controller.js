(function (global) {
    "use strict";

    class AJVYRAWebGameExperienceController {
        constructor(runtime, options = {}) {
            if (!runtime) {
                throw new Error(
                    "Runtime is required."
                );
            }

            this.runtime = runtime;

            this.gameId =
                options.gameId ||
                runtime.gameId ||
                runtime.options?.gameId ||
                "";

            this.genreRuntime = null;
            this.storyRuntime = null;
            this.campaign = null;

            this.started = false;
        }

        initialize() {
            this.attachGenreRuntime();
            this.attachStoryRuntime();
            this.createCampaign();

            return this;
        }

        attachGenreRuntime() {
            if (
                !global.AJVYRACompleteGenreRuntime
            ) {
                return;
            }

            this.genreRuntime =
                new global.AJVYRACompleteGenreRuntime(
                    this.runtime
                );

            this.genreRuntime.attach();
        }

        attachStoryRuntime() {
            if (
                !global.AJVYRAStoryChoiceRuntime ||
                !global.AJVYRA30GameStoryDatabase
            ) {
                return;
            }

            const story =
                global.AJVYRA30GameStoryDatabase.get(
                    this.gameId
                );

            if (!story) {
                return;
            }

            this.storyRuntime =
                new global.AJVYRAStoryChoiceRuntime(
                    this.runtime,
                    story
                );
        }

        createCampaign() {
            if (
                !global.AJVYRAMultiStageGameCampaign
            ) {
                return;
            }

            const stages =
                this.createStages();

            this.campaign =
                new global.AJVYRAMultiStageGameCampaign(
                    this.runtime,
                    stages
                );
        }

        createStages() {
            return [
                {
                    id: "awakening",
                    title: "Awakening",
                    objective: "Discover the threat.",
                    retry: true
                },
                {
                    id: "confrontation",
                    title: "Confrontation",
                    objective: "Face the first major enemy.",
                    retry: true
                },
                {
                    id: "descent",
                    title: "Descent",
                    objective: "Enter the deeper zone.",
                    retry: true
                },
                {
                    id: "revelation",
                    title: "Revelation",
                    objective: "Discover the truth.",
                    retry: true
                },
                {
                    id: "finale",
                    title: "Finale",
                    objective: "Decide the fate of the world.",
                    retry: true
                }
            ];
        }

        start() {
            if (this.started) {
                return false;
            }

            this.started = true;

            if (this.campaign) {
                this.campaign.start();
            }

            if (this.storyRuntime) {
                this.storyRuntime.start();
            }

            const core =
                this.runtime.core;

            if (core) {
                core.currentStage = 0;
                core.campaignFinished = false;
                core.storyFinished = false;
            }

            return true;
        }

        chooseStory(index) {
            if (!this.storyRuntime) {
                return false;
            }

            return this.storyRuntime.choose(index);
        }

        completeCurrentStage(result = {}) {
            if (!this.campaign) {
                return false;
            }

            return this.campaign.completeStage(
                result
            );
        }

        action(action, payload = {}) {
            if (
                this.genreRuntime &&
                this.genreRuntime.action(
                    action,
                    payload
                )
            ) {
                return true;
            }

            if (action === "storyChoice") {
                return this.chooseStory(
                    payload.index
                );
            }

            if (action === "completeStage") {
                return this.completeCurrentStage(
                    payload
                );
            }

            return false;
        }

        update(dt) {
            if (!this.started) {
                return;
            }

            const core =
                this.runtime.core;

            if (!core) {
                return;
            }

            if (
                core.state === "won" &&
                this.campaign &&
                !this.campaign.finished
            ) {
                this.completeCurrentStage({
                    score:
                        core.score || 0
                });

                if (!this.campaign.finished) {
                    core.state = "playing";
                }
            }
        }

        getState() {
            return {
                gameId: this.gameId,
                started: this.started,

                genre:
                    this.genreRuntime
                        ? this.genreRuntime.getState()
                        : {},

                story:
                    this.storyRuntime
                        ? this.storyRuntime.getState()
                        : null,

                campaign:
                    this.campaign
                        ? this.campaign.getState()
                        : null
            };
        }
    }

    global.AJVYRAWebGameExperienceController =
        AJVYRAWebGameExperienceController;

})(window);
