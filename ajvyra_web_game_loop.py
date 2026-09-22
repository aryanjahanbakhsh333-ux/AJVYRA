class AJVYRAWebGameLoop {
    constructor(options = {}) {
        this.update = typeof options.update === "function"
            ? options.update
            : () => {};

        this.render = typeof options.render === "function"
            ? options.render
            : () => {};

        this.onStart = typeof options.onStart === "function"
            ? options.onStart
            : () => {};

        this.onStop = typeof options.onStop === "function"
            ? options.onStop
            : () => {};

        this.onPause = typeof options.onPause === "function"
            ? options.onPause
            : () => {};

        this.onResume = typeof options.onResume === "function"
            ? options.onResume
            : () => {};

        this.running = false;
        this.paused = false;
        this.animationFrame = null;

        this.lastTimestamp = 0;
        this.elapsed = 0;
        this.frameCount = 0;

        this.maxDelta = 0.1;
    }

    start() {
        if (this.running) {
            return;
        }

        this.running = true;
        this.paused = false;
        this.lastTimestamp = 0;
        this.onStart();

        this.animationFrame = requestAnimationFrame(
            (timestamp) => this._frame(timestamp)
        );
    }

    stop() {
        if (!this.running) {
            return;
        }

        this.running = false;

        if (this.animationFrame !== null) {
            cancelAnimationFrame(this.animationFrame);
            this.animationFrame = null;
        }

        this.onStop();
    }

    pause() {
        if (!this.running || this.paused) {
            return;
        }

        this.paused = true;
        this.onPause();
    }

    resume() {
        if (!this.running || !this.paused) {
            return;
        }

        this.paused = false;
        this.lastTimestamp = 0;
        this.onResume();
    }

    togglePause() {
        if (this.paused) {
            this.resume();
        } else {
            this.pause();
        }
    }

    _frame(timestamp) {
        if (!this.running) {
            return;
        }

        if (this.lastTimestamp === 0) {
            this.lastTimestamp = timestamp;
        }

        let delta = (timestamp - this.lastTimestamp) / 1000;

        if (!Number.isFinite(delta) || delta < 0) {
            delta = 0;
        }

        delta = Math.min(delta, this.maxDelta);

        this.lastTimestamp = timestamp;

        if (!this.paused) {
            this.elapsed += delta;
            this.frameCount += 1;

            this.update(delta, {
                elapsed: this.elapsed,
                frameCount: this.frameCount,
            });
        }

        this.render({
            delta,
            elapsed: this.elapsed,
            frameCount: this.frameCount,
            paused: this.paused,
        });

        this.animationFrame = requestAnimationFrame(
            (nextTimestamp) => this._frame(nextTimestamp)
        );
    }

    getSnapshot() {
        return {
            running: this.running,
            paused: this.paused,
            elapsed: this.elapsed,
            frameCount: this.frameCount,
        };
    }
}

window.AJVYRAWebGameLoop = AJVYRAWebGameLoop;
