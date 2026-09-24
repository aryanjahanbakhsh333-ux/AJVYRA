from ajvyra_mobile_engine_v2 import (
    MobileGame,
    GameEntity,
    Transform,
    Vector2,
)
from ajvyra_character_system_v2 import CharacterSystem


class AJVYRABoxing(MobileGame):
    GAME_ID = "game_008"

    def __init__(self, width=960, height=540):
        super().__init__(width, height)

        self.characters = CharacterSystem(self)

        self.player = self.characters.create(
            "elvan",
            "اِلوان",
            "بوکسور اصلی",
            250,
            height / 2,
            speed=205,
            abilities=["ضربه مستقیم", "ضربه قدرتی"]
        )

        self.enemy = self.characters.create(
            "boxing_rival",
            "رادِک",
            "حریف",
            width - 250,
            height / 2,
            speed=170,
            abilities=["هوک سنگین"]
        )

        self.state.update({
            "round": 1,
            "round_time": 60,
            "player_health": 100,
            "enemy_health": 100,
            "stamina": 100,
            "enemy_stamina": 100,
        })

    def jab(self):
        distance = self.player.entity.distance_to(
            self.enemy.entity
        )

        if distance <= 100 and self.state["stamina"] >= 3:
            self.state["stamina"] -= 3
            self.state["enemy_health"] = max(
                0,
                self.state["enemy_health"] - 5
            )
            self.stats.score += 10

    def power_punch(self):
        distance = self.player.entity.distance_to(
            self.enemy.entity
        )

        if distance <= 105 and self.state["stamina"] >= 15:
            self.state["stamina"] -= 15
            self.state["enemy_health"] = max(
                0,
                self.state["enemy_health"] - 15
            )
            self.stats.score += 30

    def guard(self):
        self.state["stamina"] = min(
            100,
            self.state["stamina"] + 5
        )

    def update_game(self, dt):
        self.state["round_time"] = max(
            0,
            self.state["round_time"] - dt
        )

        self.state["stamina"] = min(
            100,
            self.state["stamina"] + 8 * dt
        )

        dx = self.input.axis(True)
        dy = self.input.axis(False)

        self.characters.move_character(
            "elvan",
            dx,
            dy,
            dt
        )

        if self.input.action("jab", "j"):
            self.jab()

        if self.input.action("power", "k"):
            self.power_punch()

        if self.input.action("guard", "d"):
            self.guard()

        if self.state["enemy_health"] <= 0:
            self.paused = True
            self.emit("knockout")

        if self.state["round_time"] <= 0:
            self.paused = True

            result = (
                "victory"
                if self.state["enemy_health"]
                < self.state["player_health"]
                else "defeat"
            )

            self.emit(
                "round_finished",
                result=result
            )
