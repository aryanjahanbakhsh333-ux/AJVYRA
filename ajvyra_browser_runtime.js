(() => {
    "use strict";

    class AJVYRA_BrowserRuntime {
        constructor(options = {}) {
            this.canvas =
                options.canvas ||
                document.querySelector(options.canvasSelector || "#gameCanvas");

            if (!this.canvas) {
                throw new Error("AJVYRA: game canvas not found.");
            }

            this.ctx = this.canvas.getContext("2d", {
                alpha: false,
                desynchronized: true
            });

            if (!this.ctx) {
                throw new Error("AJVYRA: Canvas 2D context unavailable.");
            }

            this.game = null;
            this.running = false;
            this.paused = false;
            this.destroyed = false;

            this.time = 0;
            this.deltaTime = 0;
            this.frame = 0;
            this.fps = 60;

            this.maxDelta = 0.05;

            this.input = null;
            this.audio = null;
            this.renderer = null;
            this.resizeManager = null;
            this.storage = null;
            this.loader = null;
            this.errors = null;

            this.onStart = options.onStart || null;
            this.onStop = options.onStop || null;
            this.onPause = options.onPause || null;
            this.onResume = options.onResume || null;

            this._raf = null;
            this._lastTime = 0;

            window.AJVYRA_RUNTIME = this;
        }

        attachSystems(systems = {}) {
            this.input = systems.input || null;
            this.audio = systems.audio || null;
            this.renderer = systems.renderer || null;
            this.resizeManager = systems.resize || null;
            this.storage = systems.storage || null;
            this.loader = systems.loader || null;
            this.errors = systems.errors || null;

            return this;
        }

        async load(gameDefinition) {
            if (!gameDefinition) {
                throw new Error("AJVYRA: invalid game definition.");
            }

            this.stop();

            this.game = gameDefinition;

            if (this.loader?.load) {
                await this.loader.load(gameDefinition);
            }

            if (typeof this.game.initialize === "function") {
                await this.game.initialize(this);
            }

            this.frame = 0;
            this.time = 0;
            this.deltaTime = 0;
            this.destroyed = false;

            return this;
        }

        start() {
            if (!this.game) {
                throw new Error("AJVYRA: no game loaded.");
            }

            if (this.running) return;

            this.running = true;
            this.paused = false;
            this._lastTime = performance.now();

            this.onStart?.(this);

            this._raf = requestAnimationFrame(
                this._tick.bind(this)
            );
        }

        _tick(timestamp) {
            if (!this.running || this.destroyed) return;

            let dt = (timestamp - this._lastTime) / 1000;

            if (!Number.isFinite(dt)) {
                dt = 0;
            }

            dt = Math.min(dt, this.maxDelta);

            this._lastTime = timestamp;
            this.deltaTime = dt;
            this.time += dt;
            this.frame++;

            if (!this.paused) {
                this.update(dt);
                this.render();
            }

            this._raf = requestAnimationFrame(
                this._tick.bind(this)
            );
        }

        update(dt) {
            try {
                this.input?.update?.(dt);

                if (typeof this.game.update === "function") {
                    this.game.update(dt, this);
                }
            } catch (error) {
                this.errors?.handle?.(error, "update");
            }
        }

        render() {
            try {
                if (this.renderer?.beginFrame) {
                    this.renderer.beginFrame();
                }

                if (typeof this.game.render === "function") {
                    this.game.render(this);
                }

                if (this.renderer?.endFrame) {
                    this.renderer.endFrame();
                }
            } catch (error) {
                this.errors?.handle?.(error, "render");
            }
        }

        pause() {
            if (!this.running || this.paused) return;

            this.paused = true;

            this.audio?.pause?.();
            this.game?.onPause?.(this);

            this.onPause?.(this);
        }

        resume() {
            if (!this.running || !this.paused) return;

            this.paused = false;
            this._lastTime = performance.now();

            this.audio?.resume?.();
            this.game?.onResume?.(this);

            this.onResume?.(this);
        }

        togglePause() {
            this.paused ? this.resume() : this.pause();
        }

        restart() {
            if (!this.game) return;

            const currentGame = this.game;

            this.stop();
            this.game = currentGame;

            if (typeof this.game.initialize === "function") {
                Promise.resolve(this.game.initialize(this))
                    .then(() => this.start());
            } else {
                this.start();
            }
        }

        stop() {
            if (this._raf !== null) {
                cancelAnimationFrame(this._raf);
                this._raf = null;
            }

            const wasRunning = this.running;

            this.running = false;
            this.paused = false;

            if (this.game?.destroy) {
                try {
                    this.game.destroy(this);
                } catch (error) {
                    this.errors?.handle?.(error, "destroy");
                }
            }

            this.audio?.stop?.();

            if (wasRunning) {
                this.onStop?.(this);
            }
        }

        destroy() {
            this.stop();

            this.destroyed = true;

            this.input?.destroy?.();
            this.audio?.destroy?.();
            this.resizeManager?.destroy?.();
        }

        getSize() {
            return {
                width: this.canvas.clientWidth || this.canvas.width,
                height: this.canvas.clientHeight || this.canvas.height
            };
        }
    }

    window.AJVYRA_BrowserRuntime = AJVYRA_BrowserRuntime;
})();
