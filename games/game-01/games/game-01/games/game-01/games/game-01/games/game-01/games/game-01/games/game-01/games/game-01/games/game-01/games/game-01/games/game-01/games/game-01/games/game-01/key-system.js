const KEY_STATE = {
    hasKey: false,
    keyId: null
};

function resetKeyState() {

    KEY_STATE.hasKey = false;

    KEY_STATE.keyId = null;
}

function collectKey(keyId = "main-key") {

    KEY_STATE.hasKey = true;

    KEY_STATE.keyId = keyId;
}

function hasKey(keyId = "main-key") {

    return (
        KEY_STATE.hasKey &&
        KEY_STATE.keyId === keyId
    );
}
