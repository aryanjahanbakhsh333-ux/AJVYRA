"""
AJVYRA 178 — Neon Chess Duel
Genre: Chess / Strategy
"""

from dataclasses import dataclass


@dataclass
class ChessPiece:
    kind: str
    power: int


class NeonChessDuel:
    title = "Neon Chess Duel"
    player = "Axiom"

    def __init__(self):
        self.turn = 1
        self.energy = 100
        self.score = 0
        self.captured = []

        self.board_power = {
            "pawn": 10,
            "knight": 30,
            "bishop": 30,
            "rook": 50,
            "queen": 90,
            "king": 100,
        }

        self.player_pieces = [
            ChessPiece("king", 100),
            ChessPiece("queen", 90),
            ChessPiece("rook", 50),
            ChessPiece("bishop", 30),
            ChessPiece("knight", 30),
            ChessPiece("pawn", 10),
        ]

    def calculate_move(self, piece, target_value):
        if self.energy < 5:
            return False

        piece_power = self.board_power.get(
            piece,
            0,
        )

        if piece_power == 0:
            return False

        self.energy -= 5

        advantage = (
            piece_power - target_value
        )

        if advantage >= 0:
            self.score += target_value * 5
            self.captured.append(
                target_value
            )
            return True

        self.score = max(
            0,
            self.score - 20,
        )
        return False

    def tactical_scan(self):
        if self.energy < 10:
            return False

        self.energy -= 10
        self.score += 75
        return True

    def recharge(self):
        self.energy = min(
            100,
            self.energy + 25,
        )

    def next_turn(self):
        self.turn += 1
        self.recharge()

    def status(self):
        return {
            "player": self.player,
            "turn": self.turn,
            "energy": self.energy,
            "score": self.score,
            "captured": list(self.captured),
        }


def create_game():
    return NeonChessDuel()


if __name__ == "__main__":
    game = create_game()
    game.tactical_scan()
    game.calculate_move("knight", 20)
    print(game.status())
