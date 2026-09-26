from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List


@dataclass
class SceneObject:
    object_id: str
    kind: str
    x: float
    y: float
    width: float = 1.0
    height: float = 1.0
    rotation: float = 0.0
    visible: bool = True
    layer: int = 0
    properties: Dict[str, Any] = field(
        default_factory=dict
    )


class VisualScene:
    def __init__(
        self,
        width: int = 1280,
        height: int = 720,
    ):
        self.width = width
        self.height = height
        self.background = "#050505"
        self.objects: List[SceneObject] = []

    def add(
        self,
        object_id: str,
        kind: str,
        x: float,
        y: float,
        **kwargs: Any,
    ) -> SceneObject:
        obj = SceneObject(
            object_id=object_id,
            kind=kind,
            x=float(x),
            y=float(y),
            **kwargs,
        )

        self.objects.append(obj)
        return obj

    def remove(self, object_id: str) -> bool:
        before = len(self.objects)

        self.objects = [
            item
            for item in self.objects
            if item.object_id != object_id
        ]

        return len(self.objects) != before

    def update(
        self,
        object_id: str,
        **changes: Any,
    ) -> bool:
        for obj in self.objects:
            if obj.object_id == object_id:
                for key, value in changes.items():
                    if hasattr(obj, key):
                        setattr(obj, key, value)
                    else:
                        obj.properties[key] = value

                return True

        return False

    def export(self) -> Dict[str, Any]:
        ordered = sorted(
            self.objects,
            key=lambda item: item.layer,
        )

        return {
            "viewport": {
                "width": self.width,
                "height": self.height,
            },
            "background": self.background,
            "objects": [
                {
                    "id": obj.object_id,
                    "kind": obj.kind,
                    "x": obj.x,
                    "y": obj.y,
                    "width": obj.width,
                    "height": obj.height,
                    "rotation": obj.rotation,
                    "visible": obj.visible,
                    "layer": obj.layer,
                    "properties": dict(
                        obj.properties
                    ),
                }
                for obj in ordered
            ],
        }
