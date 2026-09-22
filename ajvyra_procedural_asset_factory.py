from pathlib import Path
import html
import json


class AJVYRAProceduralAssetFactory:

    def __init__(self):
        self.colors = {
            "rpg": ("#d7c4ff", "#7d52d9"),
            "platformer": ("#d5e8ff", "#3979c9"),
            "horror": ("#c9b8d6", "#4a245d"),
            "racing": ("#ffd5c7", "#d95735"),
            "puzzle": ("#d1f2dc", "#3d9a68"),
            "survival": ("#f0dfbd", "#a06f2d"),
            "adventure": ("#cce8df", "#347e70"),
            "shooter": ("#f0c8cf", "#a9364b"),
            "stealth": ("#ccd2df", "#3b465c"),
            "runner": ("#f4dfbd", "#bc7d2f"),
        }

    def _svg(
        self,
        genre,
        asset_type,
        label,
    ):
        primary, secondary = self.colors.get(
            genre,
            ("#eeeeee", "#555555"),
        )

        label = html.escape(label)

        if asset_type == "character":
            body = f"""
            <circle cx="128" cy="72" r="42"
                    fill="{primary}"/>
            <rect x="76" y="110"
                  width="104"
                  height="100"
                  rx="28"
                  fill="{secondary}"/>
            <circle cx="112" cy="70" r="6" fill="#111"/>
            <circle cx="144" cy="70" r="6" fill="#111"/>
            """

        elif asset_type == "enemy":
            body = f"""
            <path d="M128 28 L220 210 L36 210 Z"
                  fill="{secondary}"/>
            <circle cx="98" cy="125" r="10" fill="#fff"/>
            <circle cx="158" cy="125" r="10" fill="#fff"/>
            <circle cx="98" cy="125" r="4" fill="#111"/>
            <circle cx="158" cy="125" r="4" fill="#111"/>
            """

        elif asset_type == "environment":
            body = f"""
            <rect width="256" height="256"
                  fill="{primary}"/>
            <rect y="170" width="256" height="86"
                  fill="{secondary}"/>
            <circle cx="205" cy="52" r="30"
                    fill="#fff" opacity=".45"/>
            <path d="M0 170 L60 100 L110 170
                     L160 90 L256 170 Z"
                  fill="#1b2433"
                  opacity=".65"/>
            """

        elif asset_type == "object":
            body = f"""
            <rect x="48" y="48"
                  width="160"
                  height="160"
                  rx="22"
                  fill="{secondary}"/>
            <circle cx="128" cy="128"
                    r="52"
                    fill="{primary}"/>
            """

        elif asset_type == "effect":
            body = f"""
            <circle cx="128" cy="128"
                    r="90"
                    fill="{secondary}"
                    opacity=".18"/>
            <circle cx="128" cy="128"
                    r="55"
                    fill="{primary}"
                    opacity=".45"/>
            <circle cx="128" cy="128"
                    r="18"
                    fill="#fff"/>
            """

        else:
            body = f"""
            <rect x="16" y="16"
                  width="224"
                  height="224"
                  rx="24"
                  fill="#121722"
                  stroke="{secondary}"
                  stroke-width="5"/>
            """

        return f"""<svg xmlns="http://www.w3.org/2000/svg"
width="256" height="256" viewBox="0 0 256 256">
{body}
<text x="128" y="244"
text-anchor="middle"
font-family="Arial"
font-size="11"
fill="#fff">{label}</text>
</svg>
"""

    def generate_game_assets(
        self,
        game_id,
        genre,
        registry,
        output_root="generated/ajvyra_assets",
    ):
        game_dir = (
            Path(output_root) /
            f"game_{game_id:02d}" /
            "assets"
        )

        game_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

        generated = []

        for asset in registry["assets"]:
            filename = (
                f'{asset["asset_id"]}.svg'
            )

            path = game_dir / filename

            svg = self._svg(
                genre=genre,
                asset_type=asset["asset_type"],
                label=asset["name"],
            )

            path.write_text(
                svg,
                encoding="utf-8",
            )

            generated.append(
                {
                    "asset_id": asset["asset_id"],
                    "path": f"assets/{filename}",
                    "type": asset["asset_type"],
                }
            )

        manifest = {
            "game_id": game_id,
            "generated_assets": generated,
            "format": "svg",
            "ready_for_browser": True,
        }

        (game_dir.parent / "asset_manifest.json").write_text(
            json.dumps(
                manifest,
                ensure_ascii=False,
                indent=2,
            ),
            encoding="utf-8",
        )

        return manifest
