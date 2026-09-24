class EscapeRoomGame:
    GAME_ID = "AJVYRA-077"
    TITLE = "Room 404"
    GENRE = "Escape Room Puzzle"

    def __init__(self):
        self.player = "Eli Voss"
        self.solved = set()
        self.keys = 0
        self.finished = False

        self.puzzles = {
            "clock": 17,
            "painting": 42,
            "safe": 73,
        }

    def solve(self, puzzle: str, answer: int):
        if puzzle not in self.puzzles:
            return False

        if puzzle in self.solved:
            return False

        if answer != self.puzzles[puzzle]:
            return False

        self.solved.add(puzzle)
        self.keys += 1

        if self.keys >= len(self.puzzles):
            self.finished = True

        return True

    def state(self):
        return {
            "game_id": self.GAME_ID,
            "player": self.player,
            "solved": list(self.solved),
            "keys": self.keys,
            "finished": self.finished,
        }
