class Camera:

    def __init__(
        self,
        screen_width,
        world_width
    ):

        self.screen_width = screen_width

        self.world_width = world_width

        self.x = 0

    def update(self, target):

        target_x = (
            target.centerx -
            self.screen_width // 2
        )

        self.x = max(
            0,
            min(
                target_x,
                self.world_width -
                self.screen_width
            )
        )

    def apply(self, rect):

        return rect.move(
            -int(self.x),
            0
        )

    def x_position(self, x):

        return int(x - self.x)
