const QUEST_STATE = {

    id: null,

    title: "",

    description: "",

    target: 0,

    progress: 0,

    completed: false
};


function createQuest(
    id,
    title,
    description,
    target
) {

    QUEST_STATE.id = id;

    QUEST_STATE.title = title;

    QUEST_STATE.description =
        description;

    QUEST_STATE.target = target;

    QUEST_STATE.progress = 0;

    QUEST_STATE.completed = false;
}


function advanceQuest(amount = 1) {

    if (
        QUEST_STATE.completed ||
        QUEST_STATE.target <= 0
    ) {
        return;
    }

    QUEST_STATE.progress =
        Math.min(
            QUEST_STATE.target,
            QUEST_STATE.progress + amount
        );

    if (
        QUEST_STATE.progress >=
        QUEST_STATE.target
    ) {

        QUEST_STATE.completed = true;

        completeMission();
    }
}


function getQuestProgress() {

    return {

        title:
            QUEST_STATE.title,

        description:
            QUEST_STATE.description,

        progress:
            QUEST_STATE.progress,

        target:
            QUEST_STATE.target,

        completed:
            QUEST_STATE.completed
    };
}
