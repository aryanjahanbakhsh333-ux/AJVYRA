const GAME_PREFERENCES = {

    vibration: true,

    sound: true,

    music: true,

    particles: true,

    showFPS: false,

    language: "en"
};


function savePreferences() {

    localStorage.setItem(
        "AJVYRA_BLACK_RUN_SETTINGS",
        JSON.stringify(
            GAME_PREFERENCES
        )
    );
}


function loadPreferences() {

    const saved =
        localStorage.getItem(
            "AJVYRA_BLACK_RUN_SETTINGS"
        );

    if (!saved) {
        return;
    }

    try {

        const data =
            JSON.parse(saved);

        Object.assign(
            GAME_PREFERENCES,
            data
        );

    } catch {

        return;
    }
}


function setPreference(
    key,
    value
) {

    if (
        !Object.prototype.hasOwnProperty
            .call(
                GAME_PREFERENCES,
                key
            )
    ) {
        return false;
    }

    GAME_PREFERENCES[key] =
        value;

    savePreferences();

    return true;
}
