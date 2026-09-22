from __future__ import annotations

import math
import random
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Tuple

try:
    from PIL import Image, ImageDraw, ImageFilter
except ImportError:
    Image = None
    ImageDraw = None
    ImageFilter = None


@dataclass
class VisualStyle:
    width: int = 1280
    height: int = 720
    fps: int = 24
    style: str = "anime"
    seed: int = 42


@dataclass
class VisualCharacter:
    name: str
    x: float
    y: float
    scale: float = 1.0
    hair: str = "dark"
    skin: str = "light"
    outfit: str = "dark"
    expression: str = "neutral"


class NativeVisualEngine:
    """
    Procedural visual engine for AJVYRA.

    It creates original stylized anime-like frames using deterministic
    drawing algorithms. No external image-generation model is required.
    """

    def __init__(self, style: VisualStyle | None = None):
        self.style = style or VisualStyle()
        self.random = random.Random(self.style.seed)

        if Image is None:
            raise RuntimeError(
                "Pillow is required. Install it with: pip install pillow"
            )

    def _gradient_background(self, scene_type: str, frame: int):
        w, h = self.style.width, self.style.height

        palette = {
            "night": ((16, 21, 38), (72, 78, 110)),
            "rain": ((25, 34, 48), (93, 104, 120)),
            "sunset": ((75, 48, 63), (210, 145, 103)),
            "forest": ((20, 43, 39), (85, 113, 88)),
            "city": ((23, 29, 43), (92, 99, 119)),
            "fantasy": ((39, 31, 67), (115, 91, 143)),
            "space": ((5, 8, 22), (36, 45, 88)),
            "default": ((31, 36, 48), (108, 113, 128)),
        }

        top, bottom = palette.get(scene_type, palette["default"])

        img = Image.new("RGB", (w, h))
        pixels = img.load()

        for y in range(h):
            t = y / max(1, h - 1)

            for x in range(w):
                wave = math.sin((x / w) * math.pi * 2 + frame * 0.002) * 2

                r = int(top[0] * (1 - t) + bottom[0] * t + wave)
                g = int(top[1] * (1 - t) + bottom[1] * t + wave)
                b = int(top[2] * (1 - t) + bottom[2] * t + wave)

                pixels[x, y] = (
                    max(0, min(255, r)),
                    max(0, min(255, g)),
                    max(0, min(255, b)),
                )

        return img

    def _draw_sun_or_moon(self, draw, scene_type: str):
        w = self.style.width

        if scene_type in {"night", "rain", "space", "fantasy"}:
            cx, cy = int(w * 0.78), 115
            radius = 48
        else:
            cx, cy = int(w * 0.78), 120
            radius = 55

        draw.ellipse(
            (
                cx - radius,
                cy - radius,
                cx + radius,
                cy + radius,
            ),
            fill=(220, 222, 205),
        )

        if scene_type == "night":
            draw.ellipse(
                (
                    cx - radius + 18,
                    cy - radius - 3,
                    cx + radius + 18,
                    cy + radius - 3,
                ),
                fill=(40, 47, 65),
            )

    def _draw_environment(self, draw, scene_type: str, frame: int):
        w, h = self.style.width, self.style.height

        horizon = int(h * 0.66)

        if scene_type in {"city", "night", "rain"}:
            buildings = [
                (0, 390, 145, horizon),
                (120, 330, 270, horizon),
                (245, 430, 375, horizon),
                (350, 300, 505, horizon),
                (480, 380, 620, horizon),
                (595, 325, 750, horizon),
                (730, 410, 900, horizon),
                (875, 350, 1030, horizon),
                (1000, 300, 1160, horizon),
                (1130, 385, 1280, horizon),
            ]

            for i, (x1, y1, x2, y2) in enumerate(buildings):
                shade = 30 + (i % 4) * 8

                draw.rectangle(
                    (x1, y1, x2, y2),
                    fill=(shade, shade + 5, shade + 14),
                )

                for wy in range(y1 + 25, y2 - 10, 38):
                    for wx in range(x1 + 15, x2 - 10, 35):
                        if (wx + wy + frame // 8) % 5 == 0:
                            draw.rectangle(
                                (wx, wy, wx + 8, wy + 12),
                                fill=(170, 155, 110),
                            )

        elif scene_type == "forest":
            for i in range(20):
                x = (i * 83) % w
                height = 150 + ((i * 47) % 180)

                draw.polygon(
                    [
                        (x, horizon),
                        (x + 55, horizon),
                        (x + 28, horizon - height),
                    ],
                    fill=(22, 53 + i % 20, 43),
                )

        elif scene_type == "space":
            for i in range(100):
                x = (i * 83 + frame) % w
                y = (i * 47) % int(h * 0.8)

                draw.ellipse(
                    (x, y, x + 2, y + 2),
                    fill=(210, 215, 225),
                )

        else:
            draw.rectangle(
                (0, horizon, w, h),
                fill=(35, 39, 43),
            )

        draw.rectangle(
            (0, horizon, w, h),
            fill=None,
            outline=(0, 0, 0),
            width=2,
        )

    def _draw_character(
        self,
        image,
        character: VisualCharacter,
        frame: int,
    ):
        draw = ImageDraw.Draw(image)

        x = int(character.x * self.style.width)
        ground = int(character.y * self.style.height)

        s = character.scale

        head_r = int(48 * s)
        body_w = int(82 * s)
        body_h = int(145 * s)

        bob = math.sin(frame * 0.08) * 3 * s

        head_y = ground - body_h - head_r * 2 + int(bob)

        skin = {
            "light": (238, 205, 185),
            "pale": (225, 220, 211),
            "warm": (194, 143, 112),
            "cool": (184, 195, 210),
        }.get(character.skin, (230, 200, 180))

        hair = {
            "dark": (25, 27, 34),
            "black": (10, 12, 17),
            "white": (225, 228, 230),
            "silver": (155, 163, 177),
            "blue": (48, 68, 100),
            "red": (91, 32, 40),
        }.get(character.hair, (25, 27, 34))

        outfit = {
            "dark": (24, 27, 34),
            "school": (39, 48, 65),
            "coat": (47, 43, 51),
            "fantasy": (62, 49, 74),
            "white": (205, 205, 202),
        }.get(character.outfit, (24, 27, 34))

        # body
        draw.rounded_rectangle(
            (
                x - body_w,
                ground - body_h,
                x + body_w,
                ground,
            ),
            radius=int(25 * s),
            fill=outfit,
        )

        # neck
        draw.rectangle(
            (
                x - int(15 * s),
                head_y + head_r * 2 - 5,
                x + int(15 * s),
                head_y + head_r * 2 + int(35 * s),
            ),
            fill=skin,
        )

        # head
        draw.ellipse(
            (
                x - head_r,
                head_y,
                x + head_r,
                head_y + head_r * 2,
            ),
            fill=skin,
            outline=(20, 20, 25),
            width=max(1, int(3 * s)),
        )

        # hair
        hair_points = [
            (x - head_r - 4, head_y + head_r),
            (x - head_r + 10, head_y - 15),
            (x - 20, head_y - 32),
            (x + 5, head_y - 20),
            (x + 30, head_y - 37),
            (x + head_r + 4, head_y + 10),
            (x + head_r - 10, head_y + head_r),
        ]

        draw.polygon(hair_points, fill=hair)

        # eyes
        eye_y = head_y + int(head_r * 0.95)
        eye_offset = int(head_r * 0.42)

        eye_w = max(4, int(11 * s))
        eye_h = max(3, int(6 * s))

        draw.ellipse(
            (
                x - eye_offset - eye_w,
                eye_y - eye_h,
                x - eye_offset + eye_w,
                eye_y + eye_h,
            ),
            fill=(18, 20, 26),
        )

        draw.ellipse(
            (
                x + eye_offset - eye_w,
                eye_y - eye_h,
                x + eye_offset + eye_w,
                eye_y + eye_h,
            ),
            fill=(18, 20, 26),
        )

        # expression
        if character.expression == "sad":
            draw.arc(
                (
                    x - 20,
                    eye_y + 15,
                    x + 20,
                    eye_y + 45,
                ),
                200,
                340,
                fill=(80, 45, 50),
                width=max(1, int(3 * s)),
            )

        elif character.expression == "happy":
            draw.arc(
                (
                    x - 20,
                    eye_y + 8,
                    x + 20,
                    eye_y + 40,
                ),
                20,
                160,
                fill=(80, 35, 40),
                width=max(1, int(3 * s)),
            )

        else:
            draw.line(
                (
                    x - 12,
                    eye_y + 26,
                    x + 12,
                    eye_y + 26,
                ),
                fill=(65, 40, 45),
                width=max(1, int(2 * s)),
            )

        # arm movement
        arm_shift = math.sin(frame * 0.06) * 5 * s

        draw.line(
            (
                x - body_w + 8,
                ground - body_h + 40,
                x - body_w - 35,
                ground - body_h + 100 + arm_shift,
            ),
            fill=outfit,
            width=max(8, int(18 * s)),
        )

        draw.line(
            (
                x + body_w - 8,
                ground - body_h + 40,
                x + body_w + 35,
                ground - body_h + 100 - arm_shift,
            ),
            fill=outfit,
            width=max(8, int(18 * s)),
        )

    def render_frame(
        self,
        scene_type: str = "night",
        characters: list[VisualCharacter] | None = None,
        frame: int = 0,
    ):
        image = self._gradient_background(scene_type, frame)
        draw = ImageDraw.Draw(image)

        self._draw_sun_or_moon(draw, scene_type)
        self._draw_environment(draw, scene_type, frame)

        if characters:
            for character in characters:
                self._draw_character(image, character, frame)

        if scene_type == "rain":
            for i in range(180):
                x = (i * 71 + frame * 7) % self.style.width
                y = (i * 37 + frame * 15) % self.style.height

                draw.line(
                    (x, y, x - 5, y + 18),
                    fill=(150, 170, 190),
                    width=1,
                )

        if scene_type == "night":
            overlay = Image.new(
                "RGBA",
                image.size,
                (8, 12, 25, 30),
            )
            image = Image.alpha_composite(
                image.convert("RGBA"),
                overlay,
            ).convert("RGB")

        return image

    def render_preview(
        self,
        output: str | Path,
        scene_type: str = "night",
        characters: list[VisualCharacter] | None = None,
    ) -> Path:
        output = Path(output)
        output.parent.mkdir(parents=True, exist_ok=True)

        image = self.render_frame(
            scene_type=scene_type,
            characters=characters,
            frame=0,
        )

        image.save(output)
        return output


if __name__ == "__main__":
    engine = NativeVisualEngine()

    engine.render_preview(
        "ajvyra_projects/visual_preview.png",
        scene_type="night",
        characters=[
            VisualCharacter(
                name="Character_A",
                x=0.50,
                y=0.91,
                scale=1.35,
                hair="black",
                outfit="dark",
                expression="sad",
            )
        ],
    )

    print("AJVYRA native visual preview created.")
