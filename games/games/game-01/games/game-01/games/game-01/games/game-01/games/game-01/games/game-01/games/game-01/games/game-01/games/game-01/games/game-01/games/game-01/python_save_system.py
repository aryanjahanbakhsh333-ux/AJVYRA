import json
from pathlib import Path


class SaveSystem:

    def __init__(self):
        self.file = Path(
            "black_run_save.json"
        )

    def save(self, state):
        data = {
            "score": state.score,
            "health": state.health,
            "orbs": state.collected_orbs,
            "completed": state.completed
        }

        try:
            self.file.write_text(
                json.dumps(
                    data,
                    indent=4
                ),
                encoding="utf-8"
            )
        except OSError:
            pass

    def load(self):

        if not self.file.exists():
            return None

        try:
            return json.loads(
                self.file.read_text(
                    encoding="utf-8"
                )
            )
        except (
            OSError,
            json.JSONDecodeError
        ):
            return None

    def delete(self):

        if self.file.exists():
            self.file.unlink()
