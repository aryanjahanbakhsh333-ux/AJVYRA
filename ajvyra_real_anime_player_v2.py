"""
AJVYRA — REAL ANIME PLAYER DATA v2

این فایل اطلاعات لازم برای ساخت Player واقعی سایت را می‌دهد.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class AnimePlayerSource:
    anime_id: str
    title: str
    video_url: str
    poster_url: str
    duration_seconds: float
    autoplay: bool = False
    controls: bool = True


class AnimePlayerFactory:

    def create(
        self,
        anime: dict,
        public_prefix: str = "/anime-assets",
    ) -> AnimePlayerSource:

        video_path = anime["video"]
        poster_path = anime["poster"]

        video_url = (
            public_prefix.rstrip("/")
            + "/"
            + video_path.replace("\\", "/")
        )

        poster_url = (
            public_prefix.rstrip("/")
            + "/"
            + poster_path.replace("\\", "/")
        )

        return AnimePlayerSource(
            anime_id=anime["id"],
            title=anime["title"],
            video_url=video_url,
            poster_url=poster_url,
            duration_seconds=float(
                anime["duration_seconds"]
            ),
        )

    def html(
        self,
        source: AnimePlayerSource,
    ) -> str:

        return f"""
<div class="ajvyra-anime-player"
     data-anime-id="{source.anime_id}">

  <video
      controls
      preload="metadata"
      playsinline
      poster="{source.poster_url}"
      style="width:100%;height:auto;background:#000;">

    <source
        src="{source.video_url}"
        type="video/mp4">

    Your browser does not support HTML5 video.
  </video>

  <div class="ajvyra-player-title">
    {source.title}
  </div>

</div>
""".strip()
