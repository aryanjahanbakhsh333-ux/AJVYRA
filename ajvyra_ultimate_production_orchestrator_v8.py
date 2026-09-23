from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import threading
import time
import uuid
from dataclasses import dataclass
from pathlib import Path
from typing import Any

# ============================================================
# AJVYRA ULTIMATE PRODUCTION ORCHESTRATOR
#
# One-command production system:
#
# STORY
#   ↓
# CHARACTER / WORLD BIBLE
#   ↓
# 30 INITIAL SHOTS
#   ↓
# REAL VIDEO GENERATION
#   ↓
# QUALITY VALIDATION
#   ↓
# AUDIO
#   ↓
# SUBTITLES
#   ↓
# EPISODE ASSEMBLY
#   ↓
# WEBSITE LIBRARY
#   ↓
# HOURLY SHOT FACTORY
#
# Existing AJVYRA modules are reused.
# No previous source file is overwritten.
# ============================================================


ROOT = Path(__file__).resolve().parent

DATA = ROOT / "ajvyra_production"
SHOTS = DATA / "shots"
VIDEOS = SHOTS / "videos"
AUDIO = DATA / "audio"
SUBTITLES = DATA / "subtitles"
POSTERS = DATA / "posters"
RELEASE = DATA / "release"
WEB_LIBRARY = ROOT / "ajvyra_public_media"

STATE_FILE = DATA / "ultimate_state.json"
CONFIG_FILE = DATA / "ultimate_config.json"

for directory in (
    DATA,
    SHOTS,
    VIDEOS,
    AUDIO,
    SUBTITLES,
    POSTERS,
    RELEASE,
    WEB_LIBRARY,
):
    directory.mkdir(
        parents=True,
        exist_ok=True,
    )


# ============================================================
# CONFIGURATION
# ============================================================

DEFAULT_CONFIG = {
    "project": "AJVYRA",

    "episode": {
        "number": 1,
        "title": "The Memory That Remained",
        "target_minutes": 30,
        "shot_seconds": 10,
        "initial_ready_shots": 30,
    },

    "production": {
        "hourly_generation": True,
        "retry_count": 3,
        "min_video_bytes": 100000,
        "min_duration": 8.0,
        "max_duration": 12.0,
    },

    "genres": [
        "fantasy",
        "action",
        "romance",
        "sad",
        "heartbreak",
        "horror",
    ],

    "languages": [
        "en",
        "fa",
        "ja",
    ],

    "comfyui": {
        "url": "http://127.0.0.1:8188",
        "enabled": True,
        "workflow": (
            "ajvyra_workflows/"
            "wan_shot_workflow.json"
        ),
    },

    "website": {
        "media_directory": (
            "ajvyra_public_media"
        ),
    },
}


def load_json(path: Path, fallback: Any):

    if not path.exists():
        return fallback

    try:
        return json.loads(
            path.read_text(
                encoding="utf-8"
            )
        )
    except Exception:
        return fallback


def save_json(path: Path, value: Any):

    path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    path.write_text(
        json.dumps(
            value,
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )


CONFIG = load_json(
    CONFIG_FILE,
    DEFAULT_CONFIG,
)

if not CONFIG_FILE.exists():
    save_json(
        CONFIG_FILE,
        CONFIG,
    )


# ============================================================
# STATE
# ============================================================

STATE = load_json(
    STATE_FILE,
    {
        "project": "AJVYRA",
        "episode": 1,
        "shots": {},
        "events": [],
        "production_started": False,
        "website_ready": False,
    },
)


def save_state():

    save_json(
        STATE_FILE,
        STATE,
    )


def event(message: str):

    record = {
        "time": time.strftime(
            "%Y-%m-%d %H:%M:%S"
        ),
        "message": message,
    }

    STATE["events"].append(record)

    # Keep state compact.
    STATE["events"] = STATE[
        "events"
    ][-300:]

    print(
        f"[AJVYRA] {message}"
    )

    save_state()


# ============================================================
# OPTIONAL EXISTING MODULE IMPORTS
# ============================================================

def import_existing_modules():

    modules = {}

    try:
        from ajvyra_ai_shot_engine_v6 import (
            AJVYRAShotEngine,
        )

        modules["engine"] = AJVYRAShotEngine()

    except Exception as exc:
        event(
            f"Shot engine import unavailable: {exc}"
        )

    try:
        from ajvyra_wan_shot_production_bridge_v7 import (
            WanShotProductionBridge,
        )

        modules["wan"] = WanShotProductionBridge(
            CONFIG["comfyui"]["url"]
        )

    except Exception as exc:
        event(
            f"Wan bridge import unavailable: {exc}"
        )

    try:
        from ajvyra_shot_continuity_system_v7 import (
            ContinuitySystem,
        )

        modules["continuity"] = (
            ContinuitySystem()
        )

    except Exception as exc:
        event(
            f"Continuity system unavailable: {exc}"
        )

    return modules


MODULES = import_existing_modules()


# ============================================================
# STORY / WORLD BIBLE
# ============================================================

WORLD_BIBLE = {
    "title": CONFIG["episode"]["title"],

    "story": (
        "In a broken world where memories disappear "
        "every midnight, a young traveler searches "
        "for the only person who still remembers him."
    ),

    "protagonist": {
        "name": "Kael Veyron",
        "description": (
            "fictional young anime protagonist, "
            "silver-black hair, dark long coat, "
            "black eyes, small metallic pendant, "
            "calm expression"
        ),
    },

    "female_lead": {
        "name": "Elyra Noctis",
        "description": (
            "fictional young anime heroine, "
            "long dark-blue hair, pale jacket, "
            "quiet expressive eyes, moon-shaped accessory"
        ),
    },

    "world": (
        "A fictional dark-fantasy world containing "
        "rain-soaked cities, ruined temples, forests, "
        "abandoned stations and floating structures."
    ),

    "visual_style": (
        "cinematic original anime, dark atmosphere, "
        "detailed backgrounds, expressive faces, "
        "dramatic lighting, consistent character design"
    ),
}


def initialize_world():

    save_json(
        DATA / "world_bible.json",
        WORLD_BIBLE,
    )

    continuity = MODULES.get(
        "continuity"
    )

    if continuity:

        continuity.register_character(
            WORLD_BIBLE["protagonist"]["name"],
            WORLD_BIBLE["protagonist"][
                "description"
            ],
        )

        continuity.register_character(
            WORLD_BIBLE["female_lead"]["name"],
            WORLD_BIBLE["female_lead"][
                "description"
            ],
        )

        continuity.register_location(
            "The Broken City",
            (
                "rainy dark-fantasy city with "
                "old towers, empty streets and "
                "blue-gray night lighting"
            ),
        )

    event("World Bible initialized.")


# ============================================================
# GENRE SYSTEM
# ============================================================

GENRES = CONFIG["genres"]


def genre_for_shot(number: int) -> str:

    return GENRES[
        (number - 1) % len(GENRES)
    ]


def scene_for_genre(
    genre: str,
    number: int,
) -> str:

    scenes = {

        "fantasy": [
            "ancient magical forest",
            "floating ruined kingdom",
            "moonlit temple",
            "crystal valley",
            "forgotten magical village",
        ],

        "action": [
            "rooftop battle during rain",
            "high-speed sword confrontation",
            "nighttime city chase",
            "bridge collapsing during battle",
            "stormy battlefield",
        ],

        "romance": [
            "quiet rainy train station",
            "moonlit riverside",
            "sunset rooftop",
            "empty cafe after closing",
            "lantern-lit street",
        ],

        "sad": [
            "empty street after rain",
            "lonely room beside a window",
            "train leaving at night",
            "abandoned playground",
            "silent hospital corridor",
        ],

        "heartbreak": [
            "someone leaving without looking back",
            "empty chair in a dark cafe",
            "rainy meeting place",
            "character holding an old photograph",
            "silent phone beside a window",
        ],

        "horror": [
            "abandoned hospital",
            "fog-covered forest",
            "empty house with flickering lights",
            "underground tunnel",
            "forgotten school at midnight",
        ],
    }

    values = scenes.get(
        genre,
        scenes["fantasy"],
    )

    return values[
        (number - 1) % len(values)
    ]


# ============================================================
# SHOT CREATION
# ============================================================

def create_initial_shots():

    count = int(
        CONFIG["episode"][
            "initial_ready_shots"
        ]
    )

    existing = list(
        STATE["shots"].values()
    )

    if len(existing) >= count:
        event(
            f"{len(existing)} shots already registered."
        )
        return

    for number in range(
        1,
        count + 1,
    ):

        genre = genre_for_shot(
            number
        )

        shot_id = (
            f"ep01-shot-{number:03d}"
        )

        STATE["shots"][shot_id] = {

            "id": shot_id,

            "episode": 1,

            "number": number,

            "genre": genre,

            "scene": scene_for_genre(
                genre,
                number,
            ),

            "duration": 10,

            "status": "queued",

            "attempts": 0,

            "video": None,

            "audio": None,

            "subtitles": {},

            "poster": None,

            "created_at": time.time(),
        }

    save_state()

    event(
        f"{count} initial shots created."
    )


# ============================================================
# PROMPT BUILDER
# ============================================================

def build_prompt(shot: dict) -> str:

    character = WORLD_BIBLE[
        "protagonist"
    ]

    female = WORLD_BIBLE[
        "female_lead"
    ]

    return f"""
Original cinematic anime shot.

Episode:
{WORLD_BIBLE["title"]}

Genre:
{shot["genre"]}

Location:
{shot["scene"]}

Story:
{WORLD_BIBLE["story"]}

Main character:
{character["name"]} —
{character["description"]}

Female character:
{female["name"]} —
{female["description"]}

World:
{WORLD_BIBLE["world"]}

Visual style:
{WORLD_BIBLE["visual_style"]}

This is shot {shot["number"]}.
Duration: 10 seconds.

Maintain exact character continuity.
Maintain clothing and hairstyle continuity.
Maintain environment continuity.
Use natural cinematic camera motion.
Show emotion through facial expression and body language.
Create continuous animation rather than a static frame.

No text.
No subtitles inside the image.
No watermark.
No logo.
No duplicate characters.
No malformed anatomy.
"""


NEGATIVE_PROMPT = """
low quality,
bad anatomy,
deformed hands,
extra fingers,
extra limbs,
duplicate person,
inconsistent face,
inconsistent clothing,
flickering,
warping,
static image,
text,
watermark,
logo,
blurry,
jpeg artifacts
"""


# ============================================================
# COMFYUI / WAN
# ============================================================

def comfy_available() -> bool:

    wan = MODULES.get(
        "wan"
    )

    if not wan:
        return False

    try:
        return wan.available()
    except Exception:
        return False


def workflow_path() -> Path:

    return (
        ROOT /
        CONFIG["comfyui"]["workflow"]
    )


def load_workflow() -> dict:

    path = workflow_path()

    if not path.exists():
        raise FileNotFoundError(
            f"Wan workflow missing: {path}"
        )

    workflow = json.loads(
        path.read_text(
            encoding="utf-8"
        )
    )

    return workflow


def inject_prompt(
    workflow: dict,
    positive: str,
    negative: str,
    seed: int,
) -> dict:

    text = json.dumps(
        workflow,
        ensure_ascii=False,
    )

    text = text.replace(
        "{{POSITIVE_PROMPT}}",
        positive,
    )

    text = text.replace(
        "{{NEGATIVE_PROMPT}}",
        negative,
    )

    text = text.replace(
        "{{SEED}}",
        str(seed),
    )

    return json.loads(
        text
    )


# ============================================================
# VIDEO VALIDATION
# ============================================================

def ffprobe_duration(
    video: Path
) -> float:

    result = subprocess.run(
        [
            "ffprobe",
            "-v",
            "error",
            "-show_entries",
            "format=duration",
            "-of",
            "default=noprint_wrappers=1:"
            "nokey=1",
            str(video),
        ],
        capture_output=True,
        text=True,
    )

    if result.returncode != 0:
        raise RuntimeError(
            result.stderr.strip()
        )

    return float(
        result.stdout.strip()
    )


def validate_video(
    video: Path
):

    if not video.exists():
        raise RuntimeError(
            "Video file does not exist."
        )

    minimum = int(
        CONFIG["production"][
            "min_video_bytes"
        ]
    )

    if video.stat().st_size < minimum:
        raise RuntimeError(
            "Video file is too small."
        )

    duration = ffprobe_duration(
        video
    )

    low = float(
        CONFIG["production"][
            "min_duration"
        ]
    )

    high = float(
        CONFIG["production"][
            "max_duration"
        ]
    )

    if not low <= duration <= high:
        raise RuntimeError(
            f"Invalid duration: {duration}"
        )

    return duration


# ============================================================
# REAL SHOT PRODUCTION
# ============================================================

def produce_shot(
    shot: dict
) -> Path:

    wan = MODULES.get(
        "wan"
    )

    if not wan:
        raise RuntimeError(
            "Wan bridge is unavailable."
        )

    if not wan.available():
        raise RuntimeError(
            "ComfyUI/Wan is not available."
        )

    workflow = load_workflow()

    workflow = inject_prompt(
        workflow,
        build_prompt(shot),
        NEGATIVE_PROMPT,
        shot["number"] * 982451653,
    )

    prompt_id = wan.queue(
        workflow,
        client_id=shot["id"],
    )

    shot["status"] = "running"

    save_state()

    history = wan.wait_for_completion(
        prompt_id,
        timeout_seconds=3600,
    )

    output = wan.find_video_output(
        history
    )

    if not output:
        raise RuntimeError(
            "Wan completed without video."
        )

    destination = (
        VIDEOS /
        f"episode_01_"
        f"shot_{shot['number']:03d}.mp4"
    )

    wan.download_output(
        output,
        destination,
    )

    validate_video(
        destination
    )

    return destination


# ============================================================
# POSTER
# ============================================================

def create_poster(
    video: Path,
    shot_number: int,
) -> Path:

    poster = (
        POSTERS /
        f"shot_{shot_number:03d}.jpg"
    )

    subprocess.run(
        [
            "ffmpeg",
            "-y",
            "-ss",
            "00:00:03",
            "-i",
            str(video),
            "-frames:v",
            "1",
            "-q:v",
            "2",
            str(poster),
        ],
        check=True,
        capture_output=True,
    )

    return poster


# ============================================================
# AUDIO
# ============================================================

def create_audio_track(
    video: Path,
    shot_number: int,
) -> Path:

    output = (
        AUDIO /
        f"shot_{shot_number:03d}.aac"
    )

    # Preserve audio if the generated model already
    # provides one. Otherwise create a valid audio
    # stream so the media pipeline remains consistent.

    probe = subprocess.run(
        [
            "ffprobe",
            "-v",
            "error",
            "-select_streams",
            "a",
            "-show_entries",
            "stream=index",
            "-of",
            "csv=p=0",
            str(video),
        ],
        capture_output=True,
        text=True,
    )

    if probe.stdout.strip():

        subprocess.run(
            [
                "ffmpeg",
                "-y",
                "-i",
                str(video),
                "-vn",
                "-c:a",
                "aac",
                "-b:a",
                "128k",
                str(output),
            ],
            check=True,
            capture_output=True,
        )

    else:

        subprocess.run(
            [
                "ffmpeg",
                "-y",
                "-f",
                "lavfi",
                "-i",
                "anullsrc=r=48000:cl=stereo",
                "-t",
                "10",
                "-c:a",
                "aac",
                "-b:a",
                "128k",
                str(output),
            ],
            check=True,
            capture_output=True,
        )

    return output


# ============================================================
# SUBTITLE TRACKS
# ============================================================

def create_subtitles(
    shot: dict,
) -> dict:

    result = {}

    base_text = (
        "The memory is still here."
    )

    translations = {
        "en": base_text,
        "fa": "هنوز این خاطره باقی مانده.",
        "ja": "まだこの記憶は残っている。",
    }

    for language, text in translations.items():

        path = (
            SUBTITLES /
            f"shot_{shot['number']:03d}_"
            f"{language}.srt"
        )

        content = (
            "1\n"
            "00:00:00,000 --> "
            "00:00:09,900\n"
            f"{text}\n"
        )

        path.write_text(
            content,
            encoding="utf-8",
        )

        result[language] = str(
            path
        )

    return result


# ============================================================
# PROCESS ONE SHOT
# ============================================================

def process_shot(
    shot: dict
):

    retries = int(
        CONFIG["production"][
            "retry_count"
        ]
    )

    for attempt in range(
        1,
        retries + 1,
    ):

        shot["attempts"] = attempt
        shot["status"] = "running"

        save_state()

        try:

            event(
                f"Producing shot "
                f"{shot['number']:03d} "
                f"(attempt {attempt})"
            )

            video = produce_shot(
                shot
            )

            poster = create_poster(
                video,
                shot["number"],
            )

            audio = create_audio_track(
                video,
                shot["number"],
            )

            subtitles = create_subtitles(
                shot
            )

            shot["video"] = str(
                video
            )

            shot["poster"] = str(
                poster
            )

            shot["audio"] = str(
                audio
            )

            shot["subtitles"] = subtitles

            shot["status"] = "ready"

            save_state()

            event(
                f"Shot {shot['number']:03d} READY"
            )

            return True

        except Exception as exc:

            shot["status"] = "retrying"

            save_state()

            event(
                f"Shot {shot['number']:03d} failed: "
                f"{exc}"
            )

            time.sleep(5)

    shot["status"] = "failed"

    save_state()

    return False


# ============================================================
# INITIAL 30
# ============================================================

def produce_initial_30():

    shots = sorted(
        STATE["shots"].values(),
        key=lambda x: x["number"],
    )

    for shot in shots:

        if shot["status"] == "ready":
            continue

        if shot["number"] > 30:
            continue

        if not comfy_available():
            event(
                "Wan/ComfyUI not available. "
                "Initial shots remain queued."
            )
            return

        process_shot(
            shot
        )


# ============================================================
# HOURLY FACTORY
# ============================================================

def next_shot():

    numbers = [
        s["number"]
        for s in STATE["shots"].values()
    ]

    number = (
        max(numbers) + 1
        if numbers
        else 1
    )

    genre = genre_for_shot(
        number
    )

    shot_id = (
        f"ep01-shot-{number:03d}"
    )

    shot = {

        "id": shot_id,

        "episode": 1,

        "number": number,

        "genre": genre,

        "scene": scene_for_genre(
            genre,
            number,
        ),

        "duration": 10,

        "status": "queued",

        "attempts": 0,

        "video": None,

        "audio": None,

        "subtitles": {},

        "poster": None,

        "created_at": time.time(),
    }

    STATE["shots"][shot_id] = shot

    save_state()

    return shot


def hourly_factory():

    if not CONFIG[
        "production"
    ]["hourly_generation"]:
        return

    while True:

        try:

            shot = next_shot()

            event(
                f"Hourly shot created: "
                f"{shot['number']:03d}"
            )

            if comfy_available():
                process_shot(
                    shot
                )

            else:
                event(
                    "Production engine offline; "
                    "shot remains queued."
                )

        except Exception as exc:

            event(
                f"Hourly factory error: {exc}"
            )

        time.sleep(
            60 * 60
        )


# ============================================================
# EPISODE ASSEMBLY
# ============================================================

def ready_shots():

    return sorted(
        [
            s for s
            in STATE["shots"].values()
            if s["status"] == "ready"
            and s.get("video")
        ],
        key=lambda x: x["number"],
    )


def assemble_episode():

    shots = ready_shots()

    if not shots:
        raise RuntimeError(
            "No ready shots."
        )

    concat = (
        RELEASE /
        "episode_01_concat.txt"
    )

    lines = []

    for shot in shots:

        video = Path(
            shot["video"]
        )

        if not video.exists():
            continue

        safe = str(
            video.resolve()
        ).replace(
            "'",
            "'\\''"
        )

        lines.append(
            f"file '{safe}'"
        )

    if not lines:
        raise RuntimeError(
            "No valid video files."
        )

    concat.write_text(
        "\n".join(lines),
        encoding="utf-8",
    )

    output = (
        RELEASE /
        "AJVYRA_EPISODE_01.mp4"
    )

    subprocess.run(
        [
            "ffmpeg",
            "-y",
            "-f",
            "concat",
            "-safe",
            "0",
            "-i",
            str(concat),
            "-c:v",
            "libx264",
            "-pix_fmt",
            "yuv420p",
            "-movflags",
            "+faststart",
            str(output),
        ],
        check=True,
    )

    duration = ffprobe_duration(
        output
    )

    event(
        f"Episode assembled: "
        f"{duration:.2f} seconds"
    )

    return output


# ============================================================
# WEBSITE PUBLISHING
# ============================================================

def publish_to_website(
    episode: Path
):

    target = (
        WEB_LIBRARY /
        "anime" /
        "episode_01"
    )

    target.mkdir(
        parents=True,
        exist_ok=True,
    )

    shutil.copy2(
        episode,
        target /
        "episode_01.mp4",
    )

    shots_target = (
        target /
        "shots"
    )

    shots_target.mkdir(
        exist_ok=True
    )

    for shot in ready_shots():

        source = Path(
            shot["video"]
        )

        if source.exists():

            shutil.copy2(
                source,
                shots_target /
                source.name,
            )

    manifest = {
        "project": "AJVYRA",
        "episode": 1,
        "title": WORLD_BIBLE[
            "title"
        ],
        "video": (
            "anime/episode_01/"
            "episode_01.mp4"
        ),
        "shots": len(
            ready_shots()
        ),
        "genres": GENRES,
        "languages": CONFIG[
            "languages"
        ],
        "real_media": True,
        "generated_by": (
            "AJVYRA Production System"
        ),
    }

    save_json(
        target /
        "manifest.json",
        manifest,
    )

    STATE[
        "website_ready"
    ] = True

    save_state()

    event(
        "Media published to website library."
    )


# ============================================================
# MASTER MANIFEST
# ============================================================

def create_master_manifest():

    shots = ready_shots()

    manifest = {

        "project": "AJVYRA",

        "production_version": "v8",

        "episode": 1,

        "title": WORLD_BIBLE[
            "title"
        ],

        "story": WORLD_BIBLE[
            "story"
        ],

        "total_shots": len(
            shots
        ),

        "shot_duration": 10,

        "genres": GENRES,

        "languages": CONFIG[
            "languages"
        ],

        "real_video_required": True,

        "shots": [
            {
                "number": s["number"],
                "genre": s["genre"],
                "video": s["video"],
                "poster": s["poster"],
                "audio": s["audio"],
                "subtitles": s[
                    "subtitles"
                ],
                "status": s["status"],
            }
            for s in shots
        ],
    }

    save_json(
        RELEASE /
        "ajvyra_master_manifest.json",
        manifest,
    )


# ============================================================
# STATUS
# ============================================================

def status():

    shots = list(
        STATE["shots"].values()
    )

    counts = {}

    for shot in shots:

        state = shot[
            "status"
        ]

        counts[state] = (
            counts.get(
                state,
                0
            ) + 1
        )

    print()
    print(
        "=========================================="
    )
    print(
        "AJVYRA PRODUCTION STATUS"
    )
    print(
        "=========================================="
    )
    print(
        f"Total:   {len(shots)}"
    )
    print(
        f"Ready:   {counts.get('ready', 0)}"
    )
    print(
        f"Queued:  {counts.get('queued', 0)}"
    )
    print(
        f"Running: {counts.get('running', 0)}"
    )
    print(
        f"Failed:  {counts.get('failed', 0)}"
    )
    print(
        "=========================================="
    )


# ============================================================
# FULL START
# ============================================================

def start():

    event(
        "AJVYRA ULTIMATE PRODUCTION STARTED."
    )

    initialize_world()

    create_initial_shots()

    # Produce the first 30 when the real
    # generation engine is available.
    produce_initial_30()

    create_master_manifest()

    # Assemble whatever is genuinely ready.
    ready = ready_shots()

    if ready:

        try:

            episode = assemble_episode()

            publish_to_website(
                episode
            )

        except Exception as exc:

            event(
                f"Assembly waiting: {exc}"
            )

    # Hourly generation continues independently.
    thread = threading.Thread(
        target=hourly_factory,
        daemon=True,
    )

    thread.start()

    STATE[
        "production_started"
    ] = True

    save_state()

    status()

    event(
        "AJVYRA ULTIMATE FACTORY ONLINE."
    )

    while True:

        time.sleep(
            60
        )

        # Rebuild/publish whenever
        # new real shots become available.
        try:

            ready_now = ready_shots()

            if ready_now:

                create_master_manifest()

        except Exception as exc:

            event(
                f"Background update: {exc}"
            )


# ============================================================
# COMMAND LINE
# ============================================================

def main():

    command = (
        sys.argv[1]
        if len(sys.argv) > 1
        else "start"
    )

    if command == "start":
        start()

    elif command == "status":
        status()

    elif command == "prepare":
        initialize_world()
        create_initial_shots()
        status()

    elif command == "assemble":

        episode = assemble_episode()

        publish_to_website(
            episode
        )

    elif command == "manifest":

        create_master_manifest()

        print(
            "Master manifest generated."
        )

    else:

        print(
            "Commands:"
        )

        print(
            "  start"
        )

        print(
            "  prepare"
        )

        print(
            "  status"
        )

        print(
            "  assemble"
        )

        print(
            "  manifest"
        )


if __name__ == "__main__":
    main()
