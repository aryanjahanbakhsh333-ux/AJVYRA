from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional
import html
import re


# ------------------------------------------------------------
# AJVYRA Anime Subtitle Engine
# ------------------------------------------------------------
# مستقل از Player / API
# وظایف:
# - خواندن SRT
# - تبدیل SRT به WebVTT
# - اعتبارسنجی زمان‌بندی
# - انتخاب زبان زیرنویس
# - حالت OFF
# - تولید Track مناسب برای HTML5
# ------------------------------------------------------------


SUPPORTED_LANGUAGES = {
    "en": "English",
    "fa": "فارسی",
    "ja": "日本語",
}

SUBTITLE_OFF = "off"


@dataclass
class SubtitleCue:
    index: int
    start: float
    end: float
    text: str

    def to_vtt(self) -> str:
        return (
            f"{format_vtt_time(self.start)} --> "
            f"{format_vtt_time(self.end)}\n"
            f"{self.text}\n"
        )


@dataclass
class SubtitleTrack:
    language: str
    label: str
    path: Optional[Path]
    enabled: bool = False

    @property
    def is_off(self) -> bool:
        return self.language == SUBTITLE_OFF


def parse_timestamp(value: str) -> float:
    """
    SRT timestamp:
    HH:MM:SS,mmm
    HH:MM:SS.mmm
    """

    value = value.strip().replace(",", ".")

    match = re.fullmatch(
        r"(\d{2}):(\d{2}):(\d{2})\.(\d{3})",
        value,
    )

    if not match:
        raise ValueError(f"Invalid timestamp: {value}")

    hours, minutes, seconds, milliseconds = map(int, match.groups())

    return (
        hours * 3600
        + minutes * 60
        + seconds
        + milliseconds / 1000
    )


def format_vtt_time(seconds: float) -> str:
    """
    Convert seconds to WebVTT timestamp:
    HH:MM:SS.mmm
    """

    if seconds < 0:
        seconds = 0

    total_ms = round(seconds * 1000)

    hours = total_ms // 3_600_000
    total_ms %= 3_600_000

    minutes = total_ms // 60_000
    total_ms %= 60_000

    secs = total_ms // 1000
    milliseconds = total_ms % 1000

    return f"{hours:02d}:{minutes:02d}:{secs:02d}.{milliseconds:03d}"


def clean_subtitle_text(text: str) -> str:
    """
    پاک‌سازی ساده متن SRT بدون تغییر محتوای اصلی.
    """

    text = text.replace("\ufeff", "")
    text = text.replace("\r\n", "\n")
    text = text.replace("\r", "\n")

    # حذف تگ‌های رایج HTML/SRT
    text = re.sub(r"<\/?i>", "", text, flags=re.IGNORECASE)
    text = re.sub(r"<\/?b>", "", text, flags=re.IGNORECASE)
    text = re.sub(r"<\/?u>", "", text, flags=re.IGNORECASE)

    return html.escape(text, quote=False)


def parse_srt(content: str) -> List[SubtitleCue]:
    """
    Parse complete SRT content into subtitle cues.
    """

    content = content.replace("\ufeff", "")
    content = content.replace("\r\n", "\n")
    content = content.replace("\r", "\n")

    blocks = re.split(r"\n\s*\n", content.strip())

    cues: List[SubtitleCue] = []

    for block in blocks:
        lines = block.split("\n")

        if len(lines) < 3:
            continue

        index_line = lines[0].strip()
        timing_line = lines[1].strip()

        try:
            index = int(index_line)
        except ValueError:
            continue

        timing_match = re.match(
            r"(.+?)\s*-->\s*(.+?)(?:\s|$)",
            timing_line,
        )

        if not timing_match:
            continue

        start_text = timing_match.group(1)
        end_text = timing_match.group(2)

        try:
            start = parse_timestamp(start_text)
            end = parse_timestamp(end_text)
        except ValueError:
            continue

        subtitle_text = "\n".join(lines[2:]).strip()

        if not subtitle_text:
            continue

        subtitle_text = clean_subtitle_text(subtitle_text)

        cues.append(
            SubtitleCue(
                index=index,
                start=start,
                end=end,
                text=subtitle_text,
            )
        )

    return cues


def validate_cues(cues: List[SubtitleCue]) -> List[str]:
    """
    بررسی مشکلات زمان‌بندی.
    """

    errors: List[str] = []

    previous_end = 0.0

    for position, cue in enumerate(cues, start=1):

        if cue.start < 0:
            errors.append(
                f"Cue {cue.index}: start time is negative."
            )

        if cue.end <= cue.start:
            errors.append(
                f"Cue {cue.index}: end must be after start."
            )

        if position > 1 and cue.start < previous_end:
            errors.append(
                f"Cue {cue.index}: overlaps previous cue."
            )

        previous_end = max(previous_end, cue.end)

    return errors


def srt_to_vtt(content: str) -> str:
    """
    Convert SRT text directly into WebVTT text.
    """

    cues = parse_srt(content)

    lines = ["WEBVTT", ""]

    for cue in cues:
        lines.append(cue.to_vtt())
        lines.append("")

    return "\n".join(lines)


def convert_file(
    srt_path: str | Path,
    vtt_path: str | Path | None = None,
) -> Path:
    """
    Convert an SRT file to VTT.

    If vtt_path is not supplied:
    example.srt -> example.vtt
    """

    srt_path = Path(srt_path)

    if not srt_path.exists():
        raise FileNotFoundError(
            f"Subtitle file not found: {srt_path}"
        )

    if vtt_path is None:
        vtt_path = srt_path.with_suffix(".vtt")
    else:
        vtt_path = Path(vtt_path)

    content = srt_path.read_text(
        encoding="utf-8-sig"
    )

    vtt_content = srt_to_vtt(content)

    vtt_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    vtt_path.write_text(
        vtt_content,
        encoding="utf-8",
    )

    return vtt_path


def get_language_name(language: str) -> str:
    return SUPPORTED_LANGUAGES.get(
        language,
        language,
    )


def build_subtitle_tracks(
    anime_number: int,
    root: str | Path = "anime_assets",
) -> List[SubtitleTrack]:
    """
    ساخت لیست Trackهای زیرنویس برای یک انیمه.

    ترتیب:
    OFF
    English
    فارسی
    日本語
    """

    root = Path(root)

    anime_folder = root / f"anime_{anime_number:02d}"
    subtitle_folder = anime_folder / "subtitles"

    tracks = [
        SubtitleTrack(
            language=SUBTITLE_OFF,
            label="Off",
            path=None,
            enabled=True,
        )
    ]

    for language, label in SUPPORTED_LANGUAGES.items():

        subtitle_path = subtitle_folder / f"{language}.srt"

        tracks.append(
            SubtitleTrack(
                language=language,
                label=label,
                path=subtitle_path,
                enabled=False,
            )
        )

    return tracks


def get_available_tracks(
    anime_number: int,
    root: str | Path = "anime_assets",
) -> List[SubtitleTrack]:

    tracks = build_subtitle_tracks(
        anime_number,
        root,
    )

    return [
        track
        for track in tracks
        if track.is_off
        or (
            track.path is not None
            and track.path.exists()
        )
    ]


def select_subtitle(
    anime_number: int,
    language: str,
    root: str | Path = "anime_assets",
) -> Dict[str, object]:

    language = language.lower().strip()

    if language == SUBTITLE_OFF:
        return {
            "anime": anime_number,
            "language": SUBTITLE_OFF,
            "label": "Off",
            "enabled": False,
            "path": None,
        }

    if language not in SUPPORTED_LANGUAGES:
        raise ValueError(
            f"Unsupported subtitle language: {language}"
        )

    tracks = get_available_tracks(
        anime_number,
        root,
    )

    selected = next(
        (
            track
            for track in tracks
            if track.language == language
        ),
        None,
    )

    if selected is None:
        raise FileNotFoundError(
            f"Subtitle not found: {language}"
        )

    return {
        "anime": anime_number,
        "language": selected.language,
        "label": selected.label,
        "enabled": True,
        "path": str(selected.path),
    }


def subtitle_status(
    anime_number: int,
    root: str | Path = "anime_assets",
) -> Dict[str, object]:

    tracks = get_available_tracks(
        anime_number,
        root,
    )

    available = [
        track.language
        for track in tracks
        if not track.is_off
    ]

    return {
        "anime": anime_number,
        "off_available": True,
        "available_languages": available,
        "language_names": {
            language: get_language_name(language)
            for language in available
        },
    }


def create_html_tracks(
    anime_number: int,
    root: str | Path = "anime_assets",
    asset_prefix: str = "/subtitle",
) -> str:
    """
    تولید <track> های HTML5.

    گزینه OFF عمداً به صورت track ساخته نمی‌شود؛
    خاموش کردن زیرنویس با track.mode = "disabled"
    در Player انجام می‌شود.
    """

    tracks = get_available_tracks(
        anime_number,
        root,
    )

    html_tracks: List[str] = []

    for track in tracks:

        if track.is_off:
            continue

        relative_path = (
            f"{asset_prefix}/"
            f"{anime_number:02d}/"
            f"{track.language}.vtt"
        )

        escaped_path = html.escape(
            relative_path,
            quote=True,
        )

        escaped_label = html.escape(
            track.label,
            quote=True,
        )

        escaped_language = html.escape(
            track.language,
            quote=True,
        )

        html_tracks.append(
            (
                f'<track kind="subtitles" '
                f'src="{escaped_path}" '
                f'srclang="{escaped_language}" '
                f'label="{escaped_label}">'
            )
        )

    return "\n".join(html_tracks)


def prepare_episode_subtitles(
    anime_number: int,
    root: str | Path = "anime_assets",
) -> Dict[str, object]:
    """
    تبدیل همه SRTهای موجود یک قسمت به VTT.
    """

    root = Path(root)

    subtitle_folder = (
        root / f"anime_{anime_number:02d}" / "subtitles"
    )

    result: Dict[str, object] = {
        "anime": anime_number,
        "converted": [],
        "missing": [],
        "errors": [],
    }

    for language in SUPPORTED_LANGUAGES:

        srt_path = subtitle_folder / f"{language}.srt"
        vtt_path = subtitle_folder / f"{language}.vtt"

        if not srt_path.exists():
            result["missing"].append(language)
            continue

        try:
            cues = parse_srt(
                srt_path.read_text(
                    encoding="utf-8-sig"
                )
            )

            validation_errors = validate_cues(cues)

            if validation_errors:
                result["errors"].append(
                    {
                        "language": language,
                        "errors": validation_errors,
                    }
                )
                continue

            convert_file(
                srt_path,
                vtt_path,
            )

            result["converted"].append(
                language
            )

        except Exception as exc:
            result["errors"].append(
                {
                    "language": language,
                    "error": str(exc),
                }
            )

    return result


def subtitle_api_payload(
    anime_number: int,
    root: str | Path = "anime_assets",
) -> Dict[str, object]:

    status = subtitle_status(
        anime_number,
        root,
    )

    tracks = []

    for language in status["available_languages"]:
        tracks.append(
            {
                "language": language,
                "label": get_language_name(language),
                "enabled": False,
            }
        )

    return {
        "anime": anime_number,
        "off": {
            "language": SUBTITLE_OFF,
            "label": "Off",
            "enabled": True,
        },
        "tracks": tracks,
    }


def main() -> None:
    print("=" * 60)
    print("AJVYRA Anime Subtitle Engine")
    print("=" * 60)

    demo_anime = 1

    print(f"\nAnime: {demo_anime}")
    print("Supported languages:")

    for code, name in SUPPORTED_LANGUAGES.items():
        print(f"  {code} -> {name}")

    print("\nSubtitle mode:")
    print("  off -> زیرنویس خاموش")

    status = subtitle_status(demo_anime)

    print("\nStatus:")
    print(status)

    print("\nHTML tracks:")
    print(
        create_html_tracks(
            demo_anime
        )
        or "No VTT tracks found."
    )


if __name__ == "__main__":
    main()
