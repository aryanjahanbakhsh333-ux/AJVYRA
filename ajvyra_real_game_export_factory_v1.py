from __future__ import annotations

import json
import subprocess
from pathlib import Path
from typing import Any


class AJVYRARealGameExporter:

    def __init__(
        self,
        godot_binary: str = "godot",
        build_root: str = "games/builds",
    ):
        self.godot = godot_binary
        self.build_root = Path(build_root)
        self.build_root.mkdir(
            parents=True,
            exist_ok=True,
        )

    def check_project(
        self,
        project: Path,
    ) -> None:

        required = [
            project / "project.godot",
            project / "scenes/main.tscn",
            project / "scripts/main.gd",
        ]

        missing = [
            str(path)
            for path in required
            if not path.exists()
        ]

        if missing:
            raise RuntimeError(
                "Game project is incomplete:\n"
                + "\n".join(missing)
            )

    def create_export_preset(
        self,
        project: Path,
        preset_name: str = "Linux",
    ) -> None:

        preset = f"""
[preset.0]

name="{preset_name}"
platform="Linux/X11"
runnable=true
dedicated_server=false

[preset.0.options]

binary_format/embed_pck=true
"""

        (project / "export_presets.cfg").write_text(
            preset.strip(),
            encoding="utf-8",
        )

    def export(
        self,
        project: str,
        game_id: str,
        preset: str = "Linux",
    ) -> Path:

        project_path = Path(project)

        self.check_project(project_path)
        self.create_export_preset(
            project_path,
            preset,
        )

        output = (
            self.build_root /
            f"{game_id}.x86_64"
        )

        command = [
            self.godot,
            "--headless",
            "--path",
            str(project_path),
            "--export-release",
            preset,
            str(output),
        ]

        print(
            "[AJVYRA] Exporting real game:"
        )
        print(" ".join(command))

        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
        )

        if result.returncode != 0:
            raise RuntimeError(
                "Godot export failed:\n"
                + result.stderr
            )

        if not output.exists():
            raise RuntimeError(
                f"Godot reported success but build "
                f"does not exist: {output}"
            )

        if output.stat().st_size <= 0:
            raise RuntimeError(
                f"Game build is empty: {output}"
            )

        return output

    def write_release_record(
        self,
        game_id: str,
        title: str,
        build: Path,
    ) -> Path:

        record = {
            "id": game_id,
            "title": title,
            "build": str(build),
            "bytes": build.stat().st_size,
            "real_build": True,
            "ready": True,
            "published": False,
        }

        path = (
            self.build_root /
            f"{game_id}.release.json"
        )

        path.write_text(
            json.dumps(
                record,
                indent=2,
                ensure_ascii=False,
            ),
            encoding="utf-8",
        )

        return path


if __name__ == "__main__":
    print(
        "AJVYRA Real Game Export Factory loaded."
    )
