const MISSION_STATE = {
    active: false,
    completed: false,
    title: "",
    description: ""
};

function startMission(
    title,
    description
) {

    MISSION_STATE.active = true;

    MISSION_STATE.completed = false;

    MISSION_STATE.title = title;

    MISSION_STATE.description =
        description;
}

function completeMission() {

    MISSION_STATE.completed = true;

    MISSION_STATE.active = false;
}

function getMissionStatus() {

    return {
        active: MISSION_STATE.active,
        completed: MISSION_STATE.completed,
        title: MISSION_STATE.title,
        description: MISSION_STATE.description
    };
}
