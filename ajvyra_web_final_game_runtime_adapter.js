/* AJVYRA — Final Game Runtime Adapter
 * New file.
 */

class AJVYRAWebFinalGameRuntimeAdapter {

    constructor(runtime, gameId) {
        if (!runtime) {
            throw new Error("AJVYRA runtime is required.");
        }

        this.runtime = runtime;
        this.gameId = gameId;

        this.profile =
            globalThis.AJVYRA30GameExperienceRegistry?.get(gameId) ||
            null;

        this.story =
            globalThis.AJVYRA30GameStoryDatabase?.get(gameId) ||
            null;

        this.experience = null;
        this.storyRuntime = null;

        this.attached = false;
        this.started = false;
    }

    attach() {
        if (this.attached) {
            return this;
        }

        if (!this.profile) {
            throw new Error(
                `Unknown AJVYRA game: ${this.gameId}`
            );
        }

        if (
            globalThis.AJVYRA30GameFinalExperience
        ) {
            this.experience =
                new globalThis.AJVYRA30GameFinalExperience(
                    this.runtime,
                    this.gameId
                );
        }

        if (
            this.story &&
            globalThis.AJVYRAStoryChoiceRuntime
        ) {
            this.storyRuntime =
                new globalThis.AJVYRAStoryChoiceRuntime(
                    this.story
                );

            this.storyRuntime.on(
                "story-finished",
                event => {
                    this.runtime.storyEnding = event.ending;

                    this.runtime.storyComplete = true;

                    this.runtime.runtimeEvents?.push?.({
                        type: "story-finished",
                        gameId: this.gameId,
                        reason: event.reason
                    });
                }
            );
        }

        this.runtime.finalGameAdapter = this;

        this.runtime.dispatchGameAction = action => {
            return this.action(action);
        };

        this.attached = true;

        return this;
    }

    start() {
        if (!this.attached) {
            this.attach();
        }

        if (this.experience) {
            try {
                this.experience.initialize();
            } catch (error) {
                console.warn(
                    "[AJVYRA] Final experience initialize:",
                    error
                );
            }

            try {
                this.experience.start();
            } catch (error) {
                console.warn(
                    "[AJVYRA] Final experience start:",
                    error
                );
            }
        }

        if (this.storyRuntime) {
            this.storyRuntime.start();
        }

        this.started = true;

        return this;
    }

    update(dt) {
        if (!this.started) {
            return;
        }

        if (
            this.experience &&
            typeof this.experience.update === "function"
        ) {
            this.experience.update(dt);
        }

        if (
            this.storyRuntime &&
            this.runtime.core?.state === "won"
        ) {
            this.storyRuntime.completeCurrentChapter();
        }
    }

    render(ctx) {
        if (
            this.experience &&
            typeof this.experience.render === "function"
        ) {
            this.experience.render(ctx);
        }
    }

    action(action, payload = {}) {
        if (!action) {
            return false;
        }

        if (action === "story-next") {
            return this.storyRuntime?.advanceDialogue() || false;
        }

        if (action.startsWith("choice:")) {
            const choiceId = action.slice("choice:".length);

            return (
                this.storyRuntime?.choose(choiceId) ||
                false
            );
        }

        if (action === "story-complete") {
            return (
                this.storyRuntime?.completeCurrentChapter() ||
                false
            );
        }

        if (
            this.experience &&
            typeof this.experience.action === "function"
        ) {
            return this.experience.action(
                action,
                payload
            );
        }

        return false;
    }

    getState() {
        return {
            gameId: this.gameId,
            profile: this.profile,
            story: this.storyRuntime?.getState?.() || null,
            runtime:
                this.runtime.getState?.() ||
                this.runtime.state ||
                null,
            started: this.started
        };
    }

    stop() {
        try {
            this.runtime.stop?.();
        } catch (error) {
            console.warn("[AJVYRA] Runtime stop:", error);
        }

        this.started = false;
    }
}

globalThis.AJVYRAWebFinalGameRuntimeAdapter =
    AJVYRAWebFinalGameRuntimeAdapter;
