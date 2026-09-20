from dataclasses import dataclass


@dataclass
class DeviceInfo:
    user_agent: str
    device: str
    mobile: bool
    touch: bool


class DeviceDetector:

    def detect(
        self,
        user_agent: str,
        touch: bool = False
    ) -> DeviceInfo:

        ua = user_agent.lower()

        if "iphone" in ua:
            device = "iPhone"
            mobile = True

        elif "ipad" in ua:
            device = "iPad"
            mobile = True

        elif "android" in ua:
            device = "Android"
            mobile = True

        elif "windows" in ua:
            device = "Windows"
            mobile = False

        elif "macintosh" in ua or "mac os" in ua:
            device = "macOS"
            mobile = False

        elif "linux" in ua:
            device = "Linux"
            mobile = False

        else:
            device = "Unknown"
            mobile = False

        return DeviceInfo(
            user_agent=user_agent,
            device=device,
            mobile=mobile,
            touch=touch,
        )

    def is_mobile(self, user_agent: str):
        return self.detect(user_agent).mobile

    def recommended_layout(self, user_agent: str):
        return (
            "mobile"
            if self.is_mobile(user_agent)
            else "desktop"
        )
