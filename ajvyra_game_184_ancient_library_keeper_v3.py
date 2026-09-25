from dataclasses import dataclass
from typing import List


@dataclass
class AncientBook:
    title: str
    category: str
    rarity: int
    restored: bool = False


class AncientLibraryKeeper:
    def __init__(self):
        self.keeper = "Eren Vale"
        self.energy = 100
        self.knowledge = 0
        self.score = 0
        self.books: List[AncientBook] = [
            AncientBook("The First Map", "History", 3),
            AncientBook("Stars Before Dawn", "Astronomy", 5),
            AncientBook("The Silent Equation", "Mathematics", 4),
            AncientBook("Garden of Symbols", "Language", 2),
        ]

    def restore_book(self, title: str):
        for book in self.books:
            if book.title == title and not book.restored:
                if self.energy < book.rarity * 5:
                    return False

                self.energy -= book.rarity * 5
                book.restored = True
                self.knowledge += book.rarity * 10
                self.score += book.rarity * 20
                return True

        return False

    def study_category(self, category: str):
        amount = sum(
            book.rarity
            for book in self.books
            if book.category == category and book.restored
        )

        self.knowledge += amount * 5
        self.score += amount * 10
        return amount

    def organize(self):
        self.books.sort(key=lambda book: (book.category, book.title))
        self.score += 20
        return True

    def rest(self):
        self.energy = min(100, self.energy + 30)

    def status(self):
        return {
            "keeper": self.keeper,
            "energy": self.energy,
            "knowledge": self.knowledge,
            "score": self.score,
            "restored_books": sum(b.restored for b in self.books),
            "library": [
                {
                    "title": b.title,
                    "category": b.category,
                    "restored": b.restored,
                }
                for b in self.books
            ],
        }


def create_game():
    return AncientLibraryKeeper()


def demo():
    game = create_game()
    game.restore_book("The First Map")
    game.restore_book("Stars Before Dawn")
    game.organize()
    game.study_category("History")
    return game.status()


if __name__ == "__main__":
    print(demo())
