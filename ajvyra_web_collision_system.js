"use strict";

class AJVYRAWebCollisionSystem {
    static rectRect(a, b) {
        if (!a || !b) {
            return false;
        }

        return (
            a.x < b.x + b.width &&
            a.x + a.width > b.x &&
            a.y < b.y + b.height &&
            a.y + a.height > b.y
        );
    }

    static circleCircle(a, b) {
        if (!a || !b) {
            return false;
        }

        const dx =
            a.x - b.x;

        const dy =
            a.y - b.y;

        const distanceSquared =
            dx * dx +
            dy * dy;

        const radius =
            Number(a.radius || 0) +
            Number(b.radius || 0);

        return (
            distanceSquared <
            radius * radius
        );
    }

    static circleRect(circle, rect) {
        if (!circle || !rect) {
            return false;
        }

        const closestX =
            Math.max(
                rect.x,
                Math.min(
                    circle.x,
                    rect.x + rect.width
                )
            );

        const closestY =
            Math.max(
                rect.y,
                Math.min(
                    circle.y,
                    rect.y + rect.height
                )
            );

        const dx =
            circle.x - closestX;

        const dy =
            circle.y - closestY;

        return (
            dx * dx +
            dy * dy
        ) < (
            circle.radius *
            circle.radius
        );
    }

    static pointRect(x, y, rect) {
        return (
            x >= rect.x &&
            x <= rect.x + rect.width &&
            y >= rect.y &&
            y <= rect.y + rect.height
        );
    }

    static pointCircle(x, y, circle) {
        const dx =
            x - circle.x;

        const dy =
            y - circle.y;

        return (
            dx * dx +
            dy * dy
        ) <= (
            circle.radius *
            circle.radius
        );
    }

    static getAABBOverlap(a, b) {
        if (!this.rectRect(a, b)) {
            return null;
        }

        const overlapX =
            Math.min(
                a.x + a.width,
                b.x + b.width
            ) -
            Math.max(a.x, b.x);

        const overlapY =
            Math.min(
                a.y + a.height,
                b.y + b.height
            ) -
            Math.max(a.y, b.y);

        return {
            x: overlapX,
            y: overlapY
        };
    }

    static getAABBCollisionNormal(a, b) {
        const overlap =
            this.getAABBOverlap(a, b);

        if (!overlap) {
            return null;
        }

        if (overlap.x < overlap.y) {
            return {
                x:
                    a.x < b.x
                        ? -1
                        : 1,
                y: 0,
                depth: overlap.x
            };
        }

        return {
            x: 0,
            y:
                a.y < b.y
                    ? -1
                    : 1,
            depth: overlap.y
        };
    }
}


window.AJVYRAWebCollisionSystem =
    AJVYRAWebCollisionSystem;
