from ajvyra_mobile_engine_v2 import (
    MobileGame,
    GameEntity,
    Transform,
    Vector2,
)
from ajvyra_character_system_v2 import CharacterSystem


class AJVYRAMMA(MobileGame):
    GAME_ID = "game_009"

    def __init__(self, width=960, height=540):
        super().__init__(width, height)

        self.characters = CharacterSystem(self)

        self.player = self.characters.create(
            "vera",
            "وِرا",
            "مبارز اصلی",
            250,
            height / 2,
            speed=215,
            abilities=["جاخالی", "کمبو"]
        )

        self.enemy = self.characters.create(
            "mma_rival",
            "کِروان",
            "حریف",
            width - 250,
            height / 2,
            speed=175,
            abilities=["گلاویز شدن"]
        )

        self.state.update({
            "player_health": 100.0,
            "enemy_health": 100.0,
            "stamina": 100.0,
            "enemy_stamina": 100.0,
            "time": 90.0,
            "grappling": False,
        })

    def strike(self):
        distance = self.player.entity.distance_to(
            self.enemy.entity
        )

        if distance <= 100 and self.state["stamina"] >= 6:
            self.state["stamina"] -= 6

            damage = self.random.randint(5, 11)

            self.state["enemy_health"] = max(
                0,
                self.state["enemy_health"] - damage
            )

            self.stats.score += damage * 2

    def grapple(self):
        distance = self.player.entity.distance_to(
            self.enemy.entity
        )

        if distance <= 70 and self.state["stamina"] >= 10:
            self.state["stamina"] -= 10
            self.state["grappling"] = True

            damage = self.random.randint(8, 16)

            self.state["enemy_health"] = max(
                0,
                self.state["enemy_health"] - damage
            )

            self.stats.score += damage * 3

    def dodge(self):
        self.player.entity.transform.position.x += (
            75 if self.random.random() > 0.5 else -75
        )

    def update_game(self, dt):
        self.state["time"] = max(
            0,
            self.state["time"] - dt
        )

        self.state["stamina"] = min(
            100,
            self.state["stamina"] + 10 * dt
        )

        dx = self.input.axis(True)
        dy = self.input.axis(False)

        self.characters.move_character(
            "vera",
            dx,
            dy,
            dt
        )

        if self.input.action("strike", "j"):
            self.strike()

        if self.input.action("grapple", "g"):
            self.grapple()

        if self.input.action("dodge", "d"):
            self.dodge()

        if self.state["enemy_health"] <= 0:
            self.paused = True
            self.emit("victory")

        elif self.state["player_health"] <= 0:
            self.paused = True
            self.emit("defeat")

        elif self.state["time"] <= 0:
            self.paused = True
            self.emit(
                "decision",
                player_health=self.state["player_health"],
                enemy_health=self.state["enemy_health"]
            )
