(function (global) {
    "use strict";

    class AJVYRAMultiStageGameCampaign {
        constructor(runtime, stages = []) {
            this.runtime = runtime;

            this.stages =
                Array.isArray(stages)
                    ? stages
                    : [];

            this.currentStage = 0;
            this.completedStages = [];
            this.checkpoints = {};

            this.started = false;
            this.finished = false;
        }

        start() {
            if (this.stages.length === 0) {
                return false;
            }

            this.started = true;
            this.finished = false;

            this.currentStage = 0;

            return true;
        }

        getStage() {
            return (
                this.stages[
                    this.currentStage
                ] || null
            );
        }

        completeStage(result = {}) {
            if (!this.started || this.finished) {
                return false;
            }

            const stage =
                this.getStage();

            if (!stage) {
                return false;
            }

            this.completedStages.push({
                id:
                    stage.id ||
                    `stage-${this.currentStage + 1}`,
                result: {
                    ...result
                }
            });

            this.saveCheckpoint();

            if (
                this.currentStage >=
                this.stages.length - 1
            ) {
                this.finishCampaign();
                return true;
            }

            this.currentStage += 1;

            this.onStageChanged();

            return true;
        }

        failStage() {
            const stage =
                this.getStage();

            if (!stage) {
                return false;
            }

            if (stage.retry !== false) {
                return true;
            }

            const core =
                this.runtime &&
                this.runtime.core;

            if (core) {
                core.state = "lost";
            }

            return false;
        }

        saveCheckpoint() {
            this.checkpoints[
                this.currentStage
            ] = {
                stage:
                    this.currentStage,
                timestamp:
                    Date.now()
            };
        }

        loadCheckpoint(index) {
            if (
                index < 0 ||
                index >= this.stages.length
            ) {
                return false;
            }

            this.currentStage = index;

            return true;
        }

        onStageChanged() {
            const core =
                this.runtime &&
                this.runtime.core;

            if (!core) {
                return;
            }

            core.currentStage =
                this.currentStage;

            core.stageTitle =
                this.getStage()?.title ||
                "";
        }

        finishCampaign() {
            this.finished = true;
            this.started = false;

            const core =
                this.runtime &&
                this.runtime.core;

            if (core) {
                core.campaignFinished =
                    true;

                core.state = "won";
            }
        }

        getProgress() {
            return {
                currentStage:
                    this.currentStage + 1,

                totalStages:
                    this.stages.length,

                completed:
                    this.completedStages.length,

                percentage:
                    this.stages.length === 0
                        ? 0
                        : Math.round(
                            (
                                this.completedStages.length /
                                this.stages.length
                            ) * 100
                        ),

                finished:
                    this.finished
            };
        }

        getState() {
            return {
                ...this.getProgress(),
                stage:
                    this.getStage(),
                completedStages:
                    [...this.completedStages]
            };
        }
    }

    global.AJVYRAMultiStageGameCampaign =
        AJVYRAMultiStageGameCampaign;

})(window);
