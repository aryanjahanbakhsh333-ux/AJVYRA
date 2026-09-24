from ajvyra_mobile_engine_v2 import (
    GameEntity,
    MobileGame,
    Transform,
    Vector2,
)
from ajvyra_character_system_v2 import CharacterSystem


class AJVYRAWrestling(MobileGame):
    GAME_ID = "game_006"

    def __init__(self, width=960, height=540):
        super().__init__(width, height)

        self.characters = CharacterSystem(self)

        self.player = self.characters.create(
            "daren",
            "دارِن",
            "کشتی‌گیر اصلی",
            250,
            height / 2,
            speed=190,
            abilities=["فن پرتاب", "دفاع سریع"]
        )

        self.enemy = self.characters.create(
            "wrestling_rival",
            "بِرانو",
            "حریف",
            width - 250,
            height / 2,
            speed=170,
            abilities=["فن قدرتی"]
        )

        self.state.update({
            "player_score": 0,
            "enemy_score": 0,
            "stamina": 100.0,
            "enemy_stamina": 100.0,
            "round_time": 120.0,
            "grapple": False,
        })

    def grapple(self):
        distance = self.player.entity.distance_to(
            self.enemy.entity
        )

        if distance > 100:
            return

        self.state["grapple"] = True

        if self.random.random() < 0.55:
            self.state["player_score"] += 2
            self.stats.score += 20
            self.state["enemy_stamina"] = max(
                0,
                self.state["enemy_stamina"] - 15
            )
            self.emit("takedown")

        else:
            self.state["stamina"] = max(
                0,
                self.state["stamina"] - 10
            )
            self.emit("countered")

    def defend(self):
        self.state["stamina"] = min(
            100,
            self.state["stamina"] + 3
        )

    def update_game(self, dt):
        self.state["round_time"] = max(
            0,
            self.state["round_time"] - dt
        )

        dx = self.input.axis(True)
        dy = self.input.axis(False)

        self.characters.move_character(
            "daren",
            dx,
            dy,
            dt
        )

        if self.input.action("grapple", "space"):
            self.grapple()

        if self.input.action("defend", "d"):
            self.defend()

        if self.state["enemy_stamina"] <= 0:
            self.state["player_score"] += 5
            self.paused = True
            self.emit("victory")

        if self.state["stamina"] <= 0:
            self.paused = True
            self.emit("defeat")

        if self.state["round_time"] <= 0:
            self.paused = True

            if self.state["player_score"] >= self.state["enemy_score"]:
                self.emit("match_finished", result="player")
            else:
                self.emit("match_finished", result="enemy")
