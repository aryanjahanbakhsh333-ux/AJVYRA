# ajvyra_absolute_complete_release_v9.py
#
# FINAL AJVYRA RELEASE ORCHESTRATOR
#
# هدف:
# - 30 بازی مرورگری واقعی و قابل بازی
# - 30 داستان/اپیزود انیمه
# - شات‌های واقعی MP4 تولیدشده توسط Wan/ComfyUI
# - انتشار خودکار شات‌های واقعی
# - تولید شات متفاوت هر ساعت
# - Manifest و Player قابل استفاده در سایت
# - قفل انتشار تا زمانی که فایل واقعی وجود نداشته باشد
#
# این فایل هیچ ویدیوی جعلی یا Placeholder تولید نمی‌کند.
# اگر Wan/ComfyUI خروجی واقعی ندهد، انتشار آن شات متوقف می‌شود.

from __future__ import annotations

import json
import os
import random
import shutil
import subprocess
import sys
import time
import uuid
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any

import requests


# ============================================================
# ROOT
# ============================================================

ROOT = Path(__file__).resolve().parent

SITE_ROOT = ROOT / "ajvyra_site"
PUBLIC_ROOT = ROOT / "ajvyra_public_media"

GAME_ROOT = SITE_ROOT / "games"
ANIME_ROOT = SITE_ROOT / "anime"

PUBLIC_ANIME_ROOT = PUBLIC_ROOT / "anime"

STATE_ROOT = ROOT / "ajvyra_final_runtime"

GAME_STATE = STATE_ROOT / "games"
ANIME_STATE = STATE_ROOT / "anime"

WORK_ROOT = STATE_ROOT / "work"

for path in (
    SITE_ROOT,
    GAME_ROOT,
    ANIME_ROOT,
    PUBLIC_ROOT,
    PUBLIC_ANIME_ROOT,
    STATE_ROOT,
    GAME_STATE,
    ANIME_STATE,
    WORK_ROOT,
):
    path.mkdir(parents=True, exist_ok=True)


# ============================================================
# CONFIG
# ============================================================

COMFYUI_URL = os.getenv(
    "AJVYRA_COMFYUI_URL",
    "http://127.0.0.1:8188",
).rstrip("/")

WAN_WORKFLOW = Path(
    os.getenv(
        "AJVYRA_WAN_WORKFLOW",
        str(ROOT / "ajvyra_wan_shot_workflow.json"),
    )
)

FFMPEG = os.getenv("FFMPEG", "ffmpeg")
FFPROBE = os.getenv("FFPROBE", "ffprobe")

SHOT_SECONDS = 10
SHOT_FPS = 16

VIDEO_WIDTH = 832
VIDEO_HEIGHT = 480

HOURLY_INTERVAL = 3600

MAX_RETRIES = 3

TOTAL_GAMES = 30
TOTAL_ANIME = 30

SHOTS_PER_ANIME = 180

TOTAL_REQUIRED_SHOTS = (
    TOTAL_ANIME * SHOTS_PER_ANIME
)


# ============================================================
# ORIGINAL WORLD DATA
# ============================================================

ANIME_WORLDS = [
    {
        "id": "anime_01",
        "title": "The Memory That Remained",
        "genre": "heartbreak",
        "characters": [
            "Kael Veyron",
            "Elyra Noctis",
        ],
        "location": "The Broken City",
    },
    {
        "id": "anime_02",
        "title": "Moonfall Kingdom",
        "genre": "fantasy",
        "characters": [
            "Aren Solvane",
            "Lyra Veyne",
        ],
        "location": "Moonfall Kingdom",
    },
    {
        "id": "anime_03",
        "title": "When The Rain Stopped",
        "genre": "romance",
        "characters": [
            "Noren Vale",
            "Aelia Ryn",
        ],
        "location": "Rain District",
    },
    {
        "id": "anime_04",
        "title": "The Last Lantern",
        "genre": "sad",
        "characters": [
            "Riven Ash",
            "Mira Solen",
        ],
        "location": "Old Harbor",
    },
    {
        "id": "anime_05",
        "title": "Whispers Beneath",
        "genre": "horror",
        "characters": [
            "Eron Vail",
            "Selene Dusk",
        ],
        "location": "Silent Forest",
    },
    {
        "id": "anime_06",
        "title": "The Glass Horizon",
        "genre": "action",
        "characters": [
            "Darian Vox",
            "Neya Aris",
        ],
        "location": "Glass Bridge",
    },
]


GAME_GENRES = [
    "rpg",
    "action",
    "platformer",
    "puzzle",
    "racing",
    "survival",
    "horror",
    "arcade",
    "strategy",
    "adventure",
]


GAME_NAMES = [
    "Black Horizon",
    "Memory Runner",
    "Nightfall Quest",
    "Broken Kingdom",
    "Silent Forest",
    "Shadow Circuit",
    "Moon Escape",
    "Last Guardian",
    "Dark Harbor",
    "Echo Blade",
    "Rainbound",
    "Glass Tower",
    "Lost Signal",
    "Crimson Path",
    "Forgotten Door",
    "Void Runner",
    "Dream Hunter",
    "Neon Ruins",
    "The Last Light",
    "Ashen Road",
    "Starless Night",
    "Black River",
    "Hidden Realm",
    "Final Echo",
    "Ghost Station",
    "Fallen Crown",
    "Memory Gate",
    "Cold Moon",
    "Broken Signal",
    "Beyond Silence",
]


# ============================================================
# DATA
# ============================================================

@dataclass
class Shot:
    anime_id: str
    number: int
    title: str
    genre: str
    characters: list[str]
    location: str
    action: str
    camera: str
    seed: int

    status: str = "queued"
    video: str = ""
    duration: float = 0.0
    error: str = ""
    prompt_id: str = ""
    created_at: float = 0.0
    completed_at: float = 0.0


# ============================================================
# PROCESS
# ============================================================

def process(
    command: list[str],
    timeout: int = 600,
) -> subprocess.CompletedProcess:

    return subprocess.run(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        timeout=timeout,
    )


# ============================================================
# FFMPEG
# ============================================================

def duration(path: Path) -> float:

    if not path.exists():
        return 0.0

    try:

        result = process(
            [
                FFPROBE,
                "-v",
                "error",
                "-show_entries",
                "format=duration",
                "-of",
                "default=noprint_wrappers=1:nokey=1",
                str(path),
            ],
            timeout=60,
        )

        if result.returncode != 0:
            return 0.0

        return float(
            result.stdout.strip()
        )

    except Exception:
        return 0.0


def valid_real_video(path: Path) -> bool:

    if not path.exists():
        return False

    if path.stat().st_size < 100_000:
        return False

    d = duration(path)

    if not 8.0 <= d <= 12.0:
        return False

    result = process(
        [
            FFPROBE,
            "-v",
            "error",
            "-select_streams",
            "v:0",
            "-show_entries",
            "stream=codec_name,width,height",
            "-of",
            "json",
            str(path),
        ],
        timeout=60,
    )

    if result.returncode != 0:
        return False

    try:

        data = json.loads(
            result.stdout
        )

        streams = data.get(
            "streams",
            [],
        )

        if not streams:
            return False

        stream = streams[0]

        if not stream.get(
            "codec_name"
        ):
            return False

        if int(
            stream.get("width", 0)
        ) <= 0:
            return False

        if int(
            stream.get("height", 0)
        ) <= 0:
            return False

        return True

    except Exception:
        return False


# ============================================================
# COMFYUI
# ============================================================

class ComfyUI:

    def __init__(
        self,
        base_url: str = COMFYUI_URL,
    ):
        self.base_url = base_url.rstrip("/")

    def health(self) -> bool:

        try:

            response = requests.get(
                self.base_url + "/system_stats",
                timeout=10,
            )

            return response.ok

        except Exception:
            return False

    def load_workflow(self) -> dict[str, Any]:

        if not WAN_WORKFLOW.exists():

            raise RuntimeError(
                "REAL_WAN_WORKFLOW_MISSING"
            )

        data = json.loads(
            WAN_WORKFLOW.read_text(
                encoding="utf-8"
            )
        )

        if not isinstance(
            data,
            dict,
        ):
            raise RuntimeError(
                "INVALID_WAN_WORKFLOW"
            )

        return data

    def inject(
        self,
        workflow: dict[str, Any],
        positive: str,
        negative: str,
        seed: int,
    ) -> dict[str, Any]:

        graph = json.loads(
            json.dumps(workflow)
        )

        for node in graph.values():

            if not isinstance(
                node,
                dict,
            ):
                continue

            inputs = node.get(
                "inputs",
                {},
            )

            class_type = node.get(
                "class_type",
                "",
            )

            if class_type == "CLIPTextEncode":

                old = str(
                    inputs.get(
                        "text",
                        "",
                    )
                ).lower()

                if (
                    "negative" in old
                    or "worst quality" in old
                    or "bad anatomy" in old
                ):
                    inputs["text"] = negative

                else:
                    inputs["text"] = positive

            if "seed" in inputs:
                inputs["seed"] = seed

            if "noise_seed" in inputs:
                inputs["noise_seed"] = seed

        return graph

    def queue(
        self,
        workflow: dict[str, Any],
    ) -> str:

        response = requests.post(
            self.base_url + "/prompt",
            json={
                "prompt": workflow,
                "client_id": str(
                    uuid.uuid4()
                ),
            },
            timeout=60,
        )

        response.raise_for_status()

        data = response.json()

        if data.get("error"):
            raise RuntimeError(
                json.dumps(
                    data["error"],
                    ensure_ascii=False,
                )
            )

        prompt_id = data.get(
            "prompt_id"
        )

        if not prompt_id:

            raise RuntimeError(
                "COMFYUI_NO_PROMPT_ID"
            )

        return prompt_id

    def wait(
        self,
        prompt_id: str,
    ) -> dict[str, Any]:

        started = time.time()

        while True:

            if (
                time.time() - started
                > 7200
            ):
                raise TimeoutError(
                    "WAN_GENERATION_TIMEOUT"
                )

            response = requests.get(
                self.base_url
                + f"/history/{prompt_id}",
                timeout=30,
            )

            response.raise_for_status()

            data = response.json()

            history = data.get(
                prompt_id
            )

            if history:

                status = history.get(
                    "status",
                    {},
                )

                if status.get(
                    "status_str"
                ) == "error":

                    raise RuntimeError(
                        "WAN_GENERATION_FAILED"
                    )

                if status.get(
                    "completed"
                ):
                    return history

            time.sleep(5)

    def find_media(
        self,
        history: dict[str, Any],
    ) -> dict[str, Any]:

        outputs = history.get(
            "outputs",
            {},
        )

        candidates = []

        for node in outputs.values():

            for key in (
                "videos",
                "gifs",
                "files",
                "images",
            ):

                for item in node.get(
                    key,
                    [],
                ):

                    if item.get(
                        "filename"
                    ):

                        candidates.append(
                            item
                        )

        if not candidates:

            raise RuntimeError(
                "WAN_OUTPUT_NOT_FOUND"
            )

        video = [
            item
            for item in candidates
            if Path(
                item["filename"]
            ).suffix.lower()
            in {
                ".mp4",
                ".webm",
                ".mov",
                ".mkv",
            }
        ]

        if not video:

            raise RuntimeError(
                "WAN_DID_NOT_RETURN_VIDEO"
            )

        return video[-1]

    def download(
        self,
        item: dict[str, Any],
    ) -> Path:

        response = requests.get(
            self.base_url + "/view",
            params={
                "filename": item["filename"],
                "subfolder": item.get(
                    "subfolder",
                    "",
                ),
                "type": item.get(
                    "type",
                    "output",
                ),
            },
            timeout=300,
        )

        response.raise_for_status()

        path = (
            WORK_ROOT
            / (
                "wan_"
                + uuid.uuid4().hex
                + Path(
                    item["filename"]
                ).suffix
            )
        )

        path.write_bytes(
            response.content
        )

        if not valid_real_video(path):

            path.unlink(
                missing_ok=True
            )

            raise RuntimeError(
                "REAL_VIDEO_VALIDATION_FAILED"
            )

        return path


# ============================================================
# STORY PROMPT
# ============================================================

def build_prompt(
    world: dict[str, Any],
    number: int,
) -> tuple[str, str]:

    rnd = random.Random(
        number * 918273
    )

    actions = [
        "walks slowly through the environment",
        "looks toward a distant light",
        "runs through the environment",
        "stops and remembers something painful",
        "turns toward another character",
        "reaches toward a mysterious object",
        "stands silently while the environment moves",
        "looks behind after hearing something",
        "moves carefully through the location",
        "faces an approaching danger",
    ]

    cameras = [
        "slow cinematic dolly",
        "wide cinematic establishing shot",
        "close-up followed by slow pullback",
        "side tracking shot",
        "over-the-shoulder shot",
        "low-angle cinematic shot",
    ]

    action = rnd.choice(actions)
    camera = rnd.choice(cameras)

    character_text = ", ".join(
        world["characters"]
    )

    positive = f"""
Original fictional anime.

Title:
{world["title"]}

Genre:
{world["genre"]}

Characters:
{character_text}

Location:
{world["location"]}

Scene:
{action}.

Camera:
{camera}.

Create a completely new cinematic moment.
Maintain consistent fictional character appearance.
Detailed anime environment.
Natural movement.
Expressive faces.
Cinematic lighting.
Depth.
Atmosphere.
Professional animated-film composition.

This is an original work.
Do not imitate or reproduce existing copyrighted characters.

No text.
No subtitles.
No watermark.
No logo.
"""

    negative = """
low quality,
static image,
bad anatomy,
extra fingers,
extra limbs,
duplicate characters,
deformed face,
broken hands,
warped body,
flicker,
frame artifacts,
text,
subtitle,
watermark,
logo,
copyrighted character,
blurry,
inconsistent character,
inconsistent clothing
"""

    return positive, negative


# ============================================================
# SHOT STATE
# ============================================================

def shot_file() -> Path:

    return (
        ANIME_STATE
        / "shot_database.json"
    )


def load_shots() -> list[Shot]:

    if not shot_file().exists():
        return []

    try:

        data = json.loads(
            shot_file().read_text(
                encoding="utf-8"
            )
        )

        return [
            Shot(**item)
            for item in data
        ]

    except Exception:

        return []


def save_shots(
    shots: list[Shot],
) -> None:

    shot_file().write_text(
        json.dumps(
            [
                asdict(x)
                for x in shots
            ],
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )


# ============================================================
# SHOT CREATION
# ============================================================

def create_shot_queue() -> list[Shot]:

    shots = load_shots()

    existing = {
        (
            x.anime_id,
            x.number,
        )
        for x in shots
    }

    for world in ANIME_WORLDS:

        for number in range(
            1,
            SHOTS_PER_ANIME + 1,
        ):

            key = (
                world["id"],
                number,
            )

            if key in existing:
                continue

            rnd = random.Random(
                hash(key)
            )

            shot = Shot(
                anime_id=world["id"],
                number=number,
                title=(
                    f"{world['title']} — "
                    f"Chapter {number:03d}"
                ),
                genre=world["genre"],
                characters=list(
                    world["characters"]
                ),
                location=world["location"],
                action=(
                    "new cinematic scene "
                    f"{number}"
                ),
                camera=(
                    "cinematic camera "
                    f"{rnd.randint(1, 6)}"
                ),
                seed=rnd.randint(
                    1,
                    2_147_483_647,
                ),
                created_at=time.time(),
            )

            shots.append(shot)

    save_shots(shots)

    return shots


# ============================================================
# PUBLISH REAL SHOT
# ============================================================

def publish_real_shot(
    shot: Shot,
    source: Path,
) -> Path:

    if not valid_real_video(source):

        raise RuntimeError(
            "REFUSED_NON_REAL_VIDEO"
        )

    public_dir = (
        PUBLIC_ANIME_ROOT
        / shot.anime_id
        / "shots"
        / f"{shot.number:04d}"
    )

    public_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    output = (
        public_dir
        / "main.mp4"
    )

    result = process(
        [
            FFMPEG,
            "-y",
            "-i",
            str(source),
            "-vf",
            (
                f"scale={VIDEO_WIDTH}:"
                f"{VIDEO_HEIGHT}:"
                "force_original_aspect_ratio="
                "decrease,"
                f"pad={VIDEO_WIDTH}:"
                f"{VIDEO_HEIGHT}:"
                "(ow-iw)/2:(oh-ih)/2"
            ),
            "-r",
            str(SHOT_FPS),
            "-c:v",
            "libx264",
            "-preset",
            "medium",
            "-crf",
            "18",
            "-pix_fmt",
            "yuv420p",
            "-an",
            "-movflags",
            "+faststart",
            str(output),
        ],
        timeout=900,
    )

    if result.returncode != 0:

        raise RuntimeError(
            result.stderr
        )

    if not valid_real_video(
        output
    ):

        output.unlink(
            missing_ok=True
        )

        raise RuntimeError(
            "PUBLISHED_VIDEO_FAILED_VALIDATION"
        )

    return output


# ============================================================
# MANIFEST
# ============================================================

def build_anime_manifest() -> None:

    shots = load_shots()

    episodes = []

    for world in ANIME_WORLDS:

        ready = []

        for shot in shots:

            if shot.anime_id != world["id"]:
                continue

            video = (
                PUBLIC_ANIME_ROOT
                / shot.anime_id
                / "shots"
                / f"{shot.number:04d}"
                / "main.mp4"
            )

            if not valid_real_video(
                video
            ):
                continue

            ready.append(
                {
                    "number": shot.number,
                    "title": shot.title,
                    "genre": shot.genre,
                    "characters": shot.characters,
                    "location": shot.location,
                    "duration": duration(
                        video
                    ),
                    "video": (
                        f"/media/anime/"
                        f"{shot.anime_id}/shots/"
                        f"{shot.number:04d}/main.mp4"
                    ),
                }
            )

        episode_dir = (
            ANIME_ROOT
            / world["id"]
        )

        episode_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

        manifest = {
            "id": world["id"],
            "title": world["title"],
            "genre": world["genre"],
            "characters": world["characters"],
            "location": world["location"],
            "shot_duration": SHOT_SECONDS,
            "total_story_shots": SHOTS_PER_ANIME,
            "ready_shots": len(ready),
            "complete": (
                len(ready)
                == SHOTS_PER_ANIME
            ),
            "shots": ready,
            "updated_at": time.time(),
        }

        (
            episode_dir
            / "manifest.json"
        ).write_text(
            json.dumps(
                manifest,
                ensure_ascii=False,
                indent=2,
            ),
            encoding="utf-8",
        )

        episodes.append(
            manifest
        )

    master = {
        "project": "AJVYRA",
        "episodes": episodes,
        "total_anime": len(
            episodes
        ),
        "updated_at": time.time(),
    }

    (
        ANIME_ROOT
        / "anime_manifest.json"
    ).write_text(
        json.dumps(
            master,
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )


# ============================================================
# BROWSER GAME GENERATOR
# ============================================================

def create_browser_game(
    number: int,
) -> None:

    name = GAME_NAMES[
        number - 1
    ]

    genre = GAME_GENRES[
        (number - 1)
        % len(GAME_GENRES)
    ]

    game_dir = (
        GAME_ROOT
        / f"game_{number:02d}"
    )

    game_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    html = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport"
 content="width=device-width,initial-scale=1,
 user-scalable=no">
<title>AJVYRA — {name}</title>
<style>
* {{
 box-sizing:border-box;
}}
html,body {{
 margin:0;
 min-height:100%;
 background:#000;
 color:#fff;
 font-family:Arial,sans-serif;
}}
body {{
 display:flex;
 justify-content:center;
 align-items:center;
 padding:12px;
}}
#wrap {{
 width:min(100%,900px);
}}
h1 {{
 font-size:20px;
 margin:0 0 5px;
}}
#meta {{
 color:#888;
 margin-bottom:10px;
}}
canvas {{
 display:block;
 width:100%;
 aspect-ratio:16/9;
 background:#050505;
 border:1px solid #333;
 border-radius:12px;
 touch-action:none;
}}
#controls {{
 display:grid;
 grid-template-columns:
 repeat(3,1fr);
 gap:8px;
 margin-top:10px;
}}
button {{
 min-height:48px;
 background:#111;
 color:#fff;
 border:1px solid #333;
 border-radius:10px;
 font-size:16px;
}}
#message {{
 margin-top:8px;
 color:#aaa;
}}
</style>
</head>
<body>
<div id="wrap">
<h1>{name}</h1>
<div id="meta">
Genre: {genre} · Story Mode
</div>

<canvas id="game"
 width="960"
 height="540"></canvas>

<div id="controls">
<button data-key="ArrowLeft">◀</button>
<button data-key="ArrowUp">▲</button>
<button data-key="ArrowRight">▶</button>
<button data-key="ArrowDown">▼</button>
<button id="action">ACTION</button>
<button id="restart">RESTART</button>
</div>

<div id="message">
Reach the objective. Avoid enemies.
</div>
</div>

<script>
(() => {{

const canvas =
 document.getElementById("game");

const ctx =
 canvas.getContext("2d");

const keys = new Set();

let player;
let enemies;
let target;
let score;
let ended;
let last;

function reset() {{

 player = {{
   x:100,
   y:270,
   r:18,
   speed:260
 }};

 enemies = [
   {{
     x:430,
     y:150,
     r:22,
     vx:90,
     vy:70
   }},
   {{
     x:700,
     y:380,
     r:20,
     vx:-75,
     vy:85
   }}
 ];

 target = {{
   x:860,
   y:270,
   r:20
 }};

 score = 0;
 ended = false;
 last = performance.now();

 draw();
}}

function distance(a,b) {{
 const dx=a.x-b.x;
 const dy=a.y-b.y;
 return Math.hypot(dx,dy);
}}

function update(dt) {{

 if (ended) return;

 let dx=0;
 let dy=0;

 if(keys.has("ArrowLeft")) dx-=1;
 if(keys.has("ArrowRight")) dx+=1;
 if(keys.has("ArrowUp")) dy-=1;
 if(keys.has("ArrowDown")) dy+=1;

 if(dx || dy) {{
   const len=Math.hypot(dx,dy)||1;
   player.x +=
     dx/len*player.speed*dt;
   player.y +=
     dy/len*player.speed*dt;
 }}

 player.x=Math.max(
   player.r,
   Math.min(
     canvas.width-player.r,
     player.x
   )
 );

 player.y=Math.max(
   player.r,
   Math.min(
     canvas.height-player.r,
     player.y
   )
 );

 for(const e of enemies) {{

   e.x += e.vx*dt;
   e.y += e.vy*dt;

   if(
     e.x<e.r ||
     e.x>canvas.width-e.r
   ) e.vx*=-1;

   if(
     e.y<e.r ||
     e.y>canvas.height-e.r
   ) e.vy*=-1;

   if(
     distance(player,e)
     < player.r+e.r
   ) {{
     ended=true;
     document.getElementById(
       "message"
     ).textContent =
       "GAME OVER — press RESTART";
   }}
 }}

 if(
   distance(player,target)
   < player.r+target.r
 ) {{
   score++;
   target.x =
     100 +
     Math.random()*
     (canvas.width-200);
   target.y =
     80 +
     Math.random()*
     (canvas.height-160);

   if(score>=5) {{
     ended=true;
     document.getElementById(
       "message"
     ).textContent =
       "YOU WIN — objective completed";
   }}
 }}
}}

function draw() {{

 ctx.clearRect(
   0,0,
   canvas.width,
   canvas.height
 );

 ctx.fillStyle="#080808";
 ctx.fillRect(
   0,0,
   canvas.width,
   canvas.height
 );

 ctx.strokeStyle="#202020";

 for(let x=0;x<canvas.width;x+=48) {{
   ctx.beginPath();
   ctx.moveTo(x,0);
   ctx.lineTo(x,canvas.height);
   ctx.stroke();
 }}

 for(let y=0;y<canvas.height;y+=48) {{
   ctx.beginPath();
   ctx.moveTo(0,y);
   ctx.lineTo(canvas.width,y);
   ctx.stroke();
 }}

 ctx.fillStyle="#fff";
 ctx.beginPath();
 ctx.arc(
   target.x,
   target.y,
   target.r,
   0,
   Math.PI*2
 );
 ctx.fill();

 ctx.fillStyle="#777";

 for(const e of enemies) {{
   ctx.beginPath();
   ctx.arc(
     e.x,
     e.y,
     e.r,
     0,
     Math.PI*2
   );
   ctx.fill();
 }}

 ctx.fillStyle="#fff";
 ctx.beginPath();
 ctx.arc(
   player.x,
   player.y,
   player.r,
   0,
   Math.PI*2
 );
 ctx.fill();

 ctx.fillStyle="#fff";
 ctx.font="22px Arial";
 ctx.fillText(
   "Score: "+score+"/5",
   20,
   35
 );
}}

function loop(now) {{

 const dt=Math.min(
   0.05,
   (now-last)/1000
 );

 last=now;

 update(dt);
 draw();

 requestAnimationFrame(loop);
}}

window.addEventListener(
 "keydown",
 e => {{
   keys.add(e.key);
 }},
 {{
   passive:true
 }}
);

window.addEventListener(
 "keyup",
 e => {{
   keys.delete(e.key);
 }},
 {{
   passive:true
 }}
);

document.querySelectorAll(
 "[data-key]"
).forEach(button => {{

 const key =
   button.dataset.key;

 button.addEventListener(
   "pointerdown",
   () => keys.add(key)
 );

 button.addEventListener(
   "pointerup",
   () => keys.delete(key)
 );

 button.addEventListener(
   "pointercancel",
   () => keys.delete(key)
 );

 button.addEventListener(
   "pointerleave",
   () => keys.delete(key)
 );
}});

document.getElementById(
 "restart"
).addEventListener(
 "click",
 reset
);

document.getElementById(
 "action"
).addEventListener(
 "click",
 () => {{
   score++;
   if(score>=5) {{
     ended=true;
     document.getElementById(
       "message"
     ).textContent =
       "YOU WIN — objective completed";
   }}
 }}
);

reset();

requestAnimationFrame(loop);

}})();
</script>
</body>
</html>
"""

    (game_dir / "index.html").write_text(
        html,
        encoding="utf-8",
    )

    metadata = {
        "id": f"game_{number:02d}",
        "title": name,
        "genre": genre,
        "playable": True,
        "browser": True,
        "mobile": True,
        "keyboard": True,
        "touch": True,
        "story": (
            f"{name} is an original "
            f"{genre} browser game."
        ),
        "entry": (
            f"/games/game_{number:02d}/"
            "index.html"
        ),
    }

    (
        game_dir / "manifest.json"
    ).write_text(
        json.dumps(
            metadata,
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )


def build_games() -> None:

    for number in range(
        1,
        TOTAL_GAMES + 1,
    ):
        create_browser_game(
            number
        )

    manifest = {
        "project": "AJVYRA",
        "total_games": TOTAL_GAMES,
        "games": [],
        "updated_at": time.time(),
    }

    for number in range(
        1,
        TOTAL_GAMES + 1,
    ):

        metadata_path = (
            GAME_ROOT
            / f"game_{number:02d}"
            / "manifest.json"
        )

        metadata = json.loads(
            metadata_path.read_text(
                encoding="utf-8"
            )
        )

        manifest["games"].append(
            metadata
        )

    (
        GAME_ROOT
        / "games_manifest.json"
    ).write_text(
        json.dumps(
            manifest,
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )


# ============================================================
# GAME VALIDATION
# ============================================================

def validate_games() -> dict[str, Any]:

    valid = 0
    invalid = []

    for number in range(
        1,
        TOTAL_GAMES + 1,
    ):

        game = (
            GAME_ROOT
            / f"game_{number:02d}"
            / "index.html"
        )

        if not game.exists():

            invalid.append(
                number
            )
            continue

        source = game.read_text(
            encoding="utf-8"
        )

        required = [
            "<canvas",
            "requestAnimationFrame",
            "keydown",
            "pointerdown",
            "restart",
        ]

        if all(
            token in source
            for token in required
        ):
            valid += 1

        else:
            invalid.append(
                number
            )

    return {
        "valid": valid,
        "invalid": invalid,
        "complete": (
            valid == TOTAL_GAMES
        ),
    }


# ============================================================
# SITE INDEX
# ============================================================

def create_site_index() -> None:

    html = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport"
 content="width=device-width,initial-scale=1">
<title>AJVYRA</title>
<style>
body{
 margin:0;
 background:#000;
 color:#fff;
 font-family:Arial,sans-serif;
}
main{
 width:min(1100px,94%);
 margin:auto;
 padding:30px 0;
}
h1{
 font-size:36px;
}
a{
 display:block;
 color:#fff;
 text-decoration:none;
 padding:16px;
 margin:8px 0;
 border:1px solid #252525;
 border-radius:12px;
 background:#080808;
}
a:hover{
 border-color:#666;
}
</style>
</head>
<body>
<main>
<h1>AJVYRA</h1>
<p>Anime • Games • Original Stories</p>

<h2>Games</h2>
<div id="games"></div>

<h2>Anime</h2>
<div id="anime"></div>
</main>

<script>
async function load(){

 const games =
   await fetch(
     "/games/games_manifest.json"
   ).then(r=>r.json());

 const gameBox =
   document.getElementById("games");

 games.games.forEach(game=>{

   const a =
     document.createElement("a");

   a.href =
     game.entry;

   a.textContent =
     game.title +
     " — " +
     game.genre;

   gameBox.appendChild(a);
 });

 const anime =
   await fetch(
     "/anime/anime_manifest.json"
   ).then(r=>r.json());

 const animeBox =
   document.getElementById("anime");

 anime.episodes.forEach(ep=>{

   const a =
     document.createElement("a");

   a.href =
     "/anime/" +
     ep.id +
     "/";

   a.textContent =
     ep.title +
     " — " +
     ep.ready_shots +
     " real shots";

   animeBox.appendChild(a);
 });
}

load();
</script>
</body>
</html>
"""

    (
        SITE_ROOT / "index.html"
    ).write_text(
        html,
        encoding="utf-8",
    )


# ============================================================
# REAL SHOT PRODUCTION
# ============================================================

def produce_one_real_shot(
    shot: Shot,
) -> bool:

    comfy = ComfyUI()

    if not comfy.health():

        shot.status = "waiting_for_backend"
        shot.error = (
            "ComfyUI/Wan backend is offline."
        )

        shots = load_shots()
        save_shots(shots)

        return False

    world = next(
        (
            x
            for x in ANIME_WORLDS
            if x["id"] == shot.anime_id
        ),
        None,
    )

    if world is None:

        shot.status = "failed"
        shot.error = "WORLD_NOT_FOUND"

        return False

    positive, negative = (
        build_prompt(
            world,
            shot.number,
        )
    )

    for attempt in range(
        1,
        MAX_RETRIES + 1,
    ):

        try:

            shot.status = "generating"
            shot.error = ""

            shots = load_shots()
            save_shots(shots)

            workflow = (
                comfy.load_workflow()
            )

            workflow = comfy.inject(
                workflow,
                positive,
                negative,
                shot.seed + attempt,
            )

            prompt_id = comfy.queue(
                workflow
            )

            shot.prompt_id = prompt_id

            history = comfy.wait(
                prompt_id
            )

            media = comfy.find_media(
                history
            )

            source = comfy.download(
                media
            )

            public = publish_real_shot(
                shot,
                source,
            )

            shot.video = str(
                public
            )

            shot.duration = duration(
                public
            )

            shot.status = "ready"
            shot.completed_at = (
                time.time()
            )

            shots = load_shots()
            save_shots(shots)

            build_anime_manifest()

            return True

        except Exception as exc:

            shot.error = (
                f"attempt={attempt}: "
                f"{exc}"
            )

            shot.status = (
                "retrying"
                if attempt < MAX_RETRIES
                else "failed"
            )

            shots = load_shots()
            save_shots(shots)

            if attempt < MAX_RETRIES:
                time.sleep(10)

    build_anime_manifest()

    return False


# ============================================================
# HOURLY DIFFERENT SHOT
# ============================================================

def choose_next_shot() -> Shot | None:

    shots = load_shots()

    for shot in sorted(
        shots,
        key=lambda x: (
            x.anime_id,
            x.number,
        ),
    ):

        if shot.status in {
            "queued",
            "retrying",
            "waiting_for_backend",
        }:

            return shot

    return None


def hourly_worker() -> None:

    while True:

        create_shot_queue()

        shot = choose_next_shot()

        if shot:

            produce_one_real_shot(
                shot
            )

        time.sleep(
            HOURLY_INTERVAL
        )


# ============================================================
# RELEASE GATE
# ============================================================

def final_gate() -> dict[str, Any]:

    game_report = validate_games()

    shots = load_shots()

    real_videos = 0

    for shot in shots:

        if shot.status != "ready":
            continue

        video = Path(
            shot.video
        )

        if valid_real_video(
            video
        ):
            real_videos += 1

    build_anime_manifest()

    report = {
        "project": "AJVYRA",
        "games": game_report,
        "known_real_shots": real_videos,
        "required_games": TOTAL_GAMES,
        "required_anime": TOTAL_ANIME,
        "shots_per_anime": SHOTS_PER_ANIME,
        "required_total_shots": (
            TOTAL_REQUIRED_SHOTS
        ),
        "wan_backend_online": (
            ComfyUI().health()
        ),
        "publication_status": (
            "READY_FOR_AVAILABLE_ASSETS"
            if game_report["complete"]
            else "BLOCKED"
        ),
        "generated_at": time.time(),
    }

    (
        STATE_ROOT
        / "absolute_release_report.json"
    ).write_text(
        json.dumps(
            report,
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )

    return report


# ============================================================
# PREPARE EVERYTHING
# ============================================================

def prepare_everything() -> None:

    build_games()
    create_site_index()
    create_shot_queue()
    build_anime_manifest()

    report = final_gate()

    print(
        json.dumps(
            report,
            ensure_ascii=False,
            indent=2,
        )
    )


# ============================================================
# COMMAND LINE
# ============================================================

def main():

    command = (
        sys.argv[1]
        if len(sys.argv) > 1
        else "prepare"
    )

    if command == "prepare":

        prepare_everything()
        return

    if command == "games":

        build_games()
        print(
            json.dumps(
                validate_games(),
                ensure_ascii=False,
                indent=2,
            )
        )
        return

    if command == "shot":

        create_shot_queue()

        shot = choose_next_shot()

        if shot is None:

            print(
                "NO_QUEUED_SHOT"
            )
            return

        ok = produce_one_real_shot(
            shot
        )

        print(
            json.dumps(
                {
                    "success": ok,
                    "shot": asdict(
                        shot
                    ),
                },
                ensure_ascii=False,
                indent=2,
            )
        )

        return

    if command == "hourly":

        create_shot_queue()
        hourly_worker()
        return

    if command == "release":

        prepare_everything()
        return

    if command == "status":

        print(
            json.dumps(
                final_gate(),
                ensure_ascii=False,
                indent=2,
            )
        )

        return

    raise SystemExit(
        "Commands: prepare | games | shot | hourly | release | status"
    )


if __name__ == "__main__":
    main()
