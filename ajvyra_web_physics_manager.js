"use strict";

class AJVYRAWebPhysicsManager {
    constructor(options = {}) {
        this.world =
            new AJVYRAWebPhysicsWorld(options);

        this.staticBodies = new Set();
        this.dynamicBodies = new Set();

        this.collisionListeners =
            new Set();

        this.worldBounds =
            options.worldBounds || null;
    }

    addDynamic(body) {
        this.world.addBody(body);
        this.dynamicBodies.add(body);

        return body;
    }

    addStatic(body) {
        body.dynamic = false;

        this.world.addBody(body);
        this.staticBodies.add(body);

        return body;
    }

    remove(body) {
        this.world.removeBody(body);

        this.dynamicBodies.delete(body);
        this.staticBodies.delete(body);
    }

    onCollision(callback) {
        if (typeof callback !== "function") {
            throw new TypeError(
                "Collision listener must be a function."
            );
        }

        this.collisionListeners.add(
            callback
        );

        return () => {
            this.collisionListeners.delete(
                callback
            );
        };
    }

    step(delta) {
        for (const body of this.dynamicBodies) {
            body.grounded = false;
        }

        this.world.step(delta);

        this.resolveDynamicVsStatic();
        this.resolveDynamicVsDynamic();

        if (this.worldBounds) {
            for (const body of this.dynamicBodies) {
                const collided =
                    AJVYRAWebPhysicsCollisionResolver
                        .constrainToWorld(
                            body,
                            this.worldBounds,
                            {
                                bounce: 0
                            }
                        );

                if (collided) {
                    this.emitCollision({
                        type: "world-boundary",
                        body
                    });
                }
            }
        }
    }

    resolveDynamicVsStatic() {
        for (const dynamicBody of this.dynamicBodies) {
            for (const staticBody of this.staticBodies) {
                if (
                    !AJVYRAWebCollisionSystem.rectRect(
                        dynamicBody,
                        staticBody
                    )
                ) {
                    continue;
                }

                const resolved =
                    AJVYRAWebPhysicsCollisionResolver
                        .resolveAABB(
                            dynamicBody,
                            staticBody,
                            {
                                moveA: true,
                                moveB: false,
                                bounce: 0
                            }
                        );

                if (resolved) {
                    this.emitCollision({
                        type: "body-static",
                        bodyA: dynamicBody,
                        bodyB: staticBody
                    });
                }
            }
        }
    }

    resolveDynamicVsDynamic() {
        const bodies =
            Array.from(this.dynamicBodies);

        for (
            let i = 0;
            i < bodies.length;
            i += 1
        ) {
            for (
                let j = i + 1;
                j < bodies.length;
                j += 1
            ) {
                const a = bodies[i];
                const b = bodies[j];

                if (
                    !AJVYRAWebCollisionSystem.rectRect(
                        a,
                        b
                    )
                ) {
                    continue;
                }

                const resolved =
                    AJVYRAWebPhysicsCollisionResolver
                        .resolveAABB(
                            a,
                            b,
                            {
                                moveA: true,
                                moveB: true,
                                bounce: 0
                            }
                        );

                if (resolved) {
                    this.emitCollision({
                        type: "body-body",
                        bodyA: a,
                        bodyB: b
                    });
                }
            }
        }
    }

    emitCollision(event) {
        for (
            const listener
            of this.collisionListeners
        ) {
            listener(event);
        }
    }

    clear() {
        this.world.clear();

        this.staticBodies.clear();
        this.dynamicBodies.clear();
        this.collisionListeners.clear();
    }
}


window.AJVYRAWebPhysicsManager =
    AJVYRAWebPhysicsManager;
