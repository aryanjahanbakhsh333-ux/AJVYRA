class AJVYRAWebGamePresentationSystem {
    constructor(options = {}) {
        this.audio =
            options.audio ||
            new AJVYRAWebGameAudioSystem();

        this.vfx =
            options.vfx ||
            new AJVYRAWebGameVFXSystem();

        this.camera =
            options.camera ||
            new AJVYRAWebAdvancedCamera();

        this.spatialAudio =
            options.spatialAudio ||
            new AJVYRAWebSpatialAudio(
                this.audio
            );

        this.lastDelta = 0;
    }

    async initializeAudio() {
        return this.audio.initialize();
    }

    update(delta, viewport = {}) {
        this.lastDelta = delta;

        this.vfx.update(delta);

        this.camera.update(
            Number(viewport.width) || 1280,
            Number(viewport.height) || 720,
            delta
        );

        const shake =
            this.vfx.getShakeOffset();

        this.camera.applyShake(
            shake.x,
            shake.y
        );
    }

    playSFX(id, options = {}) {
        return this.audio.playSFX(
            id,
            options
        );
    }

    playMusic(id, options = {}) {
        return this.audio.playMusic(
            id,
            options
        );
    }

    hitEffect(x, y, options = {}) {
        const effect =
            this.vfx.hit(
                x,
                y,
                options
            );

        if (options.shake !== false) {
            this.vfx.shake({
                duration:
                    options.shakeDuration || 160,

                strength:
                    options.shakeStrength || 3
            });
        }

        if (options.flash) {
            this.vfx.flash({
                duration:
                    options.flashDuration || 80,

                strength:
                    options.flashStrength || 0.25
            });
        }

        return effect;
    }

    explosion(x, y, options = {}) {
        const effect =
            this.vfx.explosion(
                x,
                y,
                options
            );

        this.vfx.shake({
            duration:
                options.shakeDuration || 300,

            strength:
                options.shakeStrength || 7
        });

        return effect;
    }

    setCameraTarget(target) {
        this.camera.follow(
            target
        );
    }

    setCameraZoom(zoom) {
        this.camera.setZoom(
            zoom
        );
    }

    getCamera() {
        return this.camera;
    }

    getActiveEffects() {
        return this.vfx.getActiveEffects();
    }

    getFlashStrength() {
        return this.vfx.getFlashStrength();
    }
}
