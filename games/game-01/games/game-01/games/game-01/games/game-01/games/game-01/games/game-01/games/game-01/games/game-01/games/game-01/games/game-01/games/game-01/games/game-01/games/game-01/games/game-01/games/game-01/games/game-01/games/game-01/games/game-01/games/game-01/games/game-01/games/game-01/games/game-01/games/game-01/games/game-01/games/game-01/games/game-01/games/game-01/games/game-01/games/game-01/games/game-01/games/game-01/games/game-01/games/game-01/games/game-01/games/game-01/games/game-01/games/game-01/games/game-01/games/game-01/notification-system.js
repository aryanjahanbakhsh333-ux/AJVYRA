let notificationQueue = [];

let notificationActive = false;


function notifyPlayer(
    scene,
    message,
    duration = 1800
) {

    notificationQueue.push({
        message,
        duration
    });

    processNotificationQueue(
        scene
    );
}


function processNotificationQueue(
    scene
) {

    if (
        notificationActive ||
        notificationQueue.length === 0
    ) {
        return;
    }

    notificationActive = true;

    const notification =
        notificationQueue.shift();

    const box =
        scene.add.rectangle(
            450,
            545,
            520,
            55,
            0x080808,
            0.92
        );

    const text =
        scene.add.text(
            450,
            545,
            notification.message,
            {
                fontSize: "16px",
                color: "#ffffff"
            }
        ).setOrigin(0.5);

    scene.tweens.add({

        targets: [
            box,
            text
        ],

        alpha: 0,

        duration: 300,

        delay:
            notification.duration,

        onComplete: () => {

            box.destroy();

            text.destroy();

            notificationActive =
                false;

            processNotificationQueue(
                scene
            );
        }
    });
}
