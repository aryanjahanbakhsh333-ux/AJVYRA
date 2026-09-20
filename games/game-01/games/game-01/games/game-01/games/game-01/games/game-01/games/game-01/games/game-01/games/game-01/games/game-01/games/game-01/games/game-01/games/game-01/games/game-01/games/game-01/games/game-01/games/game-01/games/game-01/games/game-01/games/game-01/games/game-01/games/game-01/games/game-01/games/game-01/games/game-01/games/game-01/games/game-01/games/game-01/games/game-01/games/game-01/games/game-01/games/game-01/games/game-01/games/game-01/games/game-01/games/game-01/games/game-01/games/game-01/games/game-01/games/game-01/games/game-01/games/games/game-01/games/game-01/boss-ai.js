function updateBossAI(
    scene,
    boss
) {

    if (
        !boss ||
        !boss.active ||
        !player ||
        !BOSS_STATE.active
    ) {
        return;
    }

    const distance =
        Phaser.Math.Distance.Between(
            boss.x,
            boss.y,
            player.x,
            player.y
        );

    if (distance > 220) {

        if (
            player.x < boss.x
        ) {

            boss.body.setVelocityX(
                -90
            );

        } else {

            boss.body.setVelocityX(
                90
            );
        }

    } else {

        boss.body.setVelocityX(0);

        bossAttack(
            scene,
            boss
        );
    }
}


function bossAttack(
    scene,
    boss
) {

    if (
        boss.attackCooldown
    ) {
        return;
    }

    boss.attackCooldown = true;

    const distance =
        Phaser.Math.Distance.Between(
            boss.x,
            boss.y,
            player.x,
            player.y
        );

    if (distance <= 150) {

        handlePlayerDamage(
            scene,
            player,
            boss
        );
    }

    scene.time.delayedCall(
        1200,
        () => {

            boss.attackCooldown = false;
        }
    );
}
