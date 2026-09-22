class AJVYRAWebGameAudioSystem {
    constructor(options = {}) {
        this.context = null;
        this.masterGain = null;
        this.musicGain = null;
        this.sfxGain = null;

        this.buffers = new Map();
        this.musicSource = null;

        this.masterVolume = Number(options.masterVolume) || 1;
        this.musicVolume = Number(options.musicVolume) || 0.7;
        this.sfxVolume = Number(options.sfxVolume) || 1;

        this.initialized = false;
    }

    async initialize() {
        if (this.initialized) {
            return true;
        }

        const AudioContextClass =
            window.AudioContext ||
            window.webkitAudioContext;

        if (!AudioContextClass) {
            throw new Error(
                "Web Audio API is not supported."
            );
        }

        this.context = new AudioContextClass();

        this.masterGain =
            this.context.createGain();

        this.musicGain =
            this.context.createGain();

        this.sfxGain =
            this.context.createGain();

        this.musicGain.gain.value =
            this.musicVolume;

        this.sfxGain.gain.value =
            this.sfxVolume;

        this.masterGain.gain.value =
            this.masterVolume;

        this.musicGain.connect(
            this.masterGain
        );

        this.sfxGain.connect(
            this.masterGain
        );

        this.masterGain.connect(
            this.context.destination
        );

        this.initialized = true;

        return true;
    }

    async resume() {
        await this.initialize();

        if (this.context.state === "suspended") {
            await this.context.resume();
        }
    }

    async load(id, url) {
        await this.initialize();

        const response = await fetch(url);

        if (!response.ok) {
            throw new Error(
                `Audio load failed: ${url}`
            );
        }

        const arrayBuffer =
            await response.arrayBuffer();

        const buffer =
            await this.context.decodeAudioData(
                arrayBuffer
            );

        this.buffers.set(
            String(id),
            buffer
        );

        return buffer;
    }

    playSFX(id, options = {}) {
        if (!this.initialized) {
            return null;
        }

        const buffer =
            this.buffers.get(String(id));

        if (!buffer) {
            return null;
        }

        const source =
            this.context.createBufferSource();

        const gain =
            this.context.createGain();

        const volume =
            Math.max(
                0,
                Math.min(
                    1,
                    Number(options.volume) || 1
                )
            );

        const pan =
            Math.max(
                -1,
                Math.min(
                    1,
                    Number(options.pan) || 0
                )
            );

        source.buffer = buffer;

        gain.gain.value = volume;

        source.connect(gain);

        if (this.context.createStereoPanner) {
            const panner =
                this.context.createStereoPanner();

            panner.pan.value = pan;

            gain.connect(panner);
            panner.connect(this.sfxGain);
        } else {
            gain.connect(this.sfxGain);
        }

        source.start(
            0,
            Math.max(
                0,
                Number(options.offset) || 0
            )
        );

        return source;
    }

    playMusic(id, options = {}) {
        if (!this.initialized) {
            return null;
        }

        const buffer =
            this.buffers.get(String(id));

        if (!buffer) {
            return null;
        }

        this.stopMusic();

        const source =
            this.context.createBufferSource();

        source.buffer = buffer;
        source.loop =
            options.loop !== false;

        source.connect(
            this.musicGain
        );

        source.start();

        this.musicSource = source;

        return source;
    }

    stopMusic() {
        if (!this.musicSource) {
            return;
        }

        try {
            this.musicSource.stop();
        } catch (_) {
            // Already stopped.
        }

        this.musicSource =
            null;
    }

    setMasterVolume(value) {
        this.masterVolume =
            Math.max(
                0,
                Math.min(
                    1,
                    Number(value) || 0
                )
            );

        if (this.masterGain) {
            this.masterGain.gain.value =
                this.masterVolume;
        }
    }

    setMusicVolume(value) {
        this.musicVolume =
            Math.max(
                0,
                Math.min(
                    1,
                    Number(value) || 0
                )
            );

        if (this.musicGain) {
            this.musicGain.gain.value =
                this.musicVolume;
        }
    }

    setSFXVolume(value) {
        this.sfxVolume =
            Math.max(
                0,
                Math.min(
                    1,
                    Number(value) || 0
                )
            );

        if (this.sfxGain) {
            this.sfxGain.gain.value =
                this.sfxVolume;
        }
    }
}
