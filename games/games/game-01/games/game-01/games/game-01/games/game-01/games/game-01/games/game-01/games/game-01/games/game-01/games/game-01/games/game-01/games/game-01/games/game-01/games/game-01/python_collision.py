class CollisionSystem:

    @staticmethod
    def resolve_vertical(
        player,
        platforms,
        velocity_y
    ):

        on_ground = False

        for platform in platforms:

            if player.colliderect(platform):

                if velocity_y > 0:

                    player.bottom = platform.top

                    velocity_y = 0

                    on_ground = True

                elif velocity_y < 0:

                    player.top = platform.bottom

                    velocity_y = 0

        return velocity_y, on_ground

    @staticmethod
    def inside_world(
        rect,
        world_width,
        world_height
    ):

        rect.x = max(
            0,
            min(
                rect.x,
                world_width - rect.width
            )
        )

        return rect.y <= world_height
