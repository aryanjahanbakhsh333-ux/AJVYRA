class AJVYRAWebSpatialAudio {
    constructor(audioSystem) {
        this.audio =
            audioSystem;

        this.sources =
            new Map();
    }

    createSource(id, bufferId) {
        if (!this.audio.context) {
            return null;
        }

        const buffer =
            this.audio.buffers.get(
                String(bufferId)
            );

        if (!buffer) {
            return null;
        }

        const source =
            this.audio.context
                .createBufferSource();

        const panner =
            this.audio.context
                .createPanner();

        panner.panningModel =
            "HRTF";

        panner.distanceModel =
            "inverse";

        panner.refDistance = 1;
        panner.maxDistance = 1000;
        panner.rolloffFactor = 1;

        source.buffer = buffer;

        source.connect(panner);
        panner.connect(
            this.audio.sfxGain
        );

        this.sources.set(
            String(id),
            {
                source,
                panner
            }
        );

        return {
            source,
            panner
        };
    }

    setPosition(id, x, y, z = 0) {
        const entry =
            this.sources.get(String(id));

        if (!entry) {
            return false;
        }

        const { panner } =
            entry;

        if (panner.positionX) {
            panner.positionX.value =
                Number(x) || 0;

            panner.positionY.value =
                Number(y) || 0;

            panner.positionZ.value =
                Number(z) || 0;
        } else {
            panner.setPosition(
                Number(x) || 0,
                Number(y) || 0,
                Number(z) || 0
            );
        }

        return true;
    }

    play(id, options = {}) {
        const entry =
            this.sources.get(String(id));

        if (!entry) {
            return false;
        }

        entry.source.loop =
            Boolean(options.loop);

        entry.source.start();

        return true;
    }

    stop(id) {
        const entry =
            this.sources.get(String(id));

        if (!entry) {
            return false;
        }

        try {
            entry.source.stop();
        } catch (_) {
            // Already stopped.
        }

        this.sources.delete(
            String(id)
        );

        return true;
    }

    clear() {
        for (const id of this.sources.keys()) {
            this.stop(id);
        }
    }
}
