from ajvyra_mobile_engine_v2 import (
    GameEntity,
    MobileGame,
    Transform,
    Vector2,
)
from ajvyra_character_system_v2 import CharacterSystem


class AJVYRAPingPong(MobileGame):
    GAME_ID = "game_005"

    def __init__(self, width=960, height=540):
        super().__init__(width, height)

        self.characters = CharacterSystem(self)

        self.player = self.characters.create(
            "meira",
            "مِیرا",
            "بازیکن اصلی",
            100,
            height / 2,
            speed=260,
            abilities=["ضربه چرخشی", "ضربه قدرتی"]
        )

        self.ball = self.add_entity(
            GameEntity(
                "pingpong_ball",
                Transform(Vector2(width / 2, height / 2)),
                tags={"ball"}
            )
        )

        self.state.update({
            "player_points": 0,
            "opponent_points": 0,
            "ball_speed": 330.0,
            "direction": 1.0,
            "spin": 0.0,
            "rally": 0,
        })

    def strike(self):
        self.state["direction"] *= -1
        self.state["spin"] = (
            self.input.axis(False) * 0.7
        )
        self.state["ball_speed"] = min(
            650,
            self.state["ball_speed"] + 12
        )
        self.state["rally"] += 1
        self.stats.score += 3

    def update_game(self, dt):
        dy = self.input.axis(False)

        self.characters.move_character(
            "meira",
            0,
            dy,
            dt
        )

        self.ball.transform.position.x += (
            self.state["direction"] *
            self.state["ball_speed"] *
            dt
        )

        self.ball.transform.position.y += (
            self.state["spin"] *
            self.state["ball_speed"] *
            dt
        )

        if self.input.action("hit", "space", "enter"):
            self.strike()

        if self.ball.transform.position.y < 20:
            self.ball.transform.position.y = 20
            self.state["spin"] *= -1

        if self.ball.transform.position.y > self.height - 20:
            self.ball.transform.position.y = self.height - 20
            self.state["spin"] *= -1

        if self.ball.transform.position.x < 0:
            self.state["opponent_points"] += 1
            self.reset_rally()

        elif self.ball.transform.position.x > self.width:
            self.state["player_points"] += 1
            self.reset_rally()

        if (
            self.state["player_points"] >= 11 or
            self.state["opponent_points"] >= 11
        ):
            self.paused = True
            self.emit(
                "match_finished",
                player=self.state["player_points"],
                opponent=self.state["opponent_points"]
            )

    def reset_rally(self):
        self.ball.transform.position = Vector2(
            self.width / 2,
            self.height / 2
        )

        self.state["ball_speed"] = 330
        self.state["direction"] = (
            1 if self.random.random() > 0.5 else -1
        )
        self.state["spin"] = 0
        self.state["rally"] = 0
