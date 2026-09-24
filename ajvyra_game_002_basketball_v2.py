from ajvyra_mobile_engine_v2 import (
    GameEntity,
    MobileGame,
    Transform,
    Vector2,
)
from ajvyra_character_system_v2 import CharacterSystem


class AJVYRAMobileBasketball(MobileGame):
    GAME_ID = "game_002"

    def __init__(self, width=960, height=540):
        super().__init__(width, height)

        self.characters = CharacterSystem(self)

        self.player = self.characters.create(
            "rehan",
            "رِهان",
            "بازیکن اصلی",
            180,
            height / 2,
            speed=210,
            abilities=["پرتاب سه‌امتیازی", "دریبل سریع"]
        )

        self.ball = self.add_entity(
            GameEntity(
                "basketball",
                Transform(Vector2(230, height / 2)),
                tags={"ball"}
            )
        )

        self.opponent = self.characters.create(
            "opponent",
            "کایرو",
            "حریف",
            width - 220,
            height / 2,
            speed=150,
            abilities=["دفاع سریع"]
        )

        self.state.update({
            "player_score": 0,
            "opponent_score": 0,
            "time": 90.0,
            "has_ball": True,
            "dribble": False,
            "shot_charge": 0.0,
        })

    def shoot(self):
        if not self.state["has_ball"]:
            return

        charge = max(0.2, min(1.0, self.state["shot_charge"]))

        distance = abs(
            self.ball.transform.position.x -
            (self.width - 100)
        )

        accuracy = max(
            0.35,
            1.0 - distance / self.width
        )

        chance = accuracy * 0.65 + charge * 0.35

        if self.random.random() <= chance:
            points = 3 if distance > self.width * 0.48 else 2
            self.state["player_score"] += points
            self.stats.score += points * 100
            self.emit(
                "basket_scored",
                points=points
            )
        else:
            self.emit("shot_missed")

        self.state["has_ball"] = False
        self.state["shot_charge"] = 0.0

        self.ball.transform.position = Vector2(
            self.width / 2,
            self.height / 2
        )

    def steal(self):
        if not self.state["has_ball"]:
            return

        if self.random.random() < 0.30:
            self.state["has_ball"] = False
            self.emit("ball_stolen")

    def update_game(self, dt):
        self.state["time"] = max(
            0,
            self.state["time"] - dt
        )

        dx = self.input.axis(True)
        dy = self.input.axis(False)

        self.characters.move_character(
            "rehan",
            dx,
            dy,
            dt
        )

        if self.state["has_ball"]:
            self.ball.transform.position = (
                self.player.entity.transform.position
                + Vector2(25, 10)
            )

        if self.input.action("dribble", "d"):
            self.state["dribble"] = True
            self.stats.score += 1
        else:
            self.state["dribble"] = False

        if self.input.action("shoot", "space"):
            self.state["shot_charge"] += dt

        if self.input.action("release", "enter"):
            self.shoot()

        if self.input.action("steal", "e"):
            self.steal()

        if self.state["time"] <= 0:
            self.paused = True
            self.emit(
                "match_finished",
                player_score=self.state["player_score"],
                opponent_score=self.state["opponent_score"]
            )
