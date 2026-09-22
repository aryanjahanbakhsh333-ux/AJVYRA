"""
AJVYRA AI BOOT

ONE ENTRY POINT.

This is the file that starts the autonomous AJVYRA production system.

Examples:

    python ajvyra_ai_boot.py
    python ajvyra_ai_boot.py --once
    python ajvyra_ai_boot.py --continuous
    python ajvyra_ai_boot.py --status
    python ajvyra_ai_boot.py --validate
"""

from __future__ import annotations

import argparse
import json
import logging
import os
from pathlib import Path

from ajvyra_ai_autonomous_controller import (
    AJVYRAAutonomousController,
)

from ajvyra_ai_completion_gate import (
    AJVYRACompletionGate,
)

from ajvyra_ai_autonomous_publisher import (
    AJVYRAAutonomousPublisher,
)


logging.basicConfig(
    level=logging.INFO,
    format=(
        "%(asctime)s | "
        "AJVYRA-AI | "
        "%(levelname)s | "
        "%(message)s"
    ),
)


def build_parser() -> argparse.ArgumentParser:

    parser = argparse.ArgumentParser(
        description=(
            "AJVYRA Autonomous AI Production System"
        )
    )

    parser.add_argument(
        "--root",
        default=os.getenv(
            "AJVYRA_ROOT",
            ".",
        ),
    )

    parser.add_argument(
        "--once",
        action="store_true",
        help="Run one complete autonomous cycle.",
    )

    parser.add_argument(
        "--continuous",
        action="store_true",
        help="Continue production until targets are reached.",
    )

    parser.add_argument(
        "--status",
        action="store_true",
        help="Show current production status.",
    )

    parser.add_argument(
        "--validate",
        action="store_true",
        help="Validate all anime and games.",
    )

    parser.add_argument(
        "--publish",
        action="store_true",
        help="Publish only content passing the completion gate.",
    )

    parser.add_argument(
        "--interval",
        type=int,
        default=10,
        help="Seconds between autonomous cycles.",
    )

    return parser


def main() -> int:

    parser = build_parser()
    args = parser.parse_args()

    root = Path(
        args.root
    ).resolve()

    public_url = os.getenv(
        "AJVYRA_PUBLIC_BASE_URL",
        "",
    )

    controller = (
        AJVYRAAutonomousController(
            root=root,
            public_base_url=public_url,
        )
    )

    # ---------------------------------------------------------
    # STATUS
    # ---------------------------------------------------------

    if args.status:

        result = (
            controller.builder.status()
        )

        print(
            json.dumps(
                result,
                ensure_ascii=False,
                indent=2,
            )
        )

        return 0

    # ---------------------------------------------------------
    # VALIDATION
    # ---------------------------------------------------------

    if args.validate:

        gate = AJVYRACompletionGate(
            root
        )

        result = (
            gate.validate_everything()
        )

        print(
            json.dumps(
                result,
                ensure_ascii=False,
                indent=2,
            )
        )

        return 0

    # ---------------------------------------------------------
    # PUBLISH
    # ---------------------------------------------------------

    if args.publish:

        publisher = (
            AJVYRAAutonomousPublisher(
                root=root,
                public_base_url=public_url,
            )
        )

        result = (
            publisher.publish_ready_content()
        )

        print(
            json.dumps(
                result,
                ensure_ascii=False,
                indent=2,
            )
        )

        return 0

    # ---------------------------------------------------------
    # CONTINUOUS
    # ---------------------------------------------------------

    if args.continuous:

        result = controller.start(
            continuous=True,
            interval_seconds=args.interval,
        )

        print(
            json.dumps(
                result,
                ensure_ascii=False,
                indent=2,
            )
        )

        return 0

    # ---------------------------------------------------------
    # DEFAULT / ONCE
    # ---------------------------------------------------------

    result = controller.start(
        continuous=False
    )

    print(
        json.dumps(
            result,
            ensure_ascii=False,
            indent=2,
        )
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(
        main()
    )
