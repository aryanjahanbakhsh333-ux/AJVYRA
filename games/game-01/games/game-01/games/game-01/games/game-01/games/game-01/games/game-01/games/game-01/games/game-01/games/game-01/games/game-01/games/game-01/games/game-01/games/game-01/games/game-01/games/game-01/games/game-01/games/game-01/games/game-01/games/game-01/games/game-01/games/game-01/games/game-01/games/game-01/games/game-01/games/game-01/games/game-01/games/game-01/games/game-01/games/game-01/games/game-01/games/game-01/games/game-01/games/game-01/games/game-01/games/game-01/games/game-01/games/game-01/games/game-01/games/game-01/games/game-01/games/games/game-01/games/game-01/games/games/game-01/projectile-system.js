const PROJECTILES = [];


function createProjectile(
    scene,
    x,
    y,
    velocityX,
    velocityY,
    damage = 25
) {

    const projectile =
        scene.add.circle(
            x,
            y,
            6,
            0xffffff
        );

    scene.physics.add.existing(
        projectile
    );

    projectile.body.setAllowGravity(
        false
    );

    projectile.body.setVelocity(
        velocityX,
        velocityY
    );

    projectile.damage =
        damage;

    PROJECTILES.push(
        projectile
    );

    return projectile;
}


function destroyProjectile(
    projectile
) {

    if (
        projectile &&
        projectile.active
    ) {

        projectile.destroy();
    }
}


function cleanupProjectiles() {

    for (
        let i = PROJECTILES.length - 1;
        i >= 0;
        i--
    ) {

        if (
            !PROJECTILES[i] ||
            !PROJECTILES[i].active
        ) {

            PROJECTILES.splice(
                i,
                1
            );
        }
    }
}
