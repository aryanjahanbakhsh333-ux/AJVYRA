from __future__ import annotations

import copy
import json
from pathlib import Path


class WanWorkflow:

    def __init__(self, workflow_file: Path):
        self.workflow_file = workflow_file

    def load(self):
        data = json.loads(
            self.workflow_file.read_text(
                encoding="utf-8"
            )
        )

        if not isinstance(data, dict):
            raise ValueError(
                "ComfyUI workflow must be a JSON object."
            )

        return data

    def build(
        self,
        prompt: str,
        negative_prompt: str,
        seed: int,
        width: int,
        height: int,
    ):
        workflow = copy.deepcopy(
            self.load()
        )

        positive_found = False
        negative_found = False

        for node_id, node in workflow.items():

            if not isinstance(node, dict):
                continue

            inputs = node.get("inputs")

            if not isinstance(inputs, dict):
                continue

            class_type = str(
                node.get("class_type", "")
            ).lower()

            title = str(
                node.get("_meta", {}).get(
                    "title",
                    ""
                )
            ).lower()

            if (
                "text" in class_type
                or "text" in title
                or "prompt" in title
            ):
                if (
                    not positive_found
                    and (
                        "positive" in title
                        or "positive" in class_type
                    )
                ):
                    inputs["text"] = prompt
                    positive_found = True

                elif (
                    not negative_found
                    and (
                        "negative" in title
                        or "negative" in class_type
                    )
                ):
                    inputs["text"] = negative_prompt
                    negative_found = True

            if "seed" in inputs:
                inputs["seed"] = seed

            if "width" in inputs:
                inputs["width"] = width

            if "height" in inputs:
                inputs["height"] = height

        if not positive_found:
            raise RuntimeError(
                "Positive prompt node was not detected "
                "in the Wan workflow."
            )

        if not negative_found:
            raise RuntimeError(
                "Negative prompt node was not detected "
                "in the Wan workflow."
            )

        return workflow
