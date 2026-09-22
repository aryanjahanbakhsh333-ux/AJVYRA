from pathlib import Path
import json


class AIAssetFactory:

    def __init__(
        self,
        root: str = "ajvyra_projects",
    ):
        self.root = Path(root)
        self.root.mkdir(
            parents=True,
            exist_ok=True,
        )

    def project_root(
        self,
        project_id: str,
    ) -> Path:

        path = self.root / project_id
        path.mkdir(
            parents=True,
            exist_ok=True,
        )

        return path

    def create_folder(
        self,
        project_id: str,
        name: str,
    ) -> Path:

        path = (
            self.project_root(project_id)
            / name
        )

        path.mkdir(
            parents=True,
            exist_ok=True,
        )

        return path

    def write_json(
        self,
        project_id: str,
        relative_path: str,
        data: dict,
    ) -> Path:

        path = (
            self.project_root(project_id)
            / relative_path
        )

        path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        path.write_text(
            json.dumps(
                data,
                ensure_ascii=False,
                indent=2,
            ),
            encoding="utf-8",
        )

        return path

    def write_text(
        self,
        project_id: str,
        relative_path: str,
        content: str,
    ) -> Path:

        path = (
            self.project_root(project_id)
            / relative_path
        )

        path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        path.write_text(
            content,
            encoding="utf-8",
        )

        return path
