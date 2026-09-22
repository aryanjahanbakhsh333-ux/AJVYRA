(function (global) {
    "use strict";

    class AJVYRACompleteGenreRuntime {
        constructor(runtime) {
            if (!runtime) {
                throw new Error("Runtime is required.");
            }

            this.runtime = runtime;

            this.systems = {
                action: null,
                fighting: null,
                survival: null,
                boss: null
            };

            this.attached = false;
            this.originalUpdate = null;
            this.originalRender = null;
        }

        attach() {
            if (this.attached) {
                return this.runtime;
            }

            this.createSystems();

            this.originalUpdate = this.runtime.update;
            this.originalRender = this.runtime.render;

            const self = this;

            this.runtime.update = function (dt) {
                if (typeof self.originalUpdate === "function") {
                    self.originalUpdate.call(this, dt);
                }

                self.updateSystems(dt);
            };

            this.runtime.render = function () {
                if (typeof self.originalRender === "function") {
                    self.originalRender.call(this);
                }

                self.renderSystems();
            };

            this.runtime.completeGenreSystems = this.systems;

            this.runtime.genreAction = function (
                action,
                payload = {}
            ) {
                return self.action(action, payload);
            };

            this.attached = true;

            return this.runtime;
        }

        createSystems() {
            const gameId =
                this.runtime.gameId ||
                this.runtime.options?.gameId ||
                "";

            const genre =
                this.resolveGenre(gameId);

            if (
                genre === "action" ||
                genre === "action-fighting"
            ) {
                if (global.AJVYRAActionGameplay) {
                    this.systems.action =
                        new global.AJVYRAActionGameplay(
                            this.runtime
                        );
                }
            }

            if (
                genre === "fighting" ||
                genre === "action-fighting"
            ) {
                if (global.AJVYRAFightingGameplay) {
                    this.systems.fighting =
                        new global.AJVYRAFightingGameplay(
                            this.runtime
                        );
                }
            }

            if (
                genre === "survival" ||
                genre === "survival-horror"
            ) {
                if (global.AJVYRASurvivalGameplay) {
                    this.systems.survival =
                        new global.AJVYRASurvivalGameplay(
                            this.runtime
                        );
                }
            }

            if (
                genre === "boss"
            ) {
                if (global.AJVYRABossGameplay) {
                    this.systems.boss =
                        new global.AJVYRABossGameplay(
                            this.runtime
                        );
                }
            }
        }

        resolveGenre(gameId) {
            const fighting = [
                "void-arena",
                "shadow-duel",
                "bladefall"
            ];

            const survival = [
                "night-hunt",
                "frostbound",
                "wildfire",
                "last-fortress"
            ];

            const boss = [
                "titan-core"
            ];

            const action = [
                "shadow-runner",
                "sky-raiders",
                "pulse-breaker",
                "zero-hour"
            ];

            if (fighting.includes(gameId)) {
                return "fighting";
            }

            if (survival.includes(gameId)) {
                return "survival";
            }

            if (boss.includes(gameId)) {
                return "boss";
            }

            if (action.includes(gameId)) {
                return "action";
            }

            return "action";
        }

        updateSystems(dt) {
            for (const key of Object.keys(this.systems)) {
                const system = this.systems[key];

                if (
                    system &&
                    typeof system.update === "function"
                ) {
                    system.update(dt);
                }
            }
        }

        renderSystems() {
            const ctx =
                this.runtime.renderer?.ctx ||
                this.runtime.ctx ||
                null;

            if (!ctx) {
                return;
            }

            for (const key of Object.keys(this.systems)) {
                const system = this.systems[key];

                if (
                    system &&
                    typeof system.render === "function"
                ) {
                    system.render(ctx);
                }
            }
        }

        action(action, payload = {}) {
            let handled = false;

            for (const key of Object.keys(this.systems)) {
                const system = this.systems[key];

                if (
                    system &&
                    typeof system.action === "function"
                ) {
                    const result =
                        system.action(
                            action,
                            payload
                        );

                    if (result) {
                        handled = true;
                    }
                }
            }

            return handled;
        }

        getState() {
            const state = {};

            for (const key of Object.keys(this.systems)) {
                const system = this.systems[key];

                if (
                    system &&
                    typeof system.getState === "function"
                ) {
                    state[key] =
                        system.getState();
                }
            }

            return state;
        }

        detach() {
            if (!this.attached) {
                return;
            }

            if (this.originalUpdate) {
                this.runtime.update =
                    this.originalUpdate;
            }

            if (this.originalRender) {
                this.runtime.render =
                    this.originalRender;
            }

            delete this.runtime.completeGenreSystems;
            delete this.runtime.genreAction;

            this.attached = false;
        }
    }

    global.AJVYRACompleteGenreRuntime =
        AJVYRACompleteGenreRuntime;

})(window);
