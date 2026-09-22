from __future__ import annotations

import argparse
import json
from pathlib import Path

from ajvyra_anime_pre_render_gate_v3 import (
    AJVYRAAnimePreRenderGateV3,
)

from ajvyra_anime_site_render_lock_v3 import (
    AJVYRAAnimeSiteRenderLockV3,
)

from ajvyra_anime_final_asset_index_v3 import (
    AJVYRAAnimeFinalAssetIndexV3,
)


def main() -> int:

    parser = argparse.ArgumentParser(
        description=(
            "AJVYRA final anime pre-render "
            "release gate"
        )
    )

    parser.add_argument(
        "--manifest",
        required=True,
    )

    parser.add_argument(
        "--asset-index",
        default="release/anime-assets.json",
    )

    parser.add_argument(
        "--render-lock",
        default="release/anime-render-approved.json",
    )

    args = parser.parse_args()

    manifest_path = Path(
        args.manifest
    )

    if not manifest_path.exists():
        raise SystemExit(
            "RELEASE BLOCKED: "
            "anime release manifest is missing."
        )

    manifest = json.loads(
        manifest_path.read_text(
            encoding="utf-8"
        )
    )

    gate = AJVYRAAnimePreRenderGateV3(
        str(manifest_path)
    )

    gate.verify()

    index_builder = (
        AJVYRAAnimeFinalAssetIndexV3(
            args.asset_index
        )
    )

    index = index_builder.build(
        manifest
    )

    lock = AJVYRAAnimeSiteRenderLockV3(
        release_manifest=str(
            manifest_path
        ),
        lock_file=args.render_lock,
    )

    approval = lock.approve()

    print(
        json.dumps(
            {
                "project": "AJVYRA",
                "anime": index["anime_count"],
                "site_render": approval[
                    "site_render"
                ],
                "status": "READY",
            },
            ensure_ascii=False,
            indent=2,
        )
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
