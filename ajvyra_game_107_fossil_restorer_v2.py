"""
AJVYRA Game 107 - Fossil Restorer
Genre: Restoration Puzzle
"""

from dataclasses import dataclass


@dataclass
class FossilPiece:
    piece_id: int
    correct_slot: int
    rotation: int = 0
    placed: bool = False


class FossilRestorer:
    title = "Fossil Restorer"
    character = "Dr. Arin Foss"

    def __init__(self):
        self.score = 0
        self.attempts = 0
        self.pieces = [
            FossilPiece(1, 0),
            FossilPiece(2, 1),
            FossilPiece(3, 2),
            FossilPiece(4, 3),
            FossilPiece(5, 4),
            FossilPiece(6, 5),
        ]

    def rotate(self, piece_id):
        piece = self._find(piece_id)

        if piece is None or piece.placed:
            return False

        piece.rotation = (piece.rotation + 90) % 360
        self.attempts += 1
        return True

    def place(self, piece_id, slot):
        piece = self._find(piece_id)

        if piece is None:
            return False

        self.attempts += 1

        if piece.correct_slot == slot and piece.rotation == 0:
            piece.placed = True
            self.score += 50
            return True

        self.score = max(0, self.score - 5)
        return False

    def _find(self, piece_id):
        for piece in self.pieces:
            if piece.piece_id == piece_id:
                return piece
        return None

    def completed(self):
        return all(piece.placed for piece in self.pieces)

    def snapshot(self):
        return {
            "restorer": self.character,
            "score": self.score,
            "attempts": self.attempts,
            "completed": self.completed(),
            "pieces": [
                {
                    "id": p.piece_id,
                    "slot": p.correct_slot,
                    "rotation": p.rotation,
                    "placed": p.placed,
                }
                for p in self.pieces
            ],
        }


def create_game():
    return FossilRestorer()


if __name__ == "__main__":
    game = create_game()

    for piece_id in range(1, 7):
        game.place(piece_id, piece_id - 1)

    print(game.snapshot())
