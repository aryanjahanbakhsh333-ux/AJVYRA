"""
AJVYRA 159 — Secret Library Mystery
Genre: Mystery / Puzzle
"""

from dataclasses import dataclass


@dataclass
class BookClue:
    title: str
    code: str
    discovered: bool = False


class SecretLibraryMystery:
    title = "Secret Library Mystery"
    detective = "Iris Quill"

    def __init__(self):
        self.focus = 100
        self.score = 0
        self.clues = [
            BookClue(
                "The Silver Atlas",
                "NORTH",
            ),
            BookClue(
                "The Empty Crown",
                "SEVEN",
            ),
            BookClue(
                "The Midnight Bell",
                "MOON",
            ),
            BookClue(
                "The Last Manuscript",
                "314",
            ),
        ]

        self.answer = []
        self.solved = False

    def inspect(self, book_title):
        book = next(
            (
                b for b in self.clues
                if b.title == book_title
            ),
            None,
        )

        if book is None or book.discovered:
            return False

        if self.focus < 15:
            return False

        self.focus -= 15
        book.discovered = True
        self.answer.append(book.code)
        self.score += 100
        return True

    def think(self):
        self.focus = min(
            100,
            self.focus + 25,
        )

    def solve(self, sequence):
        if not all(
            clue.discovered
            for clue in self.clues
        ):
            return False

        if sequence == [
            "NORTH",
            "SEVEN",
            "MOON",
            "314",
        ]:
            self.solved = True
            self.score += 1000
            return True

        self.score = max(
            0,
            self.score - 100,
        )
        return False

    def status(self):
        return {
            "detective": self.detective,
            "focus": self.focus,
            "score": self.score,
            "clues_found": len(self.answer),
            "solved": self.solved,
        }


def create_game():
    return SecretLibraryMystery()


if __name__ == "__main__":
    game = create_game()

    for clue in game.clues:
        game.inspect(clue.title)

    game.solve([
        "NORTH",
        "SEVEN",
        "MOON",
        "314",
    ])

    print(game.status())
