let QUEST_UI = null;


function createQuestUI(scene) {

    QUEST_UI =
        scene.add.container(
            650,
            25
        );

    const background =
        scene.add.rectangle(
            0,
            0,
            220,
            95,
            0x080808,
            0.88
        ).setOrigin(0);

    const title =
        createUIText(
            scene,
            15,
            12,
            "",
            15
        );

    const progress =
        createUIText(
            scene,
            15,
            45,
            "",
            13
        );

    QUEST_UI.add([
        background,
        title,
        progress
    ]);

    QUEST_UI.titleText = title;
    QUEST_UI.progressText = progress;

    updateQuestUI();

    return QUEST_UI;
}


function updateQuestUI() {

    if (!QUEST_UI) {
        return;
    }

    const quest =
        getQuestProgress();

    QUEST_UI.titleText.setText(
        quest.title || "NO ACTIVE QUEST"
    );

    QUEST_UI.progressText.setText(
        quest.progress +
        " / " +
        quest.target
    );
}
