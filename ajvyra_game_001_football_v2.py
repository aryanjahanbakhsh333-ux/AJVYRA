from ajvyra_mobile_engine_v2 import (
    GameEntity,
    MobileGame,
    Transform,
    Vector2,
)
from ajvyra_character_system_v2 import CharacterSystem
from ajvyra_game_ai_v2 import SimpleCombatAI


class AJVYRAFootballGame(MobileGame):
    GAME_ID = "game_001"

    def __init__(self, width=960, height=540):
        super().__init__(width, height)

        self.characters = CharacterSystem(self)

        self.player = self.characters.create(
            "ario",
            "آریو",
            "بازیکن",
            180,
            height / 2,
            speed=210,
            abilities=["شوت قدرتمند", "دویدن سریع"]
        )

        self.ball = self.add_entity(
            GameEntity(
                "football",
                Transform(
                    Vector2(
                        width / 2,
                        height / 2
                    )
                ),
                tags={"ball"}
            )
        )

        self.enemy = self.add_entity(
            GameEntity(
                "goalkeeper",
                Transform(
                    Vector2(
                        width - 100,
                        height / 2
                    )
                ),
                tags={"enemy"}
            )
        )

        self.ai = SimpleCombatAI(
            self,
            self.enemy,
            self.ball,
            speed=110,
            detection_range=260,
            attack_range=35
        )

        self.state.update({
            "goals": 0,
            "opponent_goals": 0,
            "match_time": 120.0,
            "possession": "player",
            "shot_power": 0.0
        })

    def shoot(self):
        if self.state["possession"] != "player":
            return

        direction = Vector2(
            1.0,
            (self.height / 2 - self.ball.transform.position.y)
            / self.height
        ).normalized()

        self.state["shot_power"] = 1.0

        self.ball.transform.position += direction * 90

        if self.ball.transform.position.x >= self.width - 45:
            self.state["goals"] += 1
            self.stats.score += 100
            self.state["possession"] = "player"

            self.ball.transform.position = Vector2(
                self.width / 2,
                self.height / 2
            )

            self.emit(
                "goal",
                team="player",
                total=self.state["goals"]
            )

    def pass_ball(self):
        if self.state["possession"] == "player":
            self.ball.transform.position.x += 45
            self.stats.score += 5

    def update_game(self, dt):
        self.state["match_time"] = max(
            0.0,
            self.state["match_time"] - dt
        )

        dx = self.input.axis(True)
        dy = self.input.axis(False)

        self.characters.move_character(
            "ario",
            dx,
            dy,
            dt
        )

        if self.state["possession"] == "player":
            self.ball.transform.position = (
                self.player.entity.transform.position
                + Vector2(28, 0)
            )

        if self.input.action("shoot", "space"):
            self.shoot()

        if self.input.action("pass", "p"):
            self.pass_ball()

        self.ai.update(dt)

        if self.state["match_time"] <= 0:
            self.paused = True
            self.emit(
                "match_finished",
                player_goals=self.state["goals"],
                opponent_goals=self.state["opponent_goals"]
            )
