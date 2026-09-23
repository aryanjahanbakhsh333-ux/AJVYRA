"""
AJVYRA browser game hub.

Generates one real HTML game-library page that links to all 30 playable games.
"""

from __future__ import annotations

import html
from pathlib import Path

from ajvyra_browser_game_runtime_v3 import GAMES


def build_hub(root: Path) -> Path:
    cards = []

    for game in GAMES:
        cards.append(
            f"""
<a class="card"
   href="/games/game_{game.number:02d}/index.html">
    <span class="number">{game.number:02d}</span>
    <h2>{html.escape(game.title)}</h2>
    <p>{html.escape(game.genre)}</p>
    <small>{html.escape(game.description)}</small>
    <strong>PLAY</strong>
</a>
"""
        )

    document = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport"
      content="width=device-width,initial-scale=1">
<title>AJVYRA — Games</title>
<style>
body {{
    margin:0;
    background:#050505;
    color:#fff;
    font-family:system-ui,sans-serif;
}}
main {{
    max-width:1200px;
    margin:auto;
    padding:30px 18px 60px;
}}
h1 {{
    font-size:44px;
    margin-bottom:4px;
}}
.subtitle {{
    color:#888;
    margin-bottom:28px;
}}
.grid {{
    display:grid;
    grid-template-columns:
        repeat(auto-fit,minmax(250px,1fr));
    gap:16px;
}}
.card {{
    position:relative;
    display:block;
    min-height:190px;
    padding:22px;
    box-sizing:border-box;
    border:1px solid #262626;
    border-radius:15px;
    background:#0c0c0c;
    color:#fff;
    text-decoration:none;
    transition:.15s;
}}
.card:hover {{
    transform:translateY(-3px);
    border-color:#555;
}}
.number {{
    color:#777;
}}
.card h2 {{
    margin:18px 0 6px;
}}
.card p {{
    color:#aaa;
}}
.card small {{
    color:#777;
}}
.card strong {{
    position:absolute;
    right:18px;
    bottom:18px;
}}
</style>
</head>
<body>
<main>
<h1>AJVYRA</h1>
<div class="subtitle">
30 original browser-playable games
</div>
<div class="grid">
{''.join(cards)}
</div>
</main>
</body>
</html>
"""

    output = root / "games" / "index.html"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(document, encoding="utf-8")

    return output
