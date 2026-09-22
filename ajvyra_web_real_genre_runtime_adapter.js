(function (global) {
    "use strict";

    class AJVYRARealGenreRuntimeAdapter {
        constructor(runtime) {
            if (!runtime) {
                throw new Error("Runtime is required.");
            }

            this.runtime = runtime;
            this.bridge = null;
            this.attached = false;

            this.originalUpdate = null;
            this.originalRender = null;
        }

        attach() {
            if (this.attached) {
                return this.runtime;
            }

            const Bridge = global.AJVYRAGenreGameplayBridge;

            if (!Bridge) {
                throw new Error(
                    "AJVYRAGenreGameplayBridge is not available."
                );
            }

            this.bridge = new Bridge(this.runtime);

            this.originalUpdate = this.runtime.update;
            this.originalRender = this.runtime.render;

            const self = this;

            this.runtime.update = function (dt) {
                if (typeof self.originalUpdate === "function") {
                    self.originalUpdate.call(this, dt);
                }

                if (self.bridge && typeof self.bridge.update === "function") {
                    self.bridge.update(dt);
                }
            };

            this.runtime.render = function () {
                if (typeof self.originalRender === "function") {
                    self.originalRender.call(this);
                }

                if (self.bridge && typeof self.bridge.render === "function") {
                    self.bridge.render();
                }
            };

            this.runtime.genreBridge = this.bridge;

            this.runtime.dispatchGameAction = function (
                action,
                payload = {}
            ) {
                if (!self.bridge) {
                    return false;
                }

                return self.bridge.action(action, payload);
            };

            this.runtime.getGenreState = function () {
                if (!self.bridge) {
                    return null;
                }

                return self.bridge.getState();
            };

            this.attached = true;

            return this.runtime;
        }

        update(dt) {
            if (!this.bridge) {
                return;
            }

            this.bridge.update(dt);
        }

        render() {
            if (!this.bridge) {
                return;
            }

            this.bridge.render();
        }

        action(action, payload = {}) {
            if (!this.bridge) {
                return false;
            }

            return this.bridge.action(action, payload);
        }

        getState() {
            if (!this.bridge) {
                return null;
            }

            return this.bridge.getState();
        }

        detach() {
            if (!this.attached) {
                return;
            }

            if (this.originalUpdate) {
                this.runtime.update = this.originalUpdate;
            }

            if (this.originalRender) {
                this.runtime.render = this.originalRender;
            }

            delete this.runtime.genreBridge;
            delete this.runtime.dispatchGameAction;
            delete this.runtime.getGenreState;

            this.bridge = null;
            this.attached = false;
        }
    }

    global.AJVYRARealGenreRuntimeAdapter =
        AJVYRARealGenreRuntimeAdapter;

})(window);
