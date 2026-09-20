class LevelManager:

    def __init__(self):
        self.current_level = 1

        self.levels = {
            1: {
                "name": "THE FIRST SHADOW",
                "orbs": 8,
                "enemies": 7
            },

            2: {
                "name": "DEAD SIGNAL",
                "orbs": 10,
                "enemies": 10
            },

            3: {
                "name": "BLACK HORIZON",
                "orbs": 12,
                "enemies": 14
            }
        }

    def get_current(self):
        return self.levels[
            self.current_level
        ]

    def complete_level(self):

        if self.current_level < len(
            self.levels
        ):

            self.current_level += 1

            return True

        return False

    def reset(self):
        self.current_level = 1
