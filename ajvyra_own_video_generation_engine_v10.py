from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import subprocess
import time
import uuid
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any, Dict, List, Optional
from urllib.parse import urlencode
from urllib.request import Request, urlopen


# ============================================================
# AJVYRA OWN VIDEO GENERATION ENGINE
# ============================================================
#
# Purpose:
#   AJVYRA's autonomous real-video production engine.
#
# Pipeline:
#
#   STORY
#      ↓
#   WORLD / CHARACTER MEMORY
#      ↓
#   SHOT PLANNER
#      ↓
#   WAN WORKFLOW
#      ↓
#   COMFYUI
#      ↓
#   REAL VIDEO
#      ↓
#   FFMPEG NORMALIZATION
#      ↓
#   PUBLIC MEDIA
#      ↓
#   WEBSITE MANIFEST
#
# No fake video.
# No placeholder media.
# No "publishable" simulation.
#
# The engine only marks a shot as READY after a real
# generated video file has been downloaded and verified.
#
# ============================================================


ENGINE_NAME = "AJVYRA OWN VIDEO ENGINE"
ENGINE_VERSION = "10.0"

ROOT = Path(__file__).resolve().parent

WORKSPACE = ROOT / "ajvyra_video_workspace"
JOBS_DIR = WORKSPACE / "jobs"
OUTPUT_DIR = WORKSPACE / "generated"
PUBLIC_DIR = ROOT / "ajvyra_public_media"

STATE_FILE = WORKSPACE / "engine_state.json"

COMFYUI_URL = os.getenv(
    "AJVYRA_COMFYUI_URL",
    "http://127.0.0.1:8188"
).rstrip("/")

WORKFLOW_FILE = Path(
    os.getenv(
        "AJVYRA_WAN_WORKFLOW",
        str(ROOT / "ajvyra_wan_shot_workflow.json")
    )
)

FPS = int(os.getenv("AJVYRA_FPS", "16"))
WIDTH = int(os.getenv("AJVYRA_WIDTH", "832"))
HEIGHT = int(os.getenv("AJVYRA_HEIGHT", "480"))

SHOT_SECONDS = int(os.getenv("AJVYRA_SHOT_SECONDS", "10"))

MAX_RETRIES = int(
    os.getenv("AJVYRA_MAX_RETRIES", "5")
)

POLL_SECONDS = float(
    os.getenv("AJVYRA_POLL_SECONDS", "2")
)

COMFY_TIMEOUT = int(
    os.getenv("AJVYRA_COMFY_TIMEOUT", "3600")
)


# ============================================================
# FILE SYSTEM
# ============================================================

def ensure_directories() -> None:
    JOBS_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    PUBLIC_DIR.mkdir(parents=True, exist_ok=True)


# ============================================================
# DATA
# ============================================================

@dataclass
class Character:
    name: str
    age: int
    gender: str
    appearance: str
    clothing: str
    personality: str


@dataclass
class World:
    name: str
    location: str
    era: str
    visual_style: str
    atmosphere: str


@dataclass
class Episode:
    episode_id: str
    title: str
    genre: str
    synopsis: str
    world: World
    characters: List[Character]


@dataclass
class Shot:
    shot_id: str
    episode_id: str
    number: int
    duration: int
    description: str
    dialogue: str
    seed: int
    status: str = "QUEUED"
    prompt_id: Optional[str] = None
    output_file: Optional[str] = None
    public_file: Optional[str] = None
    attempts: int = 0
    error: Optional[str] = None


# ============================================================
# HTTP
# ============================================================

class ComfyUI:
    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip("/")

    def request(
        self,
        path: str,
        method: str = "GET",
        payload: Optional[dict] = None,
        timeout: int = 60
    ) -> Any:

        url = self.base_url + path

        body = None

        headers = {
            "User-Agent": "AJVYRA-Video-Engine/10.0"
        }

        if payload is not None:
            body = json.dumps(payload).encode("utf-8")
            headers["Content-Type"] = "application/json"

        request = Request(
            url=url,
            data=body,
            headers=headers,
            method=method
        )

        with urlopen(request, timeout=timeout) as response:
            raw = response.read()

        if not raw:
            return None

        content_type = response.headers.get(
            "Content-Type",
            ""
        )

        if "application/json" in content_type:
            return json.loads(raw.decode("utf-8"))

        try:
            return json.loads(raw.decode("utf-8"))
        except Exception:
            return raw

    def health(self) -> dict:
        return self.request(
            "/system_stats",
            timeout=30
        )

    def queue(self, workflow: dict) -> str:

        client_id = str(uuid.uuid4())

        payload = {
            "prompt": workflow,
            "client_id": client_id
        }

        result = self.request(
            "/prompt",
            method="POST",
            payload=payload,
            timeout=120
        )

        if not isinstance(result, dict):
            raise RuntimeError(
                "ComfyUI returned an invalid queue response."
            )

        if result.get("error"):
            raise RuntimeError(
                json.dumps(
                    result,
                    ensure_ascii=False
                )
            )

        prompt_id = result.get("prompt_id")

        if not prompt_id:
            raise RuntimeError(
                "ComfyUI did not return prompt_id."
            )

        return prompt_id

    def history(self, prompt_id: str) -> dict:
        return self.request(
            f"/history/{prompt_id}",
            timeout=60
        )

    def download(
        self,
        filename: str,
        subfolder: str,
        folder_type: str,
        destination: Path
    ) -> Path:

        query = urlencode({
            "filename": filename,
            "subfolder": subfolder,
            "type": folder_type
        })

        data = self.request(
            f"/view?{query}",
            timeout=120
        )

        if not isinstance(data, (bytes, bytearray)):
            raise RuntimeError(
                "ComfyUI did not return binary media."
            )

        destination.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        destination.write_bytes(data)

        if destination.stat().st_size < 100_000:
            raise RuntimeError(
                "Generated media is too small to be accepted."
            )

        return destination


# ============================================================
# WORKFLOW
# ============================================================

class WanWorkflow:

    def __init__(self, path: Path):
        self.path = path

    def load(self) -> dict:

        if not self.path.exists():
            raise FileNotFoundError(
                f"Real Wan workflow not found: {self.path}"
            )

        with self.path.open(
            "r",
            encoding="utf-8"
        ) as file:
            workflow = json.load(file)

        if not isinstance(workflow, dict):
            raise RuntimeError(
                "Wan workflow must be a JSON object."
            )

        return workflow

    def _replace_recursive(
        self,
        value: Any,
        replacements: Dict[str, Any]
    ) -> Any:

        if isinstance(value, dict):

            return {
                key: self._replace_recursive(
                    item,
                    replacements
                )
                for key, item in value.items()
            }

        if isinstance(value, list):

            return [
                self._replace_recursive(
                    item,
                    replacements
                )
                for item in value
            ]

        if isinstance(value, str):

            result = value

            for token, replacement in replacements.items():

                if token in result:
                    result = result.replace(
                        token,
                        str(replacement)
                    )

            return result

        return value

    def prepare(
        self,
        prompt: str,
        negative_prompt: str,
        seed: int
    ) -> dict:

        workflow = self.load()

        replacements = {
            "{{AJVYRA_PROMPT}}": prompt,
            "{{AJVYRA_NEGATIVE}}": negative_prompt,
            "{{AJVYRA_SEED}}": seed,
            "{{AJVYRA_WIDTH}}": WIDTH,
            "{{AJVYRA_HEIGHT}}": HEIGHT,
            "{{AJVYRA_FPS}}": FPS,
            "{{AJVYRA_SECONDS}}": SHOT_SECONDS,
            "{{AJVYRA_FRAMES}}": FPS * SHOT_SECONDS,
        }

        return self._replace_recursive(
            workflow,
            replacements
        )


# ============================================================
# STORY MEMORY
# ============================================================

class StoryMemory:

    def __init__(self, episode: Episode):

        self.episode = episode

        self.character_text = "\n".join(
            f"""
CHARACTER:
Name: {c.name}
Age: {c.age}
Gender: {c.gender}
Appearance: {c.appearance}
Clothing: {c.clothing}
Personality: {c.personality}
""".strip()
            for c in episode.characters
        )

    def build_prompt(
        self,
        shot: Shot
    ) -> str:

        return f"""
Original cinematic anime scene.

EPISODE:
{self.episode.title}

GENRE:
{self.episode.genre}

WORLD:
Name: {self.episode.world.name}
Location: {self.episode.world.location}
Era: {self.episode.world.era}

VISUAL STYLE:
{self.episode.world.visual_style}

ATMOSPHERE:
{self.episode.world.atmosphere}

CHARACTER CONTINUITY:
{self.character_text}

SCENE:
{shot.description}

DIALOGUE CONTEXT:
{shot.dialogue}

SHOT:
{shot.number}

DURATION:
{shot.duration} seconds

Camera movement should be cinematic and intentional.
Maintain character identity, clothing, environment,
lighting language and visual continuity.

High quality anime cinematic composition.
Detailed background.
Natural movement.
Expressive faces.
Consistent anatomy.
Cinematic depth.
Professional animation direction.
""".strip()

    @staticmethod
    def negative() -> str:

        return """
low quality,
blurry,
deformed anatomy,
extra fingers,
extra limbs,
duplicate character,
broken face,
distorted eyes,
warped body,
text,
watermark,
logo,
random letters,
flickering,
frame instability,
inconsistent character,
bad hands,
cropped head,
unfinished render
""".strip()


# ============================================================
# SHOT PLANNER
# ============================================================

class ShotPlanner:

    ACTIONS = [
        "walking through the environment",
        "looking toward a distant light",
        "slowly turning toward the camera",
        "running through the environment",
        "standing silently while wind moves clothing",
        "reaching toward an object",
        "watching rain through a window",
        "entering an unfamiliar location",
        "looking back after hearing a sound",
        "walking toward another character",
        "sitting alone and remembering something",
        "raising their head after an emotional moment",
    ]

    def create(
        self,
        episode: Episode,
        number: int
    ) -> Shot:

        index = number - 1

        action = self.ACTIONS[
            index % len(self.ACTIONS)
        ]

        character = episode.characters[
            index % len(episode.characters)
        ]

        description = (
            f"{character.name} is {action}. "
            f"The scene takes place in "
            f"{episode.world.location}. "
            f"The emotional tone follows the story "
            f"of {episode.title}. "
            f"The shot naturally continues from the "
            f"previous cinematic moment."
        )

        dialogue = (
            f"{character.name}: "
            f"I remember why I came here."
        )

        seed_source = (
            f"{episode.episode_id}:"
            f"{number}:"
            f"{episode.title}"
        )

        digest = hashlib.sha256(
            seed_source.encode("utf-8")
        ).hexdigest()

        seed = int(
            digest[:12],
            16
        )

        return Shot(
            shot_id=f"{episode.episode_id}_shot_{number:04d}",
            episode_id=episode.episode_id,
            number=number,
            duration=SHOT_SECONDS,
            description=description,
            dialogue=dialogue,
            seed=seed
        )


# ============================================================
# VIDEO VALIDATION
# ============================================================

class RealVideo:

    @staticmethod
    def ffprobe(
        path: Path
    ) -> dict:

        command = [
            "ffprobe",
            "-v",
            "error",
            "-print_format",
            "json",
            "-show_streams",
            "-show_format",
            str(path)
        ]

        result = subprocess.run(
            command,
            capture_output=True,
            text=True
        )

        if result.returncode != 0:
            raise RuntimeError(
                result.stderr.strip()
            )

        return json.loads(result.stdout)

    @classmethod
    def validate(
        cls,
        path: Path
    ) -> dict:

        if not path.exists():
            raise RuntimeError(
                "Video file does not exist."
            )

        if path.stat().st_size < 100_000:
            raise RuntimeError(
                "Video file is too small."
            )

        data = cls.ffprobe(path)

        streams = data.get(
            "streams",
            []
        )

        video = next(
            (
                s for s in streams
                if s.get("codec_type") == "video"
            ),
            None
        )

        if video is None:
            raise RuntimeError(
                "No video stream found."
            )

        duration = float(
            data.get("format", {})
            .get("duration", 0)
        )

        if duration < 1:
            raise RuntimeError(
                "Invalid video duration."
            )

        return {
            "duration": duration,
            "codec": video.get("codec_name"),
            "width": video.get("width"),
            "height": video.get("height"),
            "size": path.stat().st_size
        }

    @staticmethod
    def normalize(
        source: Path,
        destination: Path
    ) -> Path:

        destination.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        command = [
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

            "-an",

            str(destination)
        ]

        result = subprocess.run(
            command,
            capture_output=True,
            text=True
        )

        if result.returncode != 0:
            raise RuntimeError(
                result.stderr[-4000:]
            )

        RealVideo.validate(destination)

        return destination


# ============================================================
# PUBLIC WEBSITE PUBLISHER
# ============================================================

class PublicPublisher:

    def __init__(
        self,
        root: Path
    ):
        self.root = root

    def publish(
        self,
        episode: Episode,
        shot: Shot,
        video: Path
    ) -> Path:

        target_dir = (
            self.root
            / "anime"
            / episode.episode_id
            / "shots"
            / f"shot_{shot.number:04d}"
        )

        target_dir.mkdir(
            parents=True,
            exist_ok=True
        )

        target = (
            target_dir
            / "main.mp4"
        )

        shutil.copy2(
            video,
            target
        )

        shot.public_file = str(
            target.relative_to(self.root)
        )

        self.write_manifest(
            episode
        )

        return target

    def write_manifest(
        self,
        episode: Episode
    ) -> None:

        episode_dir = (
            self.root
            / "anime"
            / episode.episode_id
        )

        shots_dir = (
            episode_dir
            / "shots"
        )

        records = []

        if shots_dir.exists():

            for directory in sorted(
                shots_dir.iterdir()
            ):

                video = (
                    directory
                    / "main.mp4"
                )

                if not video.exists():
                    continue

                records.append({
                    "shot": directory.name,
                    "video": (
                        f"/media/anime/"
                        f"{episode.episode_id}/"
                        f"shots/{directory.name}/main.mp4"
                    )
                })

        manifest = {
            "episode_id": episode.episode_id,
            "title": episode.title,
            "genre": episode.genre,
            "shots": records,
            "updated_at": time.time()
        }

        manifest_path = (
            episode_dir
            / "manifest.json"
        )

        manifest_path.write_text(
            json.dumps(
                manifest,
                ensure_ascii=False,
                indent=2
            ),
            encoding="utf-8"
        )


# ============================================================
# ENGINE STATE
# ============================================================

class State:

    def __init__(self):
        self.data = {
            "engine": ENGINE_VERSION,
            "started": time.time(),
            "shots": {}
        }

    def load(self):

        if not STATE_FILE.exists():
            return

        try:
            self.data = json.loads(
                STATE_FILE.read_text(
                    encoding="utf-8"
                )
            )
        except Exception:
            pass

    def save(self):

        STATE_FILE.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        STATE_FILE.write_text(
            json.dumps(
                self.data,
                ensure_ascii=False,
                indent=2
            ),
            encoding="utf-8"
        )

    def update(
        self,
        shot: Shot
    ):

        self.data["shots"][
            shot.shot_id
        ] = asdict(shot)

        self.save()


# ============================================================
# MAIN ENGINE
# ============================================================

class AJVYRAOwnVideoEngine:

    def __init__(
        self,
        episode: Episode
    ):

        ensure_directories()

        self.episode = episode

        self.comfy = ComfyUI(
            COMFYUI_URL
        )

        self.workflow = WanWorkflow(
            WORKFLOW_FILE
        )

        self.memory = StoryMemory(
            episode
        )

        self.planner = ShotPlanner()

        self.publisher = PublicPublisher(
            PUBLIC_DIR
        )

        self.state = State()

        self.state.load()

    def check_backend(self):

        print(
            "[AJVYRA] Checking real Wan backend..."
        )

        result = self.comfy.health()

        print(
            "[AJVYRA] ComfyUI/Wan backend ONLINE"
        )

        return result

    def generate(
        self,
        shot: Shot
    ) -> Shot:

        self.state.update(shot)

        prompt = self.memory.build_prompt(
            shot
        )

        negative = self.memory.negative()

        for attempt in range(
            1,
            MAX_RETRIES + 1
        ):

            shot.attempts = attempt
            shot.status = "GENERATING"
            shot.error = None

            self.state.update(shot)

            print(
                f"[AJVYRA] "
                f"{shot.shot_id} "
                f"attempt {attempt}"
            )

            try:

                graph = self.workflow.prepare(
                    prompt=prompt,
                    negative_prompt=negative,
                    seed=shot.seed + attempt
                )

                prompt_id = self.comfy.queue(
                    graph
                )

                shot.prompt_id = prompt_id

                self.state.update(shot)

                print(
                    f"[AJVYRA] Wan job: "
                    f"{prompt_id}"
                )

                output = self.wait_for_result(
                    shot
                )

                normalized = (
                    OUTPUT_DIR
                    / self.episode.episode_id
                    / f"shot_{shot.number:04d}.mp4"
                )

                RealVideo.normalize(
                    output,
                    normalized
                )

                metadata = RealVideo.validate(
                    normalized
                )

                print(
                    "[AJVYRA] REAL VIDEO CREATED:"
                )

                print(
                    json.dumps(
                        metadata,
                        indent=2
                    )
                )

                public = self.publisher.publish(
                    self.episode,
                    shot,
                    normalized
                )

                shot.output_file = str(
                    normalized
                )

                shot.public_file = str(
                    public
                )

                shot.status = "READY"

                self.state.update(shot)

                print(
                    f"[AJVYRA] "
                    f"PUBLISHED: {public}"
                )

                return shot

            except Exception as exc:

                shot.error = str(exc)
                shot.status = "RETRYING"

                self.state.update(shot)

                print(
                    f"[AJVYRA] "
                    f"Generation failed: {exc}"
                )

                if attempt < MAX_RETRIES:

                    time.sleep(
                        min(
                            30 * attempt,
                            180
                        )
                    )

        shot.status = "FAILED"

        self.state.update(shot)

        raise RuntimeError(
            f"Real generation failed permanently: "
            f"{shot.shot_id}"
        )

    def wait_for_result(
        self,
        shot: Shot
    ) -> Path:

        started = time.time()

        while True:

            if (
                time.time() - started
                > COMFY_TIMEOUT
            ):
                raise TimeoutError(
                    "Wan generation timed out."
                )

            history = self.comfy.history(
                shot.prompt_id
            )

            job = history.get(
                shot.prompt_id
            )

            if not job:

                time.sleep(
                    POLL_SECONDS
                )

                continue

            status = job.get(
                "status",
                {}
            )

            if status.get(
                "status_str"
            ) == "error":

                raise RuntimeError(
                    json.dumps(
                        status,
                        ensure_ascii=False
                    )
                )

            if not status.get(
                "completed",
                False
            ):

                time.sleep(
                    POLL_SECONDS
                )

                continue

            outputs = job.get(
                "outputs",
                {}
            )

            video_output = self.find_video(
                outputs
            )

            if not video_output:

                raise RuntimeError(
                    "Wan completed but returned "
                    "no video output."
                )

            filename = (
                video_output["filename"]
            )

            subfolder = (
                video_output.get(
                    "subfolder",
                    ""
                )
            )

            folder_type = (
                video_output.get(
                    "type",
                    "output"
                )
            )

            destination = (
                OUTPUT_DIR
                / self.episode.episode_id
                / "raw"
                / f"{shot.shot_id}.webm"
            )

            return self.comfy.download(
                filename,
                subfolder,
                folder_type,
                destination
            )

    @staticmethod
    def find_video(
        outputs: dict
    ) -> Optional[dict]:

        for node_output in outputs.values():

            if not isinstance(
                node_output,
                dict
            ):
                continue

            for key in (
                "videos",
                "gifs",
                "images"
            ):

                items = node_output.get(
                    key
                )

                if not items:
                    continue

                for item in items:

                    filename = item.get(
                        "filename"
                    )

                    if not filename:
                        continue

                    extension = (
                        Path(filename)
                        .suffix
                        .lower()
                    )

                    if extension in {
                        ".mp4",
                        ".webm",
                        ".mov",
                        ".mkv"
                    }:

                        return item

        return None

    def create_shot(
        self,
        number: int
    ) -> Shot:

        return self.planner.create(
            self.episode,
            number
        )

    def generate_shot(
        self,
        number: int
    ) -> Shot:

        shot = self.create_shot(
            number
        )

        return self.generate(
            shot
        )


# ============================================================
# EXAMPLE ORIGINAL WORLD
# ============================================================

def create_demo_episode() -> Episode:

    return Episode(

        episode_id="episode_01",

        title="The Memory That Remained",

        genre="dark fantasy",

        synopsis=(
            "A young traveler enters a broken city "
            "where forgotten memories have become "
            "physical fragments of light."
        ),

        world=World(
            name="The Broken City",
            location=(
                "a ruined midnight city "
                "surrounded by silent mountains"
            ),
            era="fictional post-modern era",
            visual_style=(
                "cinematic dark anime, "
                "detailed backgrounds, "
                "soft volumetric lighting"
            ),
            atmosphere=(
                "melancholic, mysterious, "
                "quiet, emotional"
            )
        ),

        characters=[

            Character(
                name="Kael Veyron",
                age=19,
                gender="male",
                appearance=(
                    "black hair, pale skin, "
                    "gray eyes"
                ),
                clothing=(
                    "long dark coat, "
                    "black boots"
                ),
                personality=(
                    "quiet, observant, "
                    "determined"
                )
            ),

            Character(
                name="Elyra Noctis",
                age=19,
                gender="female",
                appearance=(
                    "long silver hair, "
                    "violet eyes"
                ),
                clothing=(
                    "dark blue coat, "
                    "silver accessories"
                ),
                personality=(
                    "calm, mysterious, "
                    "emotionally guarded"
                )
            )

        ]
    )


# ============================================================
# COMMAND LINE
# ============================================================

def main():

    parser = argparse.ArgumentParser(
        description=ENGINE_NAME
    )

    parser.add_argument(
        "command",
        choices=[
            "health",
            "shot",
            "batch"
        ]
    )

    parser.add_argument(
        "--number",
        type=int,
        default=1
    )

    parser.add_argument(
        "--count",
        type=int,
        default=1
    )

    args = parser.parse_args()

    episode = create_demo_episode()

    engine = AJVYRAOwnVideoEngine(
        episode
    )

    if args.command == "health":

        result = engine.check_backend()

        print(
            json.dumps(
                result,
                indent=2
            )
        )

        return

    if args.command == "shot":

        engine.check_backend()

        shot = engine.generate_shot(
            args.number
        )

        print(
            json.dumps(
                asdict(shot),
                ensure_ascii=False,
                indent=2
            )
        )

        return

    if args.command == "batch":

        engine.check_backend()

        for number in range(
            args.number,
            args.number + args.count
        ):

            engine.generate_shot(
                number
            )


if __name__ == "__main__":
    main()
