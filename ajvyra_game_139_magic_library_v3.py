"""
AJVYRA 139 — Magic Library
Genre: Fantasy / Knowledge Adventure
"""

from dataclasses import dataclass


@dataclass
class Book:
    title: str
    magic: int
    rarity: int
    discovered: bool = False


class MagicLibrary:
    title = "Magic Library"
    librarian = "Elya Rune"

    def __init__(self):
        self.mana = 100
        self.knowledge = 0
        self.score = 0
        self.books = [
            Book("The Ember Codex", 20, 2),
            Book("Moonlit Grammar", 35, 3),
            Book("Atlas of Forgotten Roads", 50, 5),
            Book("The Final Spellbook", 80, 10),
        ]

    def search(self, index):
        if not 0 <= index < len(self.books):
            return False

        book = self.books[index]

        if book.discovered:
            return False

        cost = book.magic // 2

        if self.mana < cost:
            return False

        self.mana -= cost
        book.discovered = True
        self.knowledge += book.magic
        self.score += book.magic * book.rarity
        return True

    def study(self, index):
        if not 0 <= index < len(self.books):
            return False

        book = self.books[index]

        if not book.discovered or self.mana < 10:
            return False

        self.mana -= 10
        self.knowledge += book.rarity * 5
        self.score += 50
        return True

    def meditate(self):
        self.mana = min(
            100,
            self.mana + 30,
        )

    def unlock_archive(self):
        return (
            self.knowledge >= 150
            and self.score >= 500
        )

    def status(self):
        return {
            "librarian": self.librarian,
            "mana": self.mana,
            "knowledge": self.knowledge,
            "score": self.score,
            "books": [
                b.title
                for b in self.books
                if b.discovered
            ],
            "archive_unlocked": self.unlock_archive(),
        }


def create_game():
    return MagicLibrary()


if __name__ == "__main__":
    game = create_game()

    for i in range(4):
        game.search(i)
        game.meditate()

    print(game.status())
