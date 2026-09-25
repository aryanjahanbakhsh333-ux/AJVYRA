from dataclasses import dataclass


@dataclass
class Book:
    title: str
    knowledge: int
    rarity: int
    restored: bool = False


class AncientLibraryKeeper:
    def __init__(self):
        self.keeper = "Sera Quill"
        self.energy = 100
        self.reputation = 20
        self.coins = 150
        self.score = 0
        self.knowledge = 0

        self.books = [
            Book("Atlas of Stars", 40, 20),
            Book("Lost Kingdoms", 60, 35),
            Book("Mechanical Codex", 80, 50),
            Book("Book of First Dawn", 120, 90),
        ]

    def restore_book(self, index: int):
        if not 0 <= index < len(self.books):
            return False

        book = self.books[index]

        if book.restored or self.energy < 15:
            return False

        self.energy -= 15
        book.restored = True
        self.knowledge += book.knowledge
        self.score += book.rarity
        return True

    def study(self, index: int):
        if not 0 <= index < len(self.books):
            return False

        book = self.books[index]

        if not book.restored or self.energy < 10:
            return False

        self.energy -= 10
        self.knowledge += book.knowledge
        self.score += book.knowledge
        return True

    def host_lecture(self):
        if self.knowledge < 100:
            return False

        self.reputation += 15
        self.coins += self.knowledge // 5
        self.score += 80
        return True

    def rest(self):
        self.energy = min(100, self.energy + 35)

    def status(self):
        return {
            "keeper": self.keeper,
            "energy": self.energy,
            "knowledge": self.knowledge,
            "reputation": self.reputation,
            "coins": self.coins,
            "score": self.score,
            "restored_books": sum(
                book.restored for book in self.books
            ),
        }


def create_game():
    return AncientLibraryKeeper()


if __name__ == "__main__":
    game = create_game()
    game.restore_book(0)
    game.study(0)
    game.host_lecture()
    print(game.status())
