from __future__ import annotations

import argparse
import json

from ajvyra_wan_real_factory_bridge_v2 import (
    AJVYRAWanRealFactoryBridgeV2,
)
from ajvyra_wan_30_film_shot_factory_v2 import (
    AJVYRA30FilmShotFactoryV2,
)
from ajvyra_wan_30_film_factory_v2 import (
    AJVYRAWan30FilmFactoryV2,
)


def main() -> int:

    parser = argparse.ArgumentParser(
        description="AJVYRA real 30-film Wan production"
    )

    parser.add_argument(
        "--wan-root",
        required=True,
    )

    parser.add_argument(
        "--checkpoint-dir",
        required=True,
    )

    parser.add_argument(
        "--manifest",
        required=True,
    )

    parser.add_argument(
        "--output-root",
        default="ajvyra_production",
    )

    parser.add_argument(
        "--python",
        default="python",
    )

    args = parser.parse_args()

    bridge = AJVYRAWanRealFactoryBridgeV2(
        wan_root=args.wan_root,
        checkpoint_dir=args.checkpoint_dir,
        output_root=args.output_root,
        python_executable=args.python,
    )

    shot_factory = AJVYRA30FilmShotFactoryV2(
        bridge=bridge,
        output_root=args.output_root,
    )

    factory = AJVYRAWan30FilmFactoryV2(
        shot_factory=shot_factory,
        manifest_path=args.manifest,
    )

    results = factory.produce_all()

    print(
        json.dumps(
            results,
            ensure_ascii=False,
            indent=2,
        )
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
