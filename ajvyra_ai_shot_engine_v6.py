from __future__ import annotations

import json
import time
import uuid
import subprocess
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Optional
from urllib.request import Request, urlopen


ROOT = Path(__file__).resolve().parent
OUTPUT = ROOT / "ajvyra_shots"
OUTPUT.mkdir(exist_ok=True)

COMFY_URL = "http://127.0.0.1:8188"


@dataclass
class Shot:
    id: str
    episode: int
    number: int
    genre: str
    title: str
    prompt: str
    negative_prompt: str
    duration: int = 10
    status: str = "queued"
    video: Optional[str] = None


GENRES = {
    "fantasy": [
        "ancient magical forest",
        "floating ruined kingdom",
        "mysterious moonlit temple",
    ],
    "action": [
        "nighttime rooftop battle",
        "high speed sword confrontation",
        "stormy city chase",
    ],
    "romance": [
        "quiet rainy train station",
        "moonlit riverside meeting",
        "warm sunset school rooftop",
    ],
    "sad": [
        "empty street after rain",
        "lonely room beside a window",
        "silent train leaving at night",
    ],
    "horror": [
        "abandoned hospital corridor",
        "dark forest with unnatural fog",
        "empty house with flickering lights",
    ],
    "heartbreak": [
        "character watching someone leave",
        "empty chair in a dark cafe",
        "rain falling over an abandoned meeting place",
    ],
}


class AJVYRAShotEngine:

    def __init__(self):
        self.db = OUTPUT / "shot_database.json"
        self.shots = self._load()

    def _load(self):
        if not self.db.exists():
            return []

        try:
            return json.loads(self.db.read_text(encoding="utf-8"))
        except Exception:
            return []

    def _save(self):
        self.db.write_text(
            json.dumps(self.shots, ensure_ascii=False, indent=2),
            encoding="utf-8"
        )

    def create_shot(
        self,
        episode: int,
        number: int,
        genre: str,
        story: str,
        character: str,
    ) -> Shot:

        location = GENRES.get(
            genre,
            GENRES["fantasy"]
        )[number % len(GENRES.get(genre, GENRES["fantasy"]))]

        prompt = f"""
Cinematic original anime scene.
Genre: {genre}.
Story context: {story}.
Main character: {character}.
Location: {location}.

10 second cinematic shot.
Consistent character appearance.
Consistent clothing and hairstyle.
Strong facial emotion.
Anime cinematic composition.
Detailed environment.
Natural camera movement.
Professional lighting.
Smooth animation.
No text.
No watermark.
No logos.
"""

        negative = """
low quality,
deformed face,
extra fingers,
extra limbs,
bad anatomy,
flickering,
text,
watermark,
logo,
duplicate character,
inconsistent character,
blurry,
static image
"""

        shot = Shot(
            id=uuid.uuid4().hex,
            episode=episode,
            number=number,
            genre=genre,
            title=f"{genre.title()} Shot {number:03d}",
            prompt=prompt.strip(),
            negative_prompt=negative.strip(),
        )

        self.shots.append(asdict(shot))
        self._save()

        return shot

    def create_initial_30(
        self,
        episode: int = 1,
        story: str = "A mysterious journey through a broken world.",
        character: str = "A young anime protagonist with silver-black hair.",
    ):

        if any(
            s.get("episode") == episode
            for s in self.shots
        ):
            return [
                s for s in self.shots
                if s.get("episode") == episode
            ][:30]

        genres = list(GENRES.keys())

        for number in range(1, 31):
            genre = genres[(number - 1) % len(genres)]

            self.create_shot(
                episode=episode,
                number=number,
                genre=genre,
                story=story,
                character=character,
            )

        return [
            s for s in self.shots
            if s.get("episode") == episode
        ]

    def next_shot(self, episode: int = 1):

        episode_shots = [
            s for s in self.shots
            if s.get("episode") == episode
        ]

        if not episode_shots:
            number = 1
        else:
            number = max(
                s["number"]
                for s in episode_shots
            ) + 1

        genres = list(GENRES.keys())
        genre = genres[(number - 1) % len(genres)]

        return self.create_shot(
            episode=episode,
            number=number,
            genre=genre,
            story="Continuation of the previous cinematic scene.",
            character="The established protagonist.",
        )

    def queue_to_comfyui(self, shot: dict, workflow: dict):

        payload = {
            "prompt": workflow,
            "client_id": shot["id"],
        }

        request = Request(
            COMFY_URL + "/prompt",
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )

        with urlopen(request, timeout=30) as response:
            result = json.loads(
                response.read().decode("utf-8")
            )

        return result.get("prompt_id")

    def render_with_ffmpeg(
        self,
        source: Path,
        destination: Path
    ):

        destination.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        subprocess.run(
            [
                "ffmpeg",
                "-y",
                "-i",
                str(source),
                "-c:v",
                "libx264",
                "-pix_fmt",
                "yuv420p",
                "-movflags",
                "+faststart",
                str(destination),
            ],
            check=True,
        )

        return destination
