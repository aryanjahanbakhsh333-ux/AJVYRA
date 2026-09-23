from __future__ import annotations

import json
import subprocess
from pathlib import Path


class AJVYRA30RealGameExporter:

    def __init__(
        self,
        projects_root: str = "games/real-projects",
        builds_root: str = "games/real-builds",
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

    def read_metadata(
        self,
        project: Path,
    ) -> dict:

        metadata = project / "game.json"

        if not metadata.exists():
            raise RuntimeError(
                f"Missing metadata: {metadata}"
            )

        return json.loads(
            metadata.read_text(
                encoding="utf-8"
            )
        )

    def ensure_preset(
        self,
        project: Path,
    ):

        preset_file = (
            project /
            "export_presets.cfg"
        )

        if preset_file.exists():
            return

        preset_file.write_text(
            '''
[preset.0]

name="Web"
platform="Web"
runnable=true
dedicated_server=false

[preset.0.options]

html/export_icon=true
html/export_debug=false
'''.strip(),
            encoding="utf-8",
        )

    def export_one(
        self,
        project: Path,
    ) -> Path:

        metadata = self.read_metadata(
            project
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

        output = (
            output_dir /
            "index.html"
        )

        command = [
            self.godot,
            "--headless",
            "--path",
            str(project),
            "--export-release",
            self.preset,
            str(output),
        ]

        print(
            "[GAME EXPORT]",
            metadata["title"],
        )

        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
        )

        if result.returncode != 0:
            raise RuntimeError(
                "Godot export failed for "
                f"{metadata['title']}:\n"
                f"{result.stderr}"
            )

        if not output.exists():
            raise RuntimeError(
                "Godot reported success but "
                f"no build was produced: {output}"
            )

        record = {
            "id": game_id,
            "title": metadata["title"],
            "genre": metadata["genre"],
            "engine": "Godot",
            "real_build": True,
            "build": str(output_dir),
            "entry": str(output),
            "ready": True,
            "published": True,
        }

        release_file = (
            self.builds_root /
            f"{game_id}.release.json"
        )

        release_file.write_text(
            json.dumps(
                record,
                indent=2,
                ensure_ascii=False,
            ),
            encoding="utf-8",
        )

        return release_file

    def export_all(self):

        projects = sorted(
            self.projects_root.iterdir()
        )

        projects = [
            p for p in projects
            if p.is_dir()
            and (p / "project.godot").exists()
        ]

        if len(projects) != 30:
            raise RuntimeError(
                f"Expected 30 game projects, "
                f"found {len(projects)}."
            )

        releases = []

        for project in projects:
            releases.append(
                self.export_one(project)
            )

        if len(releases) != 30:
            raise RuntimeError(
                "30 game exports were not completed."
            )

        return releases


if __name__ == "__main__":
    exporter = AJVYRA30RealGameExporter()

    result = exporter.export_all()

    print(
        f"REAL GAME BUILDS: "
        f"{len(result)}/30"
    )
