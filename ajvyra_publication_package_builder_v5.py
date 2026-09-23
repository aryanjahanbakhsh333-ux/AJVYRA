from __future__ import annotations

import json
import shutil
from pathlib import Path


class PublicationPackageBuilder:
    def __init__(
        self,
        root="generated/ajvyra_release",
        output="generated/AJVYRA_PUBLICATION",
    ):
        self.root = Path(root)
        self.output = Path(output)

    def clean(self):
        if self.output.exists():
            shutil.rmtree(self.output)

        self.output.mkdir(
            parents=True,
            exist_ok=True,
        )

    def copy_required(self):
        site = self.root / "site"

        if not site.exists():
            raise RuntimeError(
                "Site has not been generated."
            )

        destination = self.output / "site"

        shutil.copytree(site, destination)

    def copy_media(self):
        anime = self.root / "anime"
        games = self.root / "games"

        if not anime.exists() or not games.exists():
            raise RuntimeError(
                "Anime or game release directories are missing."
            )

        shutil.copytree(
            anime,
            self.output / "site" / "anime",
        )

        shutil.copytree(
            games,
            self.output / "site" / "games",
        )

    def run(self):
        self.clean()
        self.copy_required()
        self.copy_media()

        result = {
            "project": "AJVYRA",
            "package": str(self.output),
            "ready_for_static_host": True,
        }

        (self.output / "PUBLICATION_PACKAGE.json").write_text(
            json.dumps(
                result,
                indent=2,
                ensure_ascii=False,
            ),
            encoding="utf-8",
        )

        return result


if __name__ == "__main__":
    print(json.dumps(
        PublicationPackageBuilder().run(),
        indent=2,
        ensure_ascii=False,
    ))
