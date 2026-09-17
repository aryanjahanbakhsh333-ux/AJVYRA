let scoreLabel;
let livesLabel;
let timeLabel;

function createHUD(scene) {

    scoreLabel = scene.add.text(
        25,
        25,
        "",
        {
            fontSize: "18px",
            color: "#ffffff"
        }
    );

    livesLabel = scene.add.text(
        25,
        55,
        "",
        {
            fontSize: "18px",
            color: "#ffffff"
        }
    );

    timeLabel = scene.add.text(
        25,
        85,
        "",
        {
            fontSize: "18px",
            color: "#ffffff"
        }
    );

    updateHUD();
}

function updateHUD() {

    if (scoreLabel) {
        scoreLabel.setText(
            "SCORE: " + GAME_STATE.score
        );
    }

    if (livesLabel) {
        livesLabel.setText(
            "LIVES: " + GAME_STATE.lives
        );
    }

    if (timeLabel) {
        timeLabel.setText(
            "TIME: " + GAME_STATE.time
        );
    }
}

window.updateHUD = updateHUD;
