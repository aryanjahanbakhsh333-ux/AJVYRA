from ajvyra_mobile_engine_v2 import (
    GameEntity,
    MobileGame,
    Transform,
    Vector2,
)
from ajvyra_character_system_v2 import CharacterSystem


class AJVYRAKickboxing(MobileGame):
    GAME_ID = "game_007"

    def __init__(self, width=960, height=540):
        super().__init__(width, height)

        self.characters = CharacterSystem(self)

        self.player = self.characters.create(
            "neiro",
            "نِیرو",
            "مبارز اصلی",
            260,
            height / 2,
            speed=220,
            abilities=["کمبو", "جاخالی سریع"]
        )

        self.enemy = self.characters.create(
            "kickboxing_rival",
            "زِرون",
            "حریف",
            width - 260,
            height / 2,
            speed=180,
            abilities=["ضربه سنگین"]
        )

        self.state.update({
            "round": 1,
            "time": 60.0,
            "combo": 0,
            "energy": 100.0,
            "enemy_energy": 100.0,
            "enemy_health": 100.0,
            "health": 100.0,
        })

    def punch(self):
        distance = self.player.entity.distance_to(
            self.enemy.entity
        )

        if distance <= 95 and self.state["energy"] >= 5:
            self.state["energy"] -= 5
            self.state["combo"] += 1
            damage = 7 + min(
                self.state["combo"],
                5
            )

            self.state["enemy_health"] = max(
                0,
                self.state["enemy_health"] - damage
            )

            self.stats.score += damage
            self.emit(
                "hit",
                type="punch",
                damage=damage
            )

    def kick(self):
        distance = self.player.entity.distance_to(
            self.enemy.entity
        )

        if distance <= 115 and self.state["energy"] >= 12:
            self.state["energy"] -= 12
            self.state["combo"] += 1

            damage = 13 + min(
                self.state["combo"] * 2,
                12
            )

            self.state["enemy_health"] = max(
                0,
                self.state["enemy_health"] - damage
            )

            self.stats.score += damage * 2

            self.emit(
                "hit",
                type="kick",
                damage=damage
            )

    def dodge(self):
        self.player.entity.transform.position.x += (
            -60 if self.random.random() < 0.5 else 60
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
            "neiro",
            dx,
            dy,
            dt
        )

        if self.input.action("punch", "j"):
            self.punch()

        if self.input.action("kick", "k"):
            self.kick()

        if self.input.action("dodge", "d"):
            self.dodge()

        if self.state["enemy_health"] <= 0:
            self.paused = True
            self.emit("victory")

        if self.state["time"] <= 0:
            self.paused = True

            if self.state["enemy_health"] < self.state["health"]:
                self.emit("victory_by_score")
            else:
                self.emit("defeat")
