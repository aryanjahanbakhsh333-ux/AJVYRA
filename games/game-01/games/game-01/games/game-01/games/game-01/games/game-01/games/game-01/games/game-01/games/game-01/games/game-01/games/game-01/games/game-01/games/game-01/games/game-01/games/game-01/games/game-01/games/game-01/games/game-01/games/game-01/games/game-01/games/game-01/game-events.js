const GAME_EVENTS = {
    COIN_COLLECTED: "coin-collected",
    ENEMY_DEFEATED: "enemy-defeated",
    PLAYER_DAMAGED: "player-damaged",
    CHECKPOINT_REACHED: "checkpoint-reached",
    KEY_COLLECTED: "key-collected",
    DOOR_OPENED: "door-opened",
    MISSION_COMPLETED: "mission-completed",
    LEVEL_COMPLETED: "level-completed",
    PLAYER_DIED: "player-died"
};


function emitGameEvent(scene, eventName, data = {}) {

    if (!scene || !scene.events) {
        return;
    }

    scene.events.emit(
        eventName,
        data
    );
}
