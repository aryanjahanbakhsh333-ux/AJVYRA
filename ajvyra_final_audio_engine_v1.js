export class AJVYRAAudioEngine {
    constructor() {
        this.context = null;
        this.enabled = true;
    }

    init() {
        if (this.context) return;

        const AudioContext =
            window.AudioContext ||
            window.webkitAudioContext;

        if (!AudioContext) {
            this.enabled = false;
            return;
        }

        this.context = new AudioContext();
    }

    beep(frequency = 440, duration = 0.08, type = "sine") {
        if (!this.enabled) return;

        this.init();

        if (!this.context) return;

        if (this.context.state === "suspended") {
            this.context.resume();
        }

        const oscillator = this.context.createOscillator();
        const gain = this.context.createGain();

        oscillator.type = type;
        oscillator.frequency.value = frequency;

        gain.gain.setValueAtTime(
            0.0001,
            this.context.currentTime
        );

        gain.gain.exponentialRampToValueAtTime(
            0.12,
            this.context.currentTime + 0.01
        );

        gain.gain.exponentialRampToValueAtTime(
            0.0001,
            this.context.currentTime + duration
        );

        oscillator.connect(gain);
        gain.connect(this.context.destination);

        oscillator.start();
        oscillator.stop(this.context.currentTime + duration);
    }

    action() {
        this.beep(520, 0.06, "square");
    }

    complete() {
        this.beep(660, 0.08);
        setTimeout(() => this.beep(880, 0.12), 90);
    }
}
