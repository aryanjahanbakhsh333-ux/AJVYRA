from dataclasses import dataclass, field
from typing import Callable, Dict, List, Optional


@dataclass
class StoryChoice:
    choice_id: str
    text: str
    next_scene: str
    effects: Dict[str, int] = field(default_factory=dict)


@dataclass
class StoryScene:
    scene_id: str
    title: str
    text: str
    choices: List[StoryChoice] = field(default_factory=list)


class StorySystem:
    def __init__(self):
        self.scenes: Dict[str, StoryScene] = {}
        self.current_scene: Optional[str] = None
        self.history: List[str] = []
        self.variables: Dict[str, int] = {}

    def add_scene(self, scene: StoryScene):
        self.scenes[scene.scene_id] = scene

    def start(self, scene_id: str):
        if scene_id not in self.scenes:
            raise KeyError(scene_id)

        self.current_scene = scene_id
        self.history = [scene_id]

    def current(self):
        if not self.current_scene:
            return None
        return self.scenes.get(self.current_scene)

    def choose(self, choice_id: str):
        scene = self.current()

        if not scene:
            return None

        choice = next(
            (c for c in scene.choices if c.choice_id == choice_id),
            None
        )

        if not choice:
            raise ValueError(f"Unknown choice: {choice_id}")

        for key, value in choice.effects.items():
            self.variables[key] = self.variables.get(key, 0) + value

        self.current_scene = choice.next_scene
        self.history.append(self.current_scene)

        return self.current()

    def export_state(self):
        return {
            "current_scene": self.current_scene,
            "history": self.history[:],
            "variables": self.variables.copy()
        }

    def import_state(self, data):
        self.current_scene = data.get("current_scene")
        self.history = list(data.get("history", []))
        self.variables = dict(data.get("variables", {}))
