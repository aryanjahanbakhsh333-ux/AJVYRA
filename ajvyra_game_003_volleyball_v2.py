from ajvyra_mobile_engine_v2 import (
    GameEntity,
    MobileGame,
    Transform,
    Vector2,
)
from ajvyra_character_system_v2 import CharacterSystem


class AJVYRAVolleyball(MobileGame):
    GAME_ID = "game_003"

    def __init__(self, width=960, height=540):
        super().__init__(width, height)

        self.characters = CharacterSystem(self)

        self.player = self.characters.create(
            "saya",
            "سایا",
            "بازیکن اصلی",
            180,
            height - 150,
            speed=240,
            abilities=["اسپک سریع", "سرویس چرخشی"]
        )

        self.ball = self.add_entity(
            GameEntity(
                "volleyball",
                Transform(Vector2(260, height / 2)),
                tags={"ball"}
            )
        )

        self.state.update({
            "player_points": 0,
            "opponent_points": 0,
            "ball_height": height / 2,
            "velocity_x": 180.0,
            "velocity_y": -220.0,
            "serve": True,
            "hits": 0,
            "sets": 0,
        })

    def serve(self):
        if not self.state["serve"]:
            return

        self.state["serve"] = False
        self.state["velocity_x"] = 220
        self.state["velocity_y"] = -280
        self.emit("serve")

    def hit(self, power=1.0):
        if self.state["serve"]:
            self.serve()
            return

        self.state["velocity_y"] = -(
            220 + 140 * min(power, 1.0)
        )

        self.state["velocity_x"] = 240 * min(
            power + 0.25,
            1.5
        )

        self.state["hits"] += 1
        self.stats.score += 5

    def update_game(self, dt):
        dx = self.input.axis(True)
        dy = self.input.axis(False)

        self.characters.move_character(
            "saya",
            dx,
            dy,
            dt
        )

        self.state["velocity_y"] += 500 * dt

        self.ball.transform.position.x += (
            self.state["velocity_x"] * dt
        )

        self.ball.transform.position.y += (
            self.state["velocity_y"] * dt
        )

        if self.input.action("serve", "space"):
            self.serve()

        if self.input.action("hit", "enter"):
            self.hit(1.0)

        if self.ball.transform.position.y >= self.height - 40:
            if self.ball.transform.position.x > self.width / 2:
                self.state["player_points"] += 1
            else:
                self.state["opponent_points"] += 1

            self.ball.transform.position = Vector2(
                self.width / 2,
                self.height / 2
            )

            self.state["velocity_x"] = 0
            self.state["velocity_y"] = 0
            self.state["serve"] = True

            self.emit(
                "point",
                player=self.state["player_points"],
                opponent=self.state["opponent_points"]
            )

        if self.state["player_points"] >= 15:
            self.state["sets"] += 1
            self.state["player_points"] = 0
            self.state["opponent_points"] = 0
            self.emit("set_won")

        if self.state["sets"] >= 2:
            self.paused = True
            self.emit("match_finished")
