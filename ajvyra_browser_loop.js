(() => {
    "use strict";

    class AJVYRA_BrowserLoop {
        constructor(runtime) {
            this.runtime = runtime;

            this.running = false;
            this.paused = false;

            this.last = 0;
            this.frame = 0;

            this.targetFPS = 60;
            this.frameTime = 1000 / 60;

            this.raf = null;
        }

        start() {
            if (this.running) return;

            this.running = true;
            this.paused = false;
            this.last = performance.now();

            this.raf = requestAnimationFrame(
                this.tick.bind(this)
            );
        }

        tick(now) {
            if (!this.running) return;

            let elapsed = now - this.last;

            if (elapsed < 0) elapsed = 0;

            this.last = now;

            if (!this.paused) {
                const dt = Math.min(elapsed / 1000, 0.05);

                this.runtime.update(dt);
                this.runtime.render();

                this.frame++;
            }

            this.raf = requestAnimationFrame(
                this.tick.bind(this)
            );
        }

        pause() {
            this.paused = true;
        }

        resume() {
            this.paused = false;
            this.last = performance.now();
        }

        stop() {
            this.running = false;

            if (this.raf !== null) {
                cancelAnimationFrame(this.raf);
                this.raf = null;
            }
        }
    }

    window.AJVYRA_BrowserLoop = AJVYRA_BrowserLoop;
})();
