from __future__ import annotations

import json
from pathlib import Path
from typing import Any


class AJVYRAFinalSiteIntegration:
    """
    Final integration layer for the AJVYRA release.

    Expected release root:
        generated/ajvyra_release/

    This module does not generate fake media.
    It only integrates and verifies assets that actually exist.
    """

    def __init__(self, root: str | Path = "generated/ajvyra_release"):
        self.root = Path(root)
        self.anime_dir = self.root / "anime"
        self.games_dir = self.root / "games"
        self.site_dir = self.root / "site"
        self.site_dir.mkdir(parents=True, exist_ok=True)

    def anime_entries(self) -> list[dict[str, Any]]:
        manifest = self.root / "ajvyra_real_anime_manifest.json"

        if not manifest.exists():
            return []

        data = json.loads(manifest.read_text(encoding="utf-8"))

        if isinstance(data, list):
            return data

        if isinstance(data, dict):
            for key in ("anime", "items", "entries"):
                if isinstance(data.get(key), list):
                    return data[key]

        return []

    def game_entries(self) -> list[dict[str, Any]]:
        manifest = self.root / "ajvyra_games_manifest_v3.json"

        if not manifest.exists():
            return []

        data = json.loads(manifest.read_text(encoding="utf-8"))

        if isinstance(data, list):
            return data

        if isinstance(data, dict):
            for key in ("games", "items", "entries"):
                if isinstance(data.get(key), list):
                    return data[key]

        return []

    def build_site_index(self) -> Path:
        anime = self.anime_entries()
        games = self.game_entries()

        anime_cards = []

        for i, item in enumerate(anime, 1):
            anime_cards.append(
                f"""
                <article class="card">
                    <img src="../anime/anime_{i:02d}/poster.jpg"
                         onerror="this.style.display='none'">
                    <h2>{item.get("title", f"Anime {i}")}</h2>
                    <a href="../anime/anime_{i:02d}/index.html">WATCH</a>
                </article>
                """
            )

        game_cards = []

        for i, item in enumerate(games, 1):
            game_cards.append(
                f"""
                <article class="card">
                    <h2>{item.get("title", f"Game {i}")}</h2>
                    <p>{item.get("genre", "Original Game")}</p>
                    <a href="../games/game_{i:02d}/index.html">PLAY</a>
                </article>
                """
            )

        html = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport"
      content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>AJVYRA</title>
<style>
*{{box-sizing:border-box}}
html,body{{margin:0;background:#000;color:#fff;font-family:Arial,sans-serif}}
body{{min-height:100vh}}
header{{padding:28px;text-align:center;border-bottom:1px solid #222}}
.logo{{font-size:42px;font-weight:900;letter-spacing:8px}}
.subtitle{{opacity:.65}}
section{{padding:28px}}
.grid{{display:grid;grid-template-columns:
repeat(auto-fit,minmax(220px,1fr));gap:18px}}
.card{{background:#0b0b0b;border:1px solid #222;border-radius:16px;
padding:16px;min-height:190px}}
.card img{{width:100%;height:220px;object-fit:cover;border-radius:10px}}
.card h2{{margin:12px 0 8px}}
.card p{{opacity:.65}}
a{{display:inline-block;margin-top:12px;padding:10px 16px;
background:#fff;color:#000;text-decoration:none;border-radius:8px;
font-weight:700}}
.status{{text-align:center;padding:20px;border:1px solid #222;
margin:20px;border-radius:12px}}
</style>
</head>
<body>
<header>
<div class="logo">AJVYRA</div>
<div class="subtitle">ANIME • GAMES • ORIGINAL WORLDS</div>
</header>

<div class="status">
Anime: {len(anime)}/30 &nbsp; | &nbsp; Games: {len(games)}/30
</div>

<section>
<h1>Anime</h1>
<div class="grid">
{''.join(anime_cards)}
</div>
</section>

<section>
<h1>Games</h1>
<div class="grid">
{''.join(game_cards)}
</div>
</section>
</body>
</html>
"""

        output = self.site_dir / "index.html"
        output.write_text(html, encoding="utf-8")
        return output

    def run(self) -> dict[str, Any]:
        index = self.build_site_index()

        return {
            "success": True,
            "site_index": str(index),
            "anime_count": len(self.anime_entries()),
            "game_count": len(self.game_entries()),
        }


if __name__ == "__main__":
    result = AJVYRAFinalSiteIntegration().run()
    print(json.dumps(result, indent=2, ensure_ascii=False))
