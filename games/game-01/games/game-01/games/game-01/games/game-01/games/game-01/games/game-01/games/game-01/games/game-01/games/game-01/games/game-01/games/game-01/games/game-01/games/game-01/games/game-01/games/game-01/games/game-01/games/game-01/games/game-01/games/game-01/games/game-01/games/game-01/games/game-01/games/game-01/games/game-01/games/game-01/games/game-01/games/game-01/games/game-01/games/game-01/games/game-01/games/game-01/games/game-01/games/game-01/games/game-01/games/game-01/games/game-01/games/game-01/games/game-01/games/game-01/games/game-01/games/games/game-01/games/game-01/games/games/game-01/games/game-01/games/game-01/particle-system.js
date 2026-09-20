function createHitParticles(
    scene,
    x,
    y
) {

    const particles = [];

    for (
        let i = 0;
        i < 10;
        i++
    ) {

        const particle =
            scene.add.circle(
                x,
                y,
                Phaser.Math.Between(
                    2,
                    5
                ),
                0xffffff
            );

        const angle =
            Phaser.Math.FloatBetween(
                0,
                Math.PI * 2
            );

        const distance =
            Phaser.Math.Between(
                25,
                70
            );

        particles.push(
            particle
        );

        scene.tweens.add({

            targets: particle,

            x:
                x +
                Math.cos(angle) *
                distance,

            y:
                y +
                Math.sin(angle) *
                distance,

            alpha: 0,

            duration: 450,

            onComplete: () => {

                particle.destroy();
            }
        });
    }

    return particles;
}


function createCollectParticle(
    scene,
    x,
    y
) {

    const particle =
        scene.add.circle(
            x,
            y,
            8,
            0xffffff
        );

    scene.tweens.add({

        targets: particle,

        scale: 2.5,

        alpha: 0,

        duration: 350,

        onComplete: () => {

            particle.destroy();
        }
    });
}
