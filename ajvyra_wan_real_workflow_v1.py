"""
AJVYRA — REAL WAN WORKFLOW BUILDER v1

Workflow باید یک ComfyUI API-format JSON واقعی باشد.

این فایل workflow را جعل نمی‌کند.
فقط مقادیر مورد نیاز را داخل workflow واقعی تزریق می‌کند.
"""

from __future__ import annotations

import copy
import json
import os
from pathlib import Path


class WorkflowError(RuntimeError):
    pass


class WanRealWorkflow:

    def __init__(self, workflow_path: Path):
        self.workflow_path = workflow_path

        if not workflow_path.exists():
            raise FileNotFoundError(
                f"Workflow not found: {workflow_path}"
            )

        self.base = json.loads(
            workflow_path.read_text(
                encoding="utf-8"
            )
        )

        if not isinstance(self.base, dict):
            raise WorkflowError(
                "Workflow must be a JSON object."
            )

    @staticmethod
    def _set_node_input(
        workflow: dict,
        node_id: str,
        input_name: str,
        value,
    ) -> None:

        node = workflow.get(str(node_id))

        if not node:
            raise WorkflowError(
                f"Workflow node not found: {node_id}"
            )

        inputs = node.setdefault(
            "inputs",
            {},
        )

        inputs[input_name] = value

    def build(
        self,
        prompt: str,
        negative_prompt: str,
        seed: int,
        width: int,
        height: int,
        frames: int,
    ) -> dict:

        workflow = copy.deepcopy(self.base)

        positive_node = os.getenv(
            "AJVYRA_WAN_POSITIVE_NODE",
            "",
        )

        positive_input = os.getenv(
            "AJVYRA_WAN_POSITIVE_INPUT",
            "text",
        )

        negative_node = os.getenv(
            "AJVYRA_WAN_NEGATIVE_NODE",
            "",
        )

        negative_input = os.getenv(
            "AJVYRA_WAN_NEGATIVE_INPUT",
            "text",
        )

        seed_node = os.getenv(
            "AJVYRA_WAN_SEED_NODE",
            "",
        )

        seed_input = os.getenv(
            "AJVYRA_WAN_SEED_INPUT",
            "seed",
        )

        width_node = os.getenv(
            "AJVYRA_WAN_WIDTH_NODE",
            "",
        )

        width_input = os.getenv(
            "AJVYRA_WAN_WIDTH_INPUT",
            "width",
        )

        height_node = os.getenv(
            "AJVYRA_WAN_HEIGHT_NODE",
            "",
        )

        height_input = os.getenv(
            "AJVYRA_WAN_HEIGHT_INPUT",
            "height",
        )

        frames_node = os.getenv(
            "AJVYRA_WAN_FRAMES_NODE",
            "",
        )

        frames_input = os.getenv(
            "AJVYRA_WAN_FRAMES_INPUT",
            "length",
        )

        if not positive_node:
            raise WorkflowError(
                "AJVYRA_WAN_POSITIVE_NODE is required."
            )

        if not negative_node:
            raise WorkflowError(
                "AJVYRA_WAN_NEGATIVE_NODE is required."
            )

        self._set_node_input(
            workflow,
            positive_node,
            positive_input,
            prompt,
        )

        self._set_node_input(
            workflow,
            negative_node,
            negative_input,
            negative_prompt,
        )

        if seed_node:
            self._set_node_input(
                workflow,
                seed_node,
                seed_input,
                int(seed),
            )

        if width_node:
            self._set_node_input(
                workflow,
                width_node,
                width_input,
                int(width),
            )

        if height_node:
            self._set_node_input(
                workflow,
                height_node,
                height_input,
                int(height),
            )

        if frames_node:
            self._set_node_input(
                workflow,
                frames_node,
                frames_input,
                int(frames),
            )

        return workflow
