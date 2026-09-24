from ajvyra_mobile_engine_v2 import (
    MobileGame,
    GameEntity,
    Transform,
    Vector2,
)
from ajvyra_character_system_v2 import CharacterSystem


class AJVYRAFencing(MobileGame):
    GAME_ID = "game_010"

    def __init__(self, width=960, height=540):
        super().__init__(width, height)

        self.characters = CharacterSystem(self)

        self.player = self.characters.create(
            "erin",
            "اِرین",
            "شمشیرباز اصلی",
            230,
            height / 2,
            speed=230,
            abilities=["ضربه برق‌آسا", "دفاع کامل"]
        )

        self.enemy = self.characters.create(
            "fencing_rival",
            "سِیرا",
            "رقیب",
            width - 230,
            height / 2,
            speed=210,
            abilities=["ضدحمله"]
        )

        self.state.update({
            "player_points": 0,
            "enemy_points": 0,
            "energy": 100.0,
            "enemy_energy": 100.0,
            "time": 60.0,
            "guard": False,
        })

    def attack(self):
        distance = self.player.entity.distance_to(
            self.enemy.entity
        )

        if distance <= 130 and self.state["energy"] >= 8:
            self.state["energy"] -= 8

            if self.random.random() < 0.7:
                self.state["player_points"] += 1
                self.stats.score += 100
                self.emit("touch_scored")

    def defend(self):
        self.state["guard"] = True
        self.state["energy"] = min(
            100,
            self.state["energy"] + 4
        )

    def update_game(self, dt):
        self.state["time"] = max(
            0,
            self.state["time"] - dt
        )

        self.state["energy"] = min(
            100,
            self.state["energy"] + 12 * dt
        )

        dx = self.input.axis(True)
        dy = self.input.axis(False)

        self.characters.move_character(
            "erin",
            dx,
            dy,
            dt
        )

        if self.input.action("attack", "space"):
            self.attack()

        if self.input.action("defend", "d"):
            self.defend()
        else:
            self.state["guard"] = False

        if self.state["player_points"] >= 5:
            self.paused = True
            self.emit(
                "victory",
                points=self.state["player_points"]
            )

        elif self.state["enemy_points"] >= 5:
            self.paused = True
            self.emit(
                "defeat",
                points=self.state["enemy_points"]
            )

        elif self.state["time"] <= 0:
            self.paused = True
            self.emit(
                "match_finished",
                player=self.state["player_points"],
                enemy=self.state["enemy_points"]
            )
