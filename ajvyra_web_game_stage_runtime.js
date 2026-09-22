(function (global) {
    "use strict";

    class AJVYRAWebGameStageRuntime {
        constructor(runtime, profile) {
            this.runtime = runtime;
            this.profile = profile;

            this.stageIndex = 0;
            this.stageStarted = false;

            this.stageTime = 0;
            this.stageScore = 0;

            this.completed = new Set();

            this.stageDefinitions =
                (profile.stages || []).map(
                    (id, index) => ({
                        id,
                        index,
                        title:
                            this.makeTitle(id),
                        target:
                            this.makeTarget(
                                profile,
                                id
                            )
                    })
                );
        }

        makeTitle(id) {
            return String(id)
                .split("_")
                .map(
                    word =>
                        word.charAt(0).toUpperCase() +
                        word.slice(1)
                )
                .join(" ");
        }

        makeTarget(profile, stageId) {
            const genre =
                profile.genre[0];

            const targets = {
                action:
                    "Reach the next objective.",
                racing:
                    "Reach the next checkpoint.",
                fighting:
                    "Win the current round.",
                rpg:
                    "Complete the current quest.",
                survival:
                    "Survive the current wave.",
                shooter:
                    "Eliminate the hostile threat.",
                horror:
                    "Find a way forward.",
                strategy:
                    "Secure the objective.",
                puzzle:
                    "Solve the current puzzle.",
                adventure:
                    "Discover the next location.",
                boss:
                    "Damage the boss and survive."
            };

            return targets[genre] ||
                "Complete the objective.";
        }

        start() {
            this.stageIndex = 0;
            this.stageStarted = true;
            this.stageTime = 0;
            this.stageScore = 0;

            this.syncCore();

            return this.getCurrentStage();
        }

        update(dt) {
            if (!this.stageStarted) {
                return;
            }

            dt = Math.min(
                Math.max(dt || 0, 0),
                0.05
            );

            this.stageTime += dt;

            this.syncCore();
        }

        syncCore() {
            const core =
                this.runtime &&
                this.runtime.core;

            if (!core) {
                return;
            }

            const stage =
                this.getCurrentStage();

            core.currentStage =
                this.stageIndex;

            core.stageTitle =
                stage ? stage.title : "";

            core.stageObjective =
                stage ? stage.target : "";

            core.stageTime =
                this.stageTime;
        }

        getCurrentStage() {
            return (
                this.stageDefinitions[
                    this.stageIndex
                ] || null
            );
        }

        completeStage(result = {}) {
            if (!this.stageStarted) {
                return false;
            }

            const stage =
                this.getCurrentStage();

            if (!stage) {
                return false;
            }

            this.completed.add(
                stage.id
            );

            this.stageScore +=
                Number(result.score || 0);

            if (
                this.stageIndex >=
                this.stageDefinitions.length - 1
            ) {
                this.finish();
                return true;
            }

            this.stageIndex += 1;
            this.stageTime = 0;

            this.syncCore();

            const core =
                this.runtime &&
                this.runtime.core;

            if (core) {
                core.state = "playing";
            }

            return true;
        }

        finish() {
            this.stageStarted = false;

            const core =
                this.runtime &&
                this.runtime.core;

            if (core) {
                core.campaignFinished = true;
                core.state = "won";
            }
        }

        render(ctx) {
            if (!ctx) {
                return;
            }

            const stage =
                this.getCurrentStage();

            if (!stage) {
                return;
            }

            ctx.save();

            ctx.fillStyle =
                "rgba(0,0,0,0.70)";

            ctx.fillRect(
                18,
                205,
                330,
                82
            );

            ctx.fillStyle =
                "#ffffff";

            ctx.font =
                "bold 16px Arial";

            ctx.fillText(
                `STAGE ${this.stageIndex + 1}/${this.stageDefinitions.length}`,
                32,
                230
            );

            ctx.font =
                "13px Arial";

            ctx.fillText(
                stage.title,
                32,
                252
            );

            ctx.fillText(
                stage.target,
                32,
                274
            );

            ctx.restore();
        }

        getState() {
            return {
                index: this.stageIndex,
                total:
                    this.stageDefinitions.length,
                stage:
                    this.getCurrentStage(),
                time: this.stageTime,
                score: this.stageScore,
                completed:
                    [...this.completed]
            };
        }
    }

    global.AJVYRAWebGameStageRuntime =
        AJVYRAWebGameStageRuntime;

})(window);
