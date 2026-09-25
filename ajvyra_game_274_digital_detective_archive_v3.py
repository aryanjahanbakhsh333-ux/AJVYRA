from dataclasses import dataclass


@dataclass
class ArchiveFile:
    name: str
    encryption: int
    importance: int
    unlocked: bool = False


class DigitalDetectiveArchive:
    def __init__(self):
        self.detective = "Iris Knox"
        self.focus = 100
        self.intel = 0
        self.score = 0
        self.files_unlocked = 0
        self.case_solved = False

        self.files = [
            ArchiveFile("Blue Signal", 30, 40),
            ArchiveFile("Night Protocol", 50, 70),
            ArchiveFile("Ghost Account", 70, 100),
            ArchiveFile("Final Archive", 90, 150),
        ]

    def scan_file(self, index: int):
        if not 0 <= index < len(self.files):
            return False

        if self.focus < 10:
            return False

        self.focus -= 10
        file = self.files[index]
        file.encryption = max(0, file.encryption - 15)
        self.score += 20
        return True

    def analyze_pattern(self):
        if self.focus < 15:
            return False

        self.focus -= 15
        self.intel += 20
        self.score += 40
        return True

    def unlock_file(self, index: int):
        if not 0 <= index < len(self.files):
            return False

        file = self.files[index]

        if file.unlocked or self.intel < file.encryption:
            return False

        file.unlocked = True
        self.files_unlocked += 1
        self.intel += file.importance // 5
        self.score += file.importance
        return True

    def recover_focus(self):
        self.focus = min(100, self.focus + 35)

    def solve_case(self):
        if self.files_unlocked >= 4:
            self.case_solved = True
            self.score += 400
            return True

        return False

    def status(self):
        return {
            "detective": self.detective,
            "focus": self.focus,
            "intel": self.intel,
            "files_unlocked": self.files_unlocked,
            "score": self.score,
            "case_solved": self.case_solved,
        }


def create_game():
    return DigitalDetectiveArchive()


if __name__ == "__main__":
    game = create_game()
    game.scan_file(0)
    game.scan_file(0)
    game.analyze_pattern()
    print(game.status())
