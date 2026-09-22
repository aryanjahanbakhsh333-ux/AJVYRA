"use strict";

class AJVYRAWebPhysicsCollisionResolver {
    static resolveAABB(a, b, options = {}) {
        const collision =
            AJVYRAWebCollisionSystem
                .getAABBCollisionNormal(a, b);

        if (!collision) {
            return false;
        }

        const movableA =
            options.moveA !== false;

        const movableB =
            options.moveB !== false;

        const total =
            (movableA ? 1 : 0) +
            (movableB ? 1 : 0);

        if (total === 0) {
            return false;
        }

        const depth =
            collision.depth;

        if (collision.x !== 0) {
            const direction =
                collision.x;

            if (movableA && movableB) {
                a.x +=
                    direction *
                    depth *
                    0.5;

                b.x -=
                    direction *
                    depth *
                    0.5;
            } else if (movableA) {
                a.x +=
                    direction *
                    depth;
            } else if (movableB) {
                b.x -=
                    direction *
                    depth;
            }

            if (options.bounce) {
                const bounce =
                    Math.max(
                        0,
                        Math.min(
                            1,
                            Number(
                                options.bounce
                            )
                        )
                    );

                if (movableA) {
                    a.vx =
                        -a.vx * bounce;
                }

                if (movableB) {
                    b.vx =
                        -b.vx * bounce;
                }
            }

            return true;
        }

        const direction =
            collision.y;

        if (movableA && movableB) {
            a.y +=
                direction *
                depth *
                0.5;

            b.y -=
                direction *
                depth *
                0.5;
        } else if (movableA) {
            a.y +=
                direction *
                depth;
        } else if (movableB) {
            b.y -=
                direction *
                depth;
        }

        if (
            direction < 0 &&
            movableA
        ) {
            a.grounded = true;
        }

        if (
            direction > 0 &&
            movableB
        ) {
            b.grounded = true;
        }

        if (options.bounce) {
            const bounce =
                Math.max(
                    0,
                    Math.min(
                        1,
                        Number(options.bounce)
                    )
                );

            if (movableA) {
                a.vy =
                    -a.vy * bounce;
            }

            if (movableB) {
                b.vy =
                    -b.vy * bounce;
            }
        } else {
            if (movableA && a.vy > 0) {
                a.vy = 0;
            }

            if (movableB && b.vy > 0) {
                b.vy = 0;
            }
        }

        return true;
    }

    static constrainToWorld(
        body,
        world,
        options = {}
    ) {
        let collided = false;

        if (body.left < world.left) {
            body.x = world.left;
            body.vx =
                options.bounce
                    ? Math.abs(body.vx) *
                      options.bounce
                    : 0;

            collided = true;
        }

        if (body.right > world.right) {
            body.x =
                world.right -
                body.width;

            body.vx =
                options.bounce
                    ? -Math.abs(body.vx) *
                      options.bounce
                    : 0;

            collided = true;
        }

        if (body.top < world.top) {
            body.y = world.top;

            body.vy =
                options.bounce
                    ? Math.abs(body.vy) *
                      options.bounce
                    : 0;

            collided = true;
        }

        if (body.bottom > world.bottom) {
            body.y =
                world.bottom -
                body.height;

            body.grounded = true;

            body.vy =
                options.bounce
                    ? -Math.abs(body.vy) *
                      options.bounce
                    : 0;

            if (!options.bounce) {
                body.vy = 0;
            }

            collided = true;
        }

        return collided;
    }
}


window.AJVYRAWebPhysicsCollisionResolver =
    AJVYRAWebPhysicsCollisionResolver;
