(() => {
    "use strict";

    class AJVYRA_BrowserAudio {
        constructor() {
            this.context = null;
            this.master = null;
            this.muted = false;
        }

        unlock() {
            if (!this.context) {
                const AudioContext =
                    window.AudioContext ||
                    window.webkitAudioContext;

                if (!AudioContext) return;

                this.context = new AudioContext();

                this.master =
                    this.context.createGain();

                this.master.gain.value = 0.25;

                this.master.connect(
                    this.context.destination
                );
            }

            if (this.context.state === "suspended") {
                this.context.resume();
            }
        }

        tone(
            frequency = 440,
            duration = 0.08,
            type = "sine"
        ) {
            if (this.muted) return;

            this.unlock();

            if (!this.context || !this.master) return;

            const oscillator =
                this.context.createOscillator();

            const gain =
                this.context.createGain();

            oscillator.type = type;
            oscillator.frequency.value = frequency;

            gain.gain.setValueAtTime(
                0.0001,
                this.context.currentTime
            );

            gain.gain.exponentialRampToValueAtTime(
                0.15,
                this.context.currentTime + 0.01
            );

            gain.gain.exponentialRampToValueAtTime(
                0.0001,
                this.context.currentTime + duration
            );

            oscillator.connect(gain);
            gain.connect(this.master);

            oscillator.start();
            oscillator.stop(
                this.context.currentTime + duration
            );
        }

        mute() {
            this.muted = true;
        }

        unmute() {
            this.muted = false;
        }

        pause() {}

        resume() {
            this.unlock();
        }

        stop() {}

        destroy() {
            if (this.context) {
                this.context.close();
            }

            this.context = null;
            this.master = null;
        }
    }

    window.AJVYRA_BrowserAudio = AJVYRA_BrowserAudio;
})();
