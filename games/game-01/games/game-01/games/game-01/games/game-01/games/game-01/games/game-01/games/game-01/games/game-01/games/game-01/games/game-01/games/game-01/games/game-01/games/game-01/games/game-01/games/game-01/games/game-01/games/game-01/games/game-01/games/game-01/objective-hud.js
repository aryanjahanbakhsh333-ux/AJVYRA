let objectiveLabel;

function createObjectiveHUD(scene) {

    objectiveLabel =
        scene.add.text(
            25,
            155,
            "",
            {
                fontSize: "15px",
                color: "#aaaaaa",
                lineSpacing: 6
            }
        );

    updateObjectiveHUD();
}

function updateObjectiveHUD() {

    if (!objectiveLabel) {
        return;
    }

    const objective =
        getLevelObjective(
            LEVEL_MANAGER.currentLevel
        );

    objectiveLabel.setText(
        "OBJECTIVE\n" +
        objective.objectiveText +
        "\nCORES: " +
        LEVEL_PROGRESS.coins +
        "/" +
        objective.requiredCoins
    );
}
