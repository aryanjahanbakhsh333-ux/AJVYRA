from ajvyra_mobile_engine_v2 import (
    GameEntity,
    MobileGame,
    Transform,
    Vector2,
)
from ajvyra_character_system_v2 import CharacterSystem


class AJVYRATennis(MobileGame):
    GAME_ID = "game_004"

    def __init__(self, width=960, height=540):
        super().__init__(width, height)

        self.characters = CharacterSystem(self)

        self.player = self.characters.create(
            "kayin",
            "کایِن",
            "بازیکن اصلی",
            150,
            height / 2,
            speed=220,
            abilities=["ضربه ویژه", "سرویس سریع"]
        )

        self.opponent = self.characters.create(
            "tennis_rival",
            "وِیان",
            "رقیب",
            width - 150,
            height / 2,
            speed=190,
            abilities=["ضربه زاویه‌دار"]
        )

        self.ball = self.add_entity(
            GameEntity(
                "tennis_ball",
                Transform(Vector2(width / 2, height / 2)),
                tags={"ball"}
            )
        )

        self.state.update({
            "player_points": 0,
            "opponent_points": 0,
            "player_games": 0,
            "opponent_games": 0,
            "ball_speed": 280.0,
            "ball_dx": 1.0,
            "ball_dy": 0.0,
            "serve": True,
        })

    def serve(self):
        self.state["serve"] = False
        self.state["ball_dx"] = 1.0
        self.state["ball_dy"] = (
            self.random.uniform(-0.7, 0.7)
        )

    def hit(self):
        if self.state["serve"]:
            self.serve()
            return

        self.state["ball_dx"] *= -1

        self.state["ball_dy"] = (
            self.input.axis(False) * 0.8
        )

        self.state["ball_speed"] = min(
            520,
            self.state["ball_speed"] + 8
        )

        self.stats.score += 10

    def update_game(self, dt):
        dx = self.input.axis(True)
        dy = self.input.axis(False)

        self.characters.move_character(
            "kayin",
            dx,
            dy,
            dt
        )

        self.ball.transform.position.x += (
            self.state["ball_dx"] *
            self.state["ball_speed"] *
            dt
        )

        self.ball.transform.position.y += (
            self.state["ball_dy"] *
            self.state["ball_speed"] *
            dt
        )

        if self.input.action("serve", "space"):
            self.serve()

        if self.input.action("hit", "enter"):
            self.hit()

        if self.ball.transform.position.y < 25:
            self.ball.transform.position.y = 25
            self.state["ball_dy"] *= -1

        if self.ball.transform.position.y > self.height - 25:
            self.ball.transform.position.y = self.height - 25
            self.state["ball_dy"] *= -1

        if self.ball.transform.position.x < 0:
            self.state["opponent_points"] += 1
            self.reset_ball()

        elif self.ball.transform.position.x > self.width:
            self.state["player_points"] += 1
            self.reset_ball()

        if self.state["player_points"] >= 4:
            self.state["player_games"] += 1
            self.state["player_points"] = 0
            self.state["opponent_points"] = 0

        if self.state["opponent_points"] >= 4:
            self.state["opponent_games"] += 1
            self.state["player_points"] = 0
            self.state["opponent_points"] = 0

        if (
            self.state["player_games"] >= 3 or
            self.state["opponent_games"] >= 3
        ):
            self.paused = True
            self.emit(
                "match_finished",
                player_games=self.state["player_games"],
                opponent_games=self.state["opponent_games"]
            )

    def reset_ball(self):
        self.ball.transform.position = Vector2(
            self.width / 2,
            self.height / 2
        )

        self.state["ball_speed"] = 280
        self.state["ball_dx"] = (
            -1 if self.random.random() < 0.5 else 1
        )
        self.state["ball_dy"] = 0
        self.state["serve"] = True
