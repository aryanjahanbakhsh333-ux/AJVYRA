from __future__ import annotations

import json
import subprocess
from pathlib import Path


class AJVYRAFinal30GameWebExporter:

    def __init__(
        self,
        projects_root: str = "games/real-projects",
        builds_root: str = "games/final-web-builds",
        godot: str = "godot",
        preset: str = "Web",
    ):
        self.projects_root = Path(projects_root)
        self.builds_root = Path(builds_root)
        self.godot = godot
        self.preset = preset

        self.builds_root.mkdir(
            parents=True,
            exist_ok=True,
        )

    def ensure_preset(
        self,
        project: Path,
    ):

        preset = project / "export_presets.cfg"

        if preset.exists():
            return

        preset.write_text(
            """
[preset.0]

name="Web"
platform="Web"
runnable=true
dedicated_server=false

[preset.0.options]

html/export_icon=true
html/export_debug=false
""".strip(),
            encoding="utf-8",
        )

    def export_project(
        self,
        project: Path,
    ) -> dict:

        metadata_file = (
            project / "game.json"
        )

        if not metadata_file.exists():
            raise RuntimeError(
                f"Missing game metadata: {project}"
            )

        metadata = json.loads(
            metadata_file.read_text(
                encoding="utf-8"
            )
        )

        self.ensure_preset(project)

        game_id = metadata["id"]

        output_dir = (
            self.builds_root /
            game_id
        )

        output_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

        output_zip = (
            output_dir /
            "game.zip"
        )

        command = [
            self.godot,
            "--headless",
            "--path",
            str(project),
            "--export-release",
            self.preset,
            str(output_zip),
        ]

        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
        )

        if result.returncode != 0:
            raise RuntimeError(
                f"Godot export failed for "
                f"{metadata['title']}:\n"
                f"{result.stderr}"
            )

        if not output_zip.exists():
            raise RuntimeError(
                f"No Web build produced for "
                f"{metadata['title']}"
            )

        if output_zip.stat().st_size <= 1024:
            raise RuntimeError(
                f"Web build is invalid: "
                f"{metadata['title']}"
            )

        release = {
            "id": game_id,
            "title": metadata["title"],
            "genre": metadata["genre"],
            "engine": "Godot",
            "platform": "web",
            "real_build": True,
            "ready": True,
            "published": True,
            "build": str(output_zip),
            "bytes": output_zip.stat().st_size,
        }

        release_file = (
            self.builds_root /
            f"{game_id}.final-release.json"
        )

        release_file.write_text(
            json.dumps(
                release,
                indent=2,
                ensure_ascii=False,
            ),
            encoding="utf-8",
        )

        return release

    def export_all(self):

        projects = [
            item
            for item in self.projects_root.iterdir()
            if item.is_dir()
            and (
                item / "project.godot"
            ).exists()
        ]

        if len(projects) != 30:
            raise RuntimeError(
                f"Expected 30 game projects, "
                f"found {len(projects)}"
            )

        results = []

        for project in sorted(projects):
            print(
                f"[GAME BUILD] "
                f"{project.name}"
            )

            results.append(
                self.export_project(project)
            )

        if len(results) != 30:
            raise RuntimeError(
                "30 Web game builds were not produced."
            )

        return results


if __name__ == "__main__":
    exporter = AJVYRAFinal30GameWebExporter()

    result = exporter.export_all()

    print(
        f"\nAJVYRA GAME BUILDS: "
        f"{len(result)}/30"
    )
