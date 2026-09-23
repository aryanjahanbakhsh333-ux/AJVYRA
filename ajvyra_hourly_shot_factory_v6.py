from __future__ import annotations

import json
import time
from pathlib import Path

from ajvyra_ai_shot_engine_v6 import AJVYRAShotEngine


INTERVAL_SECONDS = 60 * 60


class HourlyShotFactory:

    def __init__(self):
        self.engine = AJVYRAShotEngine()
        self.state_file = (
            Path(__file__).resolve().parent
            / "ajvyra_shot_factory_state.json"
        )

    def _load_state(self):

        if not self.state_file.exists():
            return {"episode": 1}

        try:
            return json.loads(
                self.state_file.read_text(
                    encoding="utf-8"
                )
            )
        except Exception:
            return {"episode": 1}

    def _save_state(self, state):

        self.state_file.write_text(
            json.dumps(
                state,
                ensure_ascii=False,
                indent=2
            ),
            encoding="utf-8"
        )

    def generate_one(self):

        state = self._load_state()

        episode = state["episode"]

        shot = self.engine.next_shot(
            episode=episode
        )

        print(
            f"[AJVYRA] "
            f"Shot {shot.number:03d} "
            f"| {shot.genre} "
            f"| queued"
        )

        return shot

    def run_forever(self):

        print("AJVYRA HOURLY SHOT FACTORY ONLINE")

        while True:

            try:
                self.generate_one()

            except Exception as exc:
                print(
                    "[AJVYRA] Shot generation error:",
                    exc
                )

            time.sleep(INTERVAL_SECONDS)


if __name__ == "__main__":
    HourlyShotFactory().run_forever()
