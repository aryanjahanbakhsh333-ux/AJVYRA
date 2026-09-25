"""
AJVYRA Mobile Device Adapter v1

Device/orientation information supplied by the frontend.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict


@dataclass
class DeviceProfile:
    device_type: str
    touch: bool
    orientation: str
    width: int
    height: int
    dpr: float

    @property
    def is_mobile(self) -> bool:
        return self.device_type in {"phone", "tablet"}

    @property
    def is_landscape(self) -> bool:
        return self.orientation == "landscape"


class MobileDeviceAdapter:
    PHONE_LIMIT = 768
    TABLET_LIMIT = 1200

    def detect(
        self,
        width: int,
        height: int,
        touch: bool = False,
        user_agent: str = "",
        dpr: float = 1.0,
    ) -> DeviceProfile:
        width = int(width)
        height = int(height)

        ua = user_agent.lower()

        mobile_hint = any(
            token in ua
            for token in (
                "iphone",
                "android",
                "mobile",
                "ipad",
            )
        )

        if mobile_hint or touch:
            if min(width, height) <= self.PHONE_LIMIT:
                device_type = "phone"
            else:
                device_type = "tablet"
        else:
            device_type = "desktop"

        orientation = (
            "landscape"
            if width >= height
            else "portrait"
        )

        return DeviceProfile(
            device_type=device_type,
            touch=bool(touch),
            orientation=orientation,
            width=width,
            height=height,
            dpr=float(dpr),
        )

    def runtime_config(
        self,
        profile: DeviceProfile,
    ) -> Dict[str, Any]:
        return {
            "device": profile.device_type,
            "touch_controls": profile.touch,
            "orientation": profile.orientation,
            "prefer_landscape": profile.is_mobile,
            "width": profile.width,
            "height": profile.height,
            "dpr": profile.dpr,
        }
