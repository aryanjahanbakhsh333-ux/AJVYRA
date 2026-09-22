from __future__ import annotations

import json
import time
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Dict, Optional


WATCH_ROOT = Path(
    "ajvyra_projects/anime/watch_state"
)

WATCH_ROOT.mkdir(
    parents=True,
    exist_ok=True,
)


@dataclass
class WatchState:
    anime_id: int
    position_seconds: float = 0.0
    duration_seconds: float = 1800.0
    selected_audio: str = "fa"
    selected_subtitle: str = "fa"
    updated_at: float = 0.0
    completed: bool = False


class AnimeWatchRuntime:
    """
    Playback state for AJVYRA Anime.

    Designed for mobile and desktop clients.
    """

    def __init__(
        self,
        root: Path = WATCH_ROOT,
    ):
        self.root = Path(root)
        self.root.mkdir(
            parents=True,
            exist_ok=True,
        )

    def _path(self, anime_id: int) -> Path:
        return self.root / f"anime_{int(anime_id):02d}.json"

    def load(self, anime_id: int) -> WatchState:
        path = self._path(anime_id)

        if not path.exists():
            return WatchState(
                anime_id=int(anime_id)
            )

        try:
            data = json.loads(
                path.read_text(
                    encoding="utf-8"
                )
            )

            return WatchState(
                anime_id=int(
                    data.get(
                        "anime_id",
                        anime_id,
                    )
                ),
                position_seconds=float(
                    data.get(
                        "position_seconds",
                        0,
                    )
                ),
                duration_seconds=float(
                    data.get(
                        "duration_seconds",
                        1800,
                    )
                ),
                selected_audio=str(
                    data.get(
                        "selected_audio",
                        "fa",
                    )
                ),
                selected_subtitle=str(
                    data.get(
                        "selected_subtitle",
                        "fa",
                    )
                ),
                updated_at=float(
                    data.get(
                        "updated_at",
                        0,
                    )
                ),
                completed=bool(
                    data.get(
                        "completed",
                        False,
                    )
                ),
            )

        except Exception:
            return WatchState(
                anime_id=int(anime_id)
            )

    def save(
        self,
        anime_id: int,
        position_seconds: float,
        selected_audio: str = "fa",
        selected_subtitle: str = "fa",
        duration_seconds: float = 1800,
    ) -> WatchState:

        position = max(
            0.0,
            min(
                float(position_seconds),
                float(duration_seconds),
            ),
        )

        state = WatchState(
            anime_id=int(anime_id),
            position_seconds=position,
            duration_seconds=float(
                duration_seconds
            ),
            selected_audio=(
                selected_audio
                if selected_audio in {"fa", "ja"}
                else "fa"
            ),
            selected_subtitle=(
                selected_subtitle
                if selected_subtitle in {
                    "en",
                    "fa",
                    "ja",
                    "off",
                }
                else "fa"
            ),
            updated_at=time.time(),
            completed=position >= (
                float(duration_seconds) - 5
            ),
        )

        self._path(anime_id).write_text(
            json.dumps(
                asdict(state),
                ensure_ascii=False,
                indent=2,
            ),
            encoding="utf-8",
        )

        return state

    def reset(self, anime_id: int) -> WatchState:
        state = WatchState(
            anime_id=int(anime_id)
        )

        self._path(anime_id).write_text(
            json.dumps(
                asdict(state),
                ensure_ascii=False,
                indent=2,
            ),
            encoding="utf-8",
        )

        return state

    def payload(self, anime_id: int) -> Dict[str, Any]:
        state = self.load(anime_id)

        return {
            "anime_id": state.anime_id,
            "position_seconds": state.position_seconds,
            "duration_seconds": state.duration_seconds,
            "progress": round(
                (
                    state.position_seconds
                    / max(
                        1,
                        state.duration_seconds,
                    )
                )
                * 100,
                2,
            ),
            "audio": state.selected_audio,
            "subtitle": state.selected_subtitle,
            "completed": state.completed,
            "updated_at": state.updated_at,
        }


WATCH_RUNTIME = AnimeWatchRuntime()
