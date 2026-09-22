"""
AJVYRA Real Anime Production Engine

A provider-agnostic production orchestrator for real anime media generation.
This module owns the production logic: story -> scenes -> shots -> references
-> media generation -> audio -> subtitles -> timeline -> render -> QC.

No API keys are stored here. Providers are selected through environment variables.
The engine supports a deterministic LOCAL mode for development and real provider
adapters through HTTP when credentials/endpoints are configured.

This is an orchestration engine, not a claim that a neural video model is
implemented in pure Python. Real image/video generation requires a configured
provider or a locally hosted model endpoint.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import logging
import os
import shutil
import subprocess
import time
import uuid
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Protocol, Sequence, Tuple
from urllib import error as urlerror
from urllib import request as urlrequest


LOGGER = logging.getLogger("ajvyra.anime.production")


# ---------------------------------------------------------------------------
# Data contracts
# ---------------------------------------------------------------------------

@dataclass
class ProductionConfig:
    root: Path = Path("generated/anime_production")
    provider_mode: str = "local"  # local | http | auto
    image_provider: str = ""
    video_provider: str = ""
    voice_provider: str = ""
    music_provider: str = ""
    image_endpoint: str = ""
    video_endpoint: str = ""
    voice_endpoint: str = ""
    music_endpoint: str = ""
    api_timeout_seconds: int = 180
    poll_interval_seconds: int = 5
    max_retries: int = 3
    episode_minutes: float = 30.0
    target_fps: int = 24
    resolution: str = "1920x1080"
    aspect_ratio: str = "16:9"
    languages: Tuple[str, ...] = ("fa", "ja", "en")
    render_enabled: bool = True
    keep_intermediates: bool = True

    @classmethod
    def from_env(cls, **overrides: Any) -> "ProductionConfig":
        values: Dict[str, Any] = {
            "provider_mode": os.getenv("AJVYRA_PROVIDER_MODE", "local"),
            "image_provider": os.getenv("AJVYRA_IMAGE_PROVIDER", ""),
            "video_provider": os.getenv("AJVYRA_VIDEO_PROVIDER", ""),
            "voice_provider": os.getenv("AJVYRA_VOICE_PROVIDER", ""),
            "music_provider": os.getenv("AJVYRA_MUSIC_PROVIDER", ""),
            "image_endpoint": os.getenv("AJVYRA_IMAGE_ENDPOINT", ""),
            "video_endpoint": os.getenv("AJVYRA_VIDEO_ENDPOINT", ""),
            "voice_endpoint": os.getenv("AJVYRA_VOICE_ENDPOINT", ""),
            "music_endpoint": os.getenv("AJVYRA_MUSIC_ENDPOINT", ""),
            "api_timeout_seconds": int(os.getenv("AJVYRA_API_TIMEOUT", "180")),
            "poll_interval_seconds": int(os.getenv("AJVYRA_POLL_INTERVAL", "5")),
            "max_retries": int(os.getenv("AJVYRA_MAX_RETRIES", "3")),
            "episode_minutes": float(os.getenv("AJVYRA_EPISODE_MINUTES", "30")),
            "target_fps": int(os.getenv("AJVYRA_FPS", "24")),
            "resolution": os.getenv("AJVYRA_RESOLUTION", "1920x1080"),
            "aspect_ratio": os.getenv("AJVYRA_ASPECT_RATIO", "16:9"),
            "render_enabled": os.getenv("AJVYRA_RENDER", "1") not in {"0", "false", "no"},
        }
        values.update(overrides)
        return cls(**values)


@dataclass
class CharacterSpec:
    character_id: str
    name: str
    role: str
    age_range: str = "young adult"
    gender_presentation: str = "unspecified"
    personality: List[str] = field(default_factory=list)
    appearance: Dict[str, Any] = field(default_factory=dict)
    wardrobe: Dict[str, Any] = field(default_factory=dict)
    voice_identity: str = ""
    reference_images: List[str] = field(default_factory=list)
    reference_seed: str = ""


@dataclass
class LocationSpec:
    location_id: str
    name: str
    description: str
    visual_style: str = "cinematic anime"
    time_of_day: str = "day"
    weather: str = "clear"
    reference_images: List[str] = field(default_factory=list)


@dataclass
class DialogueLine:
    speaker_id: str
    text: str
    start: float = 0.0
    end: float = 0.0
    emotion: str = "neutral"


@dataclass
class ShotSpec:
    anime_id: str
    episode_id: str
    scene_id: str
    shot_id: str
    index: int
    duration: float
    prompt: str
    action: str
    camera: Dict[str, Any] = field(default_factory=dict)
    lighting: str = "cinematic"
    emotion: str = "neutral"
    character_ids: List[str] = field(default_factory=list)
    location_id: str = ""
    dialogue: List[DialogueLine] = field(default_factory=list)
    image_references: List[str] = field(default_factory=list)
    previous_shot_id: Optional[str] = None
    next_shot_id: Optional[str] = None
    continuity_seed: str = ""
    language: str = "en"


@dataclass
class MediaAsset:
    asset_id: str
    asset_type: str
    path: str
    duration: float = 0.0
    mime_type: str = ""
    provider: str = "local"
    status: str = "created"
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class TimelineItem:
    item_id: str
    asset_path: str
    start: float
    duration: float
    track: str
    kind: str
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ProductionReport:
    anime_id: str
    episode_id: str
    status: str
    shots_total: int
    shots_ready: int
    shots_failed: int
    audio_ready: int
    subtitles_ready: int
    qc_errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    output_video: str = ""
    generated_at: float = field(default_factory=time.time)


# ---------------------------------------------------------------------------
# Utility layer
# ---------------------------------------------------------------------------

class JsonStore:
    @staticmethod
    def write(path: Path, payload: Any) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

    @staticmethod
    def read(path: Path, default: Any = None) -> Any:
        if not path.exists():
            return default
        try:
            return json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            return default


def stable_id(*parts: Any) -> str:
    raw = "|".join(str(p) for p in parts)
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()[:20]


def safe_name(value: str) -> str:
    chars = []
    for char in value.strip():
        if char.isalnum() or char in "-_":
            chars.append(char)
        elif char in " .":
            chars.append("_")
    return "".join(chars).strip("_") or "item"


def parse_resolution(value: str) -> Tuple[int, int]:
    try:
        width, height = value.lower().split("x", 1)
        width_i, height_i = int(width), int(height)
        if width_i < 320 or height_i < 240:
            raise ValueError
        return width_i, height_i
    except ValueError as exc:
        raise ValueError(f"Invalid resolution: {value!r}") from exc


# ---------------------------------------------------------------------------
# Provider contracts
# ---------------------------------------------------------------------------

class ProviderError(RuntimeError):
    pass


class ImageProvider(Protocol):
    name: str

    def generate(self, prompt: str, references: Sequence[Path], output: Path, metadata: Dict[str, Any]) -> MediaAsset:
        ...


class VideoProvider(Protocol):
    name: str

    def generate(self, prompt: str, first_frame: Optional[Path], references: Sequence[Path], duration: float, output: Path, metadata: Dict[str, Any]) -> MediaAsset:
        ...


class VoiceProvider(Protocol):
    name: str

    def synthesize(self, text: str, language: str, voice_id: str, emotion: str, output: Path, metadata: Dict[str, Any]) -> MediaAsset:
        ...


class MusicProvider(Protocol):
    name: str

    def generate(self, prompt: str, duration: float, output: Path, metadata: Dict[str, Any]) -> MediaAsset:
        ...


class LocalPlaceholderImageProvider:
    name = "local-placeholder-image"

    def generate(self, prompt: str, references: Sequence[Path], output: Path, metadata: Dict[str, Any]) -> MediaAsset:
        output.parent.mkdir(parents=True, exist_ok=True)
        # A valid SVG is deliberately used instead of pretending this is AI image generation.
        escaped = (prompt[:500].replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
                   .replace('"', "&quot;"))
        svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="1920" height="1080" viewBox="0 0 1920 1080">
<rect width="1920" height="1080" fill="#111827"/>
<text x="960" y="500" fill="#f3f4f6" text-anchor="middle" font-family="sans-serif" font-size="44">AJVYRA LOCAL KEYFRAME</text>
<text x="960" y="570" fill="#9ca3af" text-anchor="middle" font-family="sans-serif" font-size="20">{escaped}</text>
</svg>'''
        output = output.with_suffix(".svg")
        output.write_text(svg, encoding="utf-8")
        return MediaAsset(stable_id(output), "image", str(output), provider=self.name, metadata=metadata)


class LocalPlaceholderVideoProvider:
    name = "local-placeholder-video"

    def generate(self, prompt: str, first_frame: Optional[Path], references: Sequence[Path], duration: float, output: Path, metadata: Dict[str, Any]) -> MediaAsset:
        raise ProviderError("Local mode cannot create a real video. Configure a video provider or use render-only mode.")


class LocalSilenceVoiceProvider:
    name = "local-silence-voice"

    def synthesize(self, text: str, language: str, voice_id: str, emotion: str, output: Path, metadata: Dict[str, Any]) -> MediaAsset:
        raise ProviderError("Local mode does not fake speech audio. Configure a real TTS provider or connect AJVYRA's existing TTS engine.")


class LocalMusicPlaceholderProvider:
    name = "local-music-placeholder"

    def generate(self, prompt: str, duration: float, output: Path, metadata: Dict[str, Any]) -> MediaAsset:
        raise ProviderError("Local mode does not fake music audio. Configure a music provider or supply licensed/local music assets.")


class HttpJsonProvider:
    """Generic provider adapter.

    The endpoint contract is intentionally simple so AJVYRA can connect to a
    self-hosted model gateway or a provider adapter without changing production logic.
    Expected JSON response examples:
      {"path": "/absolute/or/relative/output.mp4"}
      {"url": "https://.../file"}
      {"status": "queued", "job_id": "..."}
    A gateway can also return {"bytes_base64": "..."}.
    """

    def __init__(self, name: str, endpoint: str, timeout: int = 180, retries: int = 3):
        self.name = name
        self.endpoint = endpoint
        self.timeout = timeout
        self.retries = retries

    def request_json(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        if not self.endpoint:
            raise ProviderError(f"Provider {self.name} has no endpoint configured")
        data = json.dumps(payload).encode("utf-8")
        req = urlrequest.Request(self.endpoint, data=data, headers={"Content-Type": "application/json"}, method="POST")
        last_error: Optional[Exception] = None
        for attempt in range(1, self.retries + 1):
            try:
                with urlrequest.urlopen(req, timeout=self.timeout) as response:
                    body = response.read().decode("utf-8")
                    parsed = json.loads(body)
                    if not isinstance(parsed, dict):
                        raise ProviderError("Provider response must be a JSON object")
                    return parsed
            except (urlerror.URLError, TimeoutError, json.JSONDecodeError, ProviderError) as exc:
                last_error = exc
                if attempt < self.retries:
                    time.sleep(min(2 ** attempt, 8))
        raise ProviderError(f"Provider {self.name} failed after {self.retries} attempts: {last_error}")

    @staticmethod
    def materialize(response: Dict[str, Any], output: Path) -> None:
        import base64
        import urllib.request as req

        output.parent.mkdir(parents=True, exist_ok=True)
        if response.get("bytes_base64"):
            output.write_bytes(base64.b64decode(response["bytes_base64"]))
            return
        source = response.get("path") or response.get("url")
        if not source:
            raise ProviderError("Provider response contains no path, url, or bytes_base64")
        if str(source).startswith(("http://", "https://")):
            with req.urlopen(str(source), timeout=180) as handle:
                output.write_bytes(handle.read())
        else:
            source_path = Path(str(source))
            if not source_path.exists():
                raise ProviderError(f"Provider output does not exist: {source_path}")
            shutil.copy2(source_path, output)


class HttpImageProvider(HttpJsonProvider):
    def generate(self, prompt: str, references: Sequence[Path], output: Path, metadata: Dict[str, Any]) -> MediaAsset:
        response = self.request_json({"type": "image", "prompt": prompt, "references": [str(p) for p in references], "metadata": metadata})
        self.materialize(response, output)
        return MediaAsset(stable_id(output), "image", str(output), provider=self.name, metadata=metadata)


class HttpVideoProvider(HttpJsonProvider):
    def generate(self, prompt: str, first_frame: Optional[Path], references: Sequence[Path], duration: float, output: Path, metadata: Dict[str, Any]) -> MediaAsset:
        response = self.request_json({"type": "video", "prompt": prompt, "first_frame": str(first_frame) if first_frame else None, "references": [str(p) for p in references], "duration": duration, "metadata": metadata})
        self.materialize(response, output)
        return MediaAsset(stable_id(output), "video", str(output), duration=duration, provider=self.name, metadata=metadata)


class HttpVoiceProvider(HttpJsonProvider):
    def synthesize(self, text: str, language: str, voice_id: str, emotion: str, output: Path, metadata: Dict[str, Any]) -> MediaAsset:
        response = self.request_json({"type": "voice", "text": text, "language": language, "voice_id": voice_id, "emotion": emotion, "metadata": metadata})
        self.materialize(response, output)
        return MediaAsset(stable_id(output), "audio", str(output), provider=self.name, metadata=metadata)


class HttpMusicProvider(HttpJsonProvider):
    def generate(self, prompt: str, duration: float, output: Path, metadata: Dict[str, Any]) -> MediaAsset:
        response = self.request_json({"type": "music", "prompt": prompt, "duration": duration, "metadata": metadata})
        self.materialize(response, output)
        return MediaAsset(stable_id(output), "music", str(output), duration=duration, provider=self.name, metadata=metadata)


# ---------------------------------------------------------------------------
# Story / episode director
# ---------------------------------------------------------------------------

class EpisodeDirector:
    def __init__(self, config: ProductionConfig):
        self.config = config

    def create_episode(self, anime_id: str, episode_number: int, title: str, synopsis: str = "") -> Dict[str, Any]:
        episode_id = f"{safe_name(anime_id)}_s01_e{episode_number:02d}"
        return {
            "anime_id": anime_id,
            "episode_id": episode_id,
            "episode_number": episode_number,
            "title": title,
            "synopsis": synopsis or f"Episode {episode_number} of {anime_id}.",
            "target_duration": self.config.episode_minutes * 60,
            "languages": list(self.config.languages),
            "status": "planned",
        }

    def build_scenes(self, episode: Dict[str, Any], story: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        target = float(episode["target_duration"])
        scene_count = max(12, min(40, round(target / 90)))
        supplied = (story or {}).get("scenes")
        if isinstance(supplied, list) and supplied:
            return supplied
        duration = target / scene_count
        scenes = []
        for i in range(scene_count):
            scenes.append({
                "scene_id": f"scene_{i + 1:03d}",
                "index": i,
                "duration": duration,
                "summary": f"Cinematic scene {i + 1} advancing the episode story.",
                "location_id": "loc_primary",
                "characters": ["protagonist"],
                "emotion": "tension" if i % 3 == 0 else "melancholy",
            })
        return scenes

    def build_shots(self, episode: Dict[str, Any], scenes: Sequence[Dict[str, Any]], characters: Sequence[CharacterSpec], locations: Sequence[LocationSpec]) -> List[ShotSpec]:
        character_map = {c.character_id: c for c in characters}
        location_map = {l.location_id: l for l in locations}
        shots: List[ShotSpec] = []
        previous: Optional[str] = None
        global_index = 0
        for scene in scenes:
            scene_duration = max(1.0, float(scene.get("duration", 60)))
            shot_count = max(3, min(24, round(scene_duration / 7.0)))
            base_duration = scene_duration / shot_count
            scene_chars = [str(x) for x in scene.get("characters", []) if str(x) in character_map]
            if not scene_chars:
                scene_chars = [characters[0].character_id] if characters else []
            location_id = str(scene.get("location_id", locations[0].location_id if locations else ""))
            if location_id not in location_map and locations:
                location_id = locations[0].location_id
            for local_index in range(shot_count):
                shot_id = f"{episode['episode_id']}_{scene['scene_id']}_shot_{local_index + 1:03d}"
                next_id = None
                prompt = self._shot_prompt(scene, local_index, scene_chars, location_map.get(location_id))
                shot = ShotSpec(
                    anime_id=episode["anime_id"],
                    episode_id=episode["episode_id"],
                    scene_id=str(scene["scene_id"]),
                    shot_id=shot_id,
                    index=global_index,
                    duration=base_duration,
                    prompt=prompt,
                    action=str(scene.get("summary", "Characters act within the scene.")),
                    camera={"type": self._camera_type(local_index), "movement": self._camera_movement(local_index)},
                    lighting="soft cinematic anime lighting",
                    emotion=str(scene.get("emotion", "neutral")),
                    character_ids=scene_chars,
                    location_id=location_id,
                    continuity_seed=stable_id(episode["anime_id"], episode["episode_id"], scene["scene_id"], local_index),
                    language="en",
                    previous_shot_id=previous,
                )
                if previous:
                    for existing in shots:
                        if existing.shot_id == previous:
                            existing.next_shot_id = shot_id
                            break
                shots.append(shot)
                previous = shot_id
                global_index += 1
        return shots

    @staticmethod
    def _camera_type(index: int) -> str:
        return ["wide", "medium", "close_up", "over_shoulder", "tracking"][index % 5]

    @staticmethod
    def _camera_movement(index: int) -> str:
        return ["slow_pan", "static", "push_in", "orbit", "tracking"][index % 5]

    @staticmethod
    def _shot_prompt(scene: Dict[str, Any], index: int, characters: Sequence[str], location: Optional[LocationSpec]) -> str:
        location_text = location.description if location else "cinematic environment"
        return (
            f"Original cinematic anime shot. Scene: {scene.get('summary', '')}. "
            f"Shot {index + 1}. Characters: {', '.join(characters) or 'none'}. "
            f"Location: {location_text}. Preserve character identity, wardrobe, proportions and continuity. "
            f"Camera and lighting should feel intentional and story-driven. No logos, no copyrighted characters."
        )


# ---------------------------------------------------------------------------
# Reference and asset manager
# ---------------------------------------------------------------------------

class ReferenceManager:
    def __init__(self, episode_dir: Path):
        self.episode_dir = episode_dir
        self.reference_dir = episode_dir / "references"
        self.reference_dir.mkdir(parents=True, exist_ok=True)

    def character_reference_dir(self, character_id: str) -> Path:
        path = self.reference_dir / "characters" / safe_name(character_id)
        path.mkdir(parents=True, exist_ok=True)
        return path

    def location_reference_dir(self, location_id: str) -> Path:
        path = self.reference_dir / "locations" / safe_name(location_id)
        path.mkdir(parents=True, exist_ok=True)
        return path

    def collect_character_references(self, character: CharacterSpec) -> List[Path]:
        return [Path(p) for p in character.reference_images if Path(p).exists()]

    def collect_location_references(self, location: LocationSpec) -> List[Path]:
        return [Path(p) for p in location.reference_images if Path(p).exists()]


# ---------------------------------------------------------------------------
# Subtitle engine
# ---------------------------------------------------------------------------

class SubtitleBuilder:
    def __init__(self, languages: Sequence[str]):
        self.languages = tuple(languages)

    @staticmethod
    def _timestamp(seconds: float) -> str:
        seconds = max(0.0, float(seconds))
        ms = int(round((seconds - int(seconds)) * 1000))
        total = int(seconds)
        s = total % 60
        m = (total // 60) % 60
        h = total // 3600
        if ms >= 1000:
            ms = 0
            s += 1
        return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"

    def write_srt(self, lines: Sequence[DialogueLine], language: str, output: Path) -> Path:
        output.parent.mkdir(parents=True, exist_ok=True)
        chunks = []
        for index, line in enumerate(lines, 1):
            start = line.start
            end = line.end if line.end > start else start + max(1.0, min(7.0, len(line.text) / 12.0))
            chunks.append(f"{index}\n{self._timestamp(start)} --> {self._timestamp(end)}\n{line.text.strip()}\n")
        output.write_text("\n".join(chunks), encoding="utf-8")
        return output


# ---------------------------------------------------------------------------
# Timeline + renderer
# ---------------------------------------------------------------------------

class TimelineBuilder:
    def build(self, shots: Sequence[ShotSpec], video_assets: Dict[str, MediaAsset], audio_assets: Dict[str, List[MediaAsset]], music_assets: Sequence[MediaAsset] = ()) -> List[TimelineItem]:
        timeline: List[TimelineItem] = []
        cursor = 0.0
        for shot in shots:
            asset = video_assets.get(shot.shot_id)
            if asset and Path(asset.path).exists():
                timeline.append(TimelineItem(shot.shot_id, asset.path, cursor, shot.duration, "video", "shot", {"scene_id": shot.scene_id}))
            for audio in audio_assets.get(shot.shot_id, []):
                timeline.append(TimelineItem(stable_id(shot.shot_id, audio.path), audio.path, cursor, shot.duration, "dialogue", "audio", {"shot_id": shot.shot_id}))
            cursor += shot.duration
        for music in music_assets:
            timeline.append(TimelineItem(stable_id("music", music.path), music.path, 0.0, music.duration, "music", "music"))
        return timeline


class FFmpegRenderer:
    def __init__(self, config: ProductionConfig):
        self.config = config

    @staticmethod
    def executable() -> Optional[str]:
        return shutil.which("ffmpeg")

    def render(self, timeline: Sequence[TimelineItem], output: Path) -> Tuple[bool, str]:
        ffmpeg = self.executable()
        if not ffmpeg:
            return False, "ffmpeg_not_found"
        video_items = [x for x in timeline if x.track == "video" and Path(x.asset_path).exists()]
        if not video_items:
            return False, "no_video_assets"
        output.parent.mkdir(parents=True, exist_ok=True)
        concat_file = output.parent / "video_concat.txt"
        lines = []
        for item in video_items:
            path = Path(item.asset_path).resolve().as_posix().replace("'", "'\\''")
            lines.append(f"file '{path}'")
        concat_file.write_text("\n".join(lines), encoding="utf-8")
        cmd = [ffmpeg, "-y", "-f", "concat", "-safe", "0", "-i", str(concat_file), "-c:v", "libx264", "-pix_fmt", "yuv420p", "-movflags", "+faststart", str(output)]
        try:
            completed = subprocess.run(cmd, capture_output=True, text=True, timeout=3600)
        except subprocess.TimeoutExpired:
            return False, "ffmpeg_timeout"
        if completed.returncode != 0:
            return False, completed.stderr[-4000:]
        return True, "rendered"


# ---------------------------------------------------------------------------
# Quality control
# ---------------------------------------------------------------------------

class ProductionQualityGate:
    REQUIRED_EPISODE_FILES = ("episode.json", "characters.json", "locations.json", "shots.json", "timeline.json")

    def validate_shots(self, shots: Sequence[ShotSpec]) -> List[str]:
        errors: List[str] = []
        if not shots:
            errors.append("no_shots")
            return errors
        previous = None
        for shot in shots:
            if shot.duration <= 0:
                errors.append(f"invalid_duration:{shot.shot_id}")
            if previous and shot.previous_shot_id != previous:
                errors.append(f"broken_previous_link:{shot.shot_id}")
            previous = shot.shot_id
        return errors

    def validate_media(self, shots: Sequence[ShotSpec], assets: Dict[str, MediaAsset]) -> List[str]:
        errors: List[str] = []
        for shot in shots:
            asset = assets.get(shot.shot_id)
            if not asset:
                errors.append(f"missing_video_asset:{shot.shot_id}")
                continue
            if not Path(asset.path).exists():
                errors.append(f"missing_video_file:{shot.shot_id}")
        return errors

    def validate_episode_directory(self, episode_dir: Path) -> List[str]:
        errors = []
        for name in self.REQUIRED_EPISODE_FILES:
            if not (episode_dir / name).exists():
                errors.append(f"missing_file:{name}")
        return errors


# ---------------------------------------------------------------------------
# Main production engine
# ---------------------------------------------------------------------------

class AJVYRAAnimeRealProductionEngine:
    """Runs a complete episode production lifecycle.

    The engine itself owns the orchestration and data contracts. External
    generative models are adapters, not the application architecture.
    """

    def __init__(self, config: Optional[ProductionConfig] = None):
        self.config = config or ProductionConfig.from_env()
        parse_resolution(self.config.resolution)
        self.config.root.mkdir(parents=True, exist_ok=True)
        self.director = EpisodeDirector(self.config)
        self.timeline_builder = TimelineBuilder()
        self.qc = ProductionQualityGate()
        self.subtitle_builder = SubtitleBuilder(self.config.languages)
        self.renderer = FFmpegRenderer(self.config)
        self.image_provider, self.video_provider, self.voice_provider, self.music_provider = self._providers()

    def _providers(self):
        mode = self.config.provider_mode.lower()
        real = mode in {"http", "auto"}
        image = HttpImageProvider("http-image", self.config.image_endpoint, self.config.api_timeout_seconds, self.config.max_retries) if real and self.config.image_endpoint else LocalPlaceholderImageProvider()
        video = HttpVideoProvider("http-video", self.config.video_endpoint, self.config.api_timeout_seconds, self.config.max_retries) if real and self.config.video_endpoint else LocalPlaceholderVideoProvider()
        voice = HttpVoiceProvider("http-voice", self.config.voice_endpoint, self.config.api_timeout_seconds, self.config.max_retries) if real and self.config.voice_endpoint else LocalSilenceVoiceProvider()
        music = HttpMusicProvider("http-music", self.config.music_endpoint, self.config.api_timeout_seconds, self.config.max_retries) if real and self.config.music_endpoint else LocalMusicPlaceholderProvider()
        return image, video, voice, music

    def episode_dir(self, anime_id: str, episode_number: int) -> Path:
        return self.config.root / safe_name(anime_id) / "season_01" / f"episode_{episode_number:02d}"

    def produce_episode(
        self,
        anime_id: str,
        episode_number: int,
        title: str,
        synopsis: str = "",
        story: Optional[Dict[str, Any]] = None,
        characters: Optional[Sequence[CharacterSpec]] = None,
        locations: Optional[Sequence[LocationSpec]] = None,
        dry_run: bool = False,
    ) -> ProductionReport:
        episode = self.director.create_episode(anime_id, episode_number, title, synopsis)
        episode_dir = self.episode_dir(anime_id, episode_number)
        self._prepare_dirs(episode_dir)
        JsonStore.write(episode_dir / "episode.json", episode)

        chars = list(characters or self._default_characters(anime_id))
        locs = list(locations or self._default_locations(anime_id))
        JsonStore.write(episode_dir / "characters.json", [asdict(x) for x in chars])
        JsonStore.write(episode_dir / "locations.json", [asdict(x) for x in locs])

        scenes = self.director.build_scenes(episode, story)
        shots = self.director.build_shots(episode, scenes, chars, locs)
        JsonStore.write(episode_dir / "scenes.json", scenes)
        JsonStore.write(episode_dir / "shots.json", [self._shot_dict(s) for s in shots])

        if dry_run:
            timeline = self.timeline_builder.build(shots, {}, {})
            JsonStore.write(episode_dir / "timeline.json", [asdict(x) for x in timeline])
            errors = self.qc.validate_shots(shots)
            report = ProductionReport(anime_id, episode["episode_id"], "dry_run", len(shots), 0, 0, 0, 0, errors, ["dry_run_no_media_generation"])
            JsonStore.write(episode_dir / "report.json", asdict(report))
            return report

        refs = ReferenceManager(episode_dir)
        video_assets: Dict[str, MediaAsset] = {}
        audio_assets: Dict[str, List[MediaAsset]] = {}
        failed = 0
        warnings: List[str] = []

        for shot in shots:
            try:
                keyframe = self._generate_keyframe(shot, chars, locs, refs, episode_dir)
                video_asset = self._generate_video(shot, keyframe, chars, locs, refs, episode_dir)
                video_assets[shot.shot_id] = video_asset
                audio_assets[shot.shot_id] = self._generate_dialogue_audio(shot, chars, episode_dir)
            except ProviderError as exc:
                failed += 1
                warnings.append(f"{shot.shot_id}:{exc}")
                LOGGER.warning("Shot %s failed: %s", shot.shot_id, exc)

        subtitle_files = self._build_subtitles(shots, episode_dir)
        timeline = self.timeline_builder.build(shots, video_assets, audio_assets)
        JsonStore.write(episode_dir / "timeline.json", [asdict(x) for x in timeline])

        qc_errors = self.qc.validate_shots(shots) + self.qc.validate_media(shots, video_assets)
        output_video = episode_dir / "episode.mp4"
        rendered = False
        render_message = "render_disabled"
        if self.config.render_enabled and video_assets:
            rendered, render_message = self.renderer.render(timeline, output_video)
            if not rendered:
                warnings.append(f"render:{render_message}")
        elif self.config.render_enabled:
            warnings.append("render:no_video_assets")

        status = "complete" if not failed and not qc_errors and rendered else "partial"
        if not rendered and self.config.render_enabled:
            status = "partial"
        report = ProductionReport(
            anime_id=anime_id,
            episode_id=episode["episode_id"],
            status=status,
            shots_total=len(shots),
            shots_ready=len(video_assets),
            shots_failed=failed,
            audio_ready=sum(len(v) for v in audio_assets.values()),
            subtitles_ready=len(subtitle_files),
            qc_errors=qc_errors,
            warnings=warnings,
            output_video=str(output_video) if output_video.exists() else "",
        )
        JsonStore.write(episode_dir / "report.json", asdict(report))
        return report

    def _prepare_dirs(self, episode_dir: Path) -> None:
        for name in ("media/images", "media/video", "audio/dialogue", "audio/music", "subtitles", "references", "logs"):
            (episode_dir / name).mkdir(parents=True, exist_ok=True)

    def _generate_keyframe(self, shot: ShotSpec, characters: Sequence[CharacterSpec], locations: Sequence[LocationSpec], refs: ReferenceManager, episode_dir: Path) -> MediaAsset:
        character_refs: List[Path] = []
        for character in characters:
            if character.character_id in shot.character_ids:
                character_refs.extend(refs.collect_character_references(character))
        for location in locations:
            if location.location_id == shot.location_id:
                character_refs.extend(refs.collect_location_references(location))
        output = episode_dir / "media" / "images" / f"{safe_name(shot.shot_id)}.png"
        metadata = {"shot_id": shot.shot_id, "continuity_seed": shot.continuity_seed, "references": [str(x) for x in character_refs]}
        return self.image_provider.generate(shot.prompt, character_refs, output, metadata)

    def _generate_video(self, shot: ShotSpec, keyframe: MediaAsset, characters: Sequence[CharacterSpec], locations: Sequence[LocationSpec], refs: ReferenceManager, episode_dir: Path) -> MediaAsset:
        reference_paths: List[Path] = [Path(keyframe.path)]
        for character in characters:
            if character.character_id in shot.character_ids:
                reference_paths.extend(refs.collect_character_references(character))
        output = episode_dir / "media" / "video" / f"{safe_name(shot.shot_id)}.mp4"
        prompt = f"{shot.prompt} Action: {shot.action}. Camera: {shot.camera}. Emotion: {shot.emotion}. Maintain visual continuity from the reference frame."
        metadata = {"shot_id": shot.shot_id, "anime_id": shot.anime_id, "episode_id": shot.episode_id, "duration": shot.duration, "fps": self.config.target_fps, "resolution": self.config.resolution}
        return self.video_provider.generate(prompt, Path(keyframe.path), reference_paths[:4], shot.duration, output, metadata)

    def _generate_dialogue_audio(self, shot: ShotSpec, characters: Sequence[CharacterSpec], episode_dir: Path) -> List[MediaAsset]:
        character_map = {c.character_id: c for c in characters}
        assets: List[MediaAsset] = []
        for index, line in enumerate(shot.dialogue):
            character = character_map.get(line.speaker_id)
            voice_id = character.voice_identity if character else line.speaker_id
            output = episode_dir / "audio" / "dialogue" / f"{safe_name(shot.shot_id)}_{index:02d}_{line.speaker_id}.wav"
            metadata = {"shot_id": shot.shot_id, "speaker_id": line.speaker_id, "language": line.text, "emotion": line.emotion}
            asset = self.voice_provider.synthesize(line.text, shot.language, voice_id, line.emotion, output, metadata)
            assets.append(asset)
        return assets

    def _build_subtitles(self, shots: Sequence[ShotSpec], episode_dir: Path) -> List[Path]:
        # The exact translated text should come from the translation pipeline.
        # This engine writes one subtitle file per configured language when dialogue exists.
        lines = [line for shot in shots for line in shot.dialogue]
        if not lines:
            return []
        outputs = []
        for language in self.config.languages:
            output = episode_dir / "subtitles" / f"episode_{language}.srt"
            outputs.append(self.subtitle_builder.write_srt(lines, language, output))
        return outputs

    @staticmethod
    def _shot_dict(shot: ShotSpec) -> Dict[str, Any]:
        data = asdict(shot)
        data["dialogue"] = [asdict(x) for x in shot.dialogue]
        return data

    @staticmethod
    def _default_characters(anime_id: str) -> List[CharacterSpec]:
        return [
            CharacterSpec(
                character_id="protagonist",
                name=f"{safe_name(anime_id)} Protagonist",
                role="protagonist",
                personality=["reserved", "curious", "determined"],
                appearance={"hair": "original dark anime hairstyle", "eyes": "deep expressive eyes", "build": "slim athletic"},
                wardrobe={"primary": "original modern dark outfit"},
                voice_identity=f"{safe_name(anime_id)}_protagonist_voice",
                reference_seed=stable_id(anime_id, "protagonist"),
            ),
        ]

    @staticmethod
    def _default_locations(anime_id: str) -> List[LocationSpec]:
        return [LocationSpec("loc_primary", f"{safe_name(anime_id)} Main Location", "An original cinematic location designed for the story.")]

    def produce_30_anime_first_episodes(self, catalog: Sequence[Dict[str, Any]], dry_run: bool = False) -> List[ProductionReport]:
        reports = []
        for item in catalog[:30]:
            reports.append(self.produce_episode(
                anime_id=str(item["anime_id"]),
                episode_number=1,
                title=str(item.get("title", "Episode 1")),
                synopsis=str(item.get("synopsis", "")),
                dry_run=dry_run,
            ))
        return reports


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def _load_catalog(path: Optional[str]) -> List[Dict[str, Any]]:
    if not path:
        return []
    data = JsonStore.read(Path(path), [])
    if isinstance(data, dict):
        data = data.get("anime", data.get("items", []))
    return data if isinstance(data, list) else []


def main() -> int:
    parser = argparse.ArgumentParser(description="AJVYRA real anime production engine")
    parser.add_argument("--anime", default="Veylora")
    parser.add_argument("--episode", type=int, default=1)
    parser.add_argument("--title", default="Episode 1")
    parser.add_argument("--synopsis", default="")
    parser.add_argument("--catalog", default="")
    parser.add_argument("--mode", choices=["local", "http", "auto"], default=os.getenv("AJVYRA_PROVIDER_MODE", "local"))
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--no-render", action="store_true")
    parser.add_argument("--log-level", default="INFO")
    args = parser.parse_args()

    logging.basicConfig(level=getattr(logging, args.log_level.upper(), logging.INFO), format="%(asctime)s | %(levelname)s | %(message)s")
    config = ProductionConfig.from_env(provider_mode=args.mode, render_enabled=not args.no_render)
    engine = AJVYRAAnimeRealProductionEngine(config)

    if args.catalog:
        catalog = _load_catalog(args.catalog)
        reports = engine.produce_30_anime_first_episodes(catalog, dry_run=args.dry_run)
        print(json.dumps([asdict(r) for r in reports], ensure_ascii=False, indent=2))
        return 0 if all(r.status in {"complete", "dry_run"} for r in reports) else 2

    report = engine.produce_episode(args.anime, args.episode, args.title, args.synopsis, dry_run=args.dry_run)
    print(json.dumps(asdict(report), ensure_ascii=False, indent=2))
    return 0 if report.status in {"complete", "dry_run"} else 2


if __name__ == "__main__":
    raise SystemExit(main())
