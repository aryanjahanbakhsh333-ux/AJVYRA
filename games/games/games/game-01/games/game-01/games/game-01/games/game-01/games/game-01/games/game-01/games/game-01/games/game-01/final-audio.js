class FinalAudio {
    constructor(scene) {
        this.scene = scene;
        this.enabled = true;
        this.audioContext = null;
    }

    init() {
        if (!this.enabled) return;

        try {
            this.audioContext =
                new (
                    window.AudioContext ||
                    window.webkitAudioContext
                )();
        } catch (error) {
            this.enabled = false;
        }
    }

    beep(frequency = 440, duration = 0.08) {
        if (!this.enabled || !this.audioContext) return;

        const oscillator =
            this.audioContext.createOscillator();

        const gain =
            this.audioContext.createGain();

        oscillator.frequency.value = frequency;

        gain.gain.setValueAtTime(
            0.04,
            this.audioContext.currentTime
        );

        gain.gain.exponentialRampToValueAtTime(
            0.001,
            this.audioContext.currentTime + duration
        );

        oscillator.connect(gain);
        gain.connect(this.audioContext.destination);

        oscillator.start();
        oscillator.stop(
            this.audioContext.currentTime + duration
        );
    }
}
