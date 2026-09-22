from dataclasses import dataclass
from typing import Iterable, List


@dataclass
class Rect:
    x: float
    y: float
    width: float
    height: float


@dataclass
class Circle:
    x: float
    y: float
    radius: float


class AJVYRACollisionSystem:
    """
    Final shared collision utilities for AJVYRA games.
    """

    @staticmethod
    def rectangles_intersect(a: Rect, b: Rect) -> bool:
        return (
            a.x < b.x + b.width
            and a.x + a.width > b.x
            and a.y < b.y + b.height
            and a.y + a.height > b.y
        )

    @staticmethod
    def circles_intersect(
        a: Circle,
        b: Circle,
    ) -> bool:

        dx = a.x - b.x
        dy = a.y - b.y

        distance_squared = (
            dx * dx +
            dy * dy
        )

        radius_sum = a.radius + b.radius

        return distance_squared <= radius_sum * radius_sum

    @staticmethod
    def circle_rectangle(
        circle: Circle,
        rectangle: Rect,
    ) -> bool:

        closest_x = max(
            rectangle.x,
            min(
                circle.x,
                rectangle.x + rectangle.width,
            ),
        )

        closest_y = max(
            rectangle.y,
            min(
                circle.y,
                rectangle.y + rectangle.height,
            ),
        )

        dx = circle.x - closest_x
        dy = circle.y - closest_y

        return (
            dx * dx +
            dy * dy
            <= circle.radius * circle.radius
        )

    @staticmethod
    def keep_inside(
        x: float,
        y: float,
        width: float,
        height: float,
        world_width: float,
        world_height: float,
    ):

        return (
            max(0, min(x, world_width - width)),
            max(0, min(y, world_height - height)),
        )

    @staticmethod
    def any_collision(
        target: Rect,
        obstacles: Iterable[Rect],
    ) -> bool:

        return any(
            AJVYRACollisionSystem.rectangles_intersect(
                target,
                obstacle,
            )
            for obstacle in obstacles
        )
