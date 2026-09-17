let audioEnabled = true;

function createAudioSystem(scene) {

    scene.sound.volume = 0.5;

    scene.input.once(
        "pointerdown",
        () => {

            if (
                scene.sound &&
                scene.sound.context &&
                scene.sound.context.state === "suspended"
            ) {
                scene.sound.context.resume();
            }
        }
    );
}

function toggleAudio(scene) {

    audioEnabled = !audioEnabled;

    scene.sound.mute = !audioEnabled;
}
