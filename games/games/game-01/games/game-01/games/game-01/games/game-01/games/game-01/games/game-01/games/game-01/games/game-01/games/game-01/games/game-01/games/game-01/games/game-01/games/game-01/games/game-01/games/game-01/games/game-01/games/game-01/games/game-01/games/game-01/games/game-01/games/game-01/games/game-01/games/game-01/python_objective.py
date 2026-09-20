class ObjectiveSystem:

    def __init__(self, total_orbs):

        self.total_orbs = total_orbs

        self.collected = 0

        self.exit_unlocked = False

    def collect(self):

        self.collected += 1

        if self.collected >= self.total_orbs:

            self.exit_unlocked = True

    def completed(self):

        return self.exit_unlocked

    def progress(self):

        return (
            self.collected,
            self.total_orbs
        )
