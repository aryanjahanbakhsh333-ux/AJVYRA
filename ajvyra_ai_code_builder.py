from pathlib import Path


class AICodeBuilder:

    def __init__(
        self,
        factory,
    ):
        self.factory = factory

    def create_python_module(
        self,
        project_id: str,
        module_name: str,
        source: str,
    ) -> Path:

        if not module_name.endswith(".py"):
            module_name += ".py"

        if not source.strip():
            raise ValueError(
                "Generated source cannot be empty."
            )

        return self.factory.write_text(
            project_id,
            f"code/{module_name}",
            source,
        )

    def create_json_data(
        self,
        project_id: str,
        filename: str,
        data: dict,
    ) -> Path:

        if not filename.endswith(".json"):
            filename += ".json"

        return self.factory.write_json(
            project_id,
            f"data/{filename}",
            data,
        )
