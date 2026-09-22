from __future__ import annotations

from pathlib import Path
import json
import hashlib
from datetime import datetime, timezone


class AJVYRAGamesFinalClosure:
    """
    FINAL GAMES CLOSURE

    This is the final integration layer for AJVYRA Games.

    It does NOT create another game engine.

    It connects and finalizes the systems that already exist:

        70 Game Runtime
              ↓
        Asset / Model Runtime
              ↓
        Browser Runtime
              ↓
        Offline Cache
              ↓
        Runtime Safety
              ↓
        Mobile Compatibility
              ↓
        Release Manifest
              ↓
        Final Health Report

    After this file has run successfully, the Games core
    should be considered CLOSED.

    Future work can add content/assets/models/providers,
    but should not require another Games core rewrite.
    """

    VERSION = "1.0.0-FINAL"

    EXPECTED_GAMES = 70

    REQUIRED_GAME_FILES = (
        "index.html",
        "game.js",
        "game.css",
        "metadata.json",
        "production.json",
        "asset_connection.json",
    )

    REQUIRED_ASSET_FILES = (
        "asset_registry.json",
        "asset_manifest.json",
    )

    REQUIRED_RUNTIME_MARKERS = (
        "requestAnimationFrame",
        "localStorage",
        "AJVYRA_ASSET_RUNTIME",
    )

    def __init__(
        self,
        games_root="generated/final_games",
        assets_root="generated/ajvyra_assets",
        release_root="release/ajvyra_games",
    ):
        self.games_root = Path(games_root)
        self.assets_root = Path(assets_root)
        self.release_root = Path(release_root)

        self.report = {
            "project": "AJVYRA",
            "system": "GAMES_FINAL_CLOSURE",
            "version": self.VERSION,
            "started_at": self._now(),
            "expected_games": self.EXPECTED_GAMES,
            "games": [],
            "errors": [],
            "warnings": [],
        }

    # ---------------------------------------------------------
    # BASIC UTILITIES
    # ---------------------------------------------------------

    @staticmethod
    def _now():
        return datetime.now(
            timezone.utc
        ).isoformat()

    @staticmethod
    def _sha256(path: Path):
        digest = hashlib.sha256()

        with path.open("rb") as file:
            while True:
                chunk = file.read(1024 * 1024)

                if not chunk:
                    break

                digest.update(chunk)

        return digest.hexdigest()

    @staticmethod
    def _write(path: Path, content: str):
        path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        path.write_text(
            content,
            encoding="utf-8",
        )

    # ---------------------------------------------------------
    # VALIDATE GAME
    # ---------------------------------------------------------

    def validate_game(self, game_id: int):
        game_dir = (
            self.games_root /
            f"game_{game_id:02d}"
        )

        result = {
            "game_id": game_id,
            "directory": str(game_dir),
            "valid": True,
            "errors": [],
            "warnings": [],
        }

        if not game_dir.exists():
            result["valid"] = False
            result["errors"].append(
                "Game directory does not exist."
            )
            return result

        # Required files
        for filename in self.REQUIRED_GAME_FILES:
            path = game_dir / filename

            if not path.is_file():
                result["valid"] = False

                result["errors"].append(
                    f"Missing game file: {filename}"
                )

        # Metadata
        metadata_path = (
            game_dir /
            "metadata.json"
        )

        metadata = {}

        if metadata_path.exists():
            try:
                metadata = json.loads(
                    metadata_path.read_text(
                        encoding="utf-8"
                    )
                )
            except Exception as exc:
                result["valid"] = False

                result["errors"].append(
                    f"Invalid metadata.json: {exc}"
                )

        if metadata:
            if metadata.get("id") != game_id:
                result["warnings"].append(
                    "Metadata ID differs from directory ID."
                )

            if not metadata.get("title"):
                result["valid"] = False
                result["errors"].append(
                    "Game title is missing."
                )

            if not metadata.get("genre"):
                result["valid"] = False
                result["errors"].append(
                    "Game genre is missing."
                )

            if metadata.get("playable") is not True:
                result["valid"] = False
                result["errors"].append(
                    "Game is not marked playable."
                )

        # JavaScript runtime
        game_js = game_dir / "game.js"

        if game_js.exists():
            content = game_js.read_text(
                encoding="utf-8"
            )

            for marker in self.REQUIRED_RUNTIME_MARKERS:
                if marker not in content:
                    result["warnings"].append(
                        f"Runtime marker missing: {marker}"
                    )

        # Asset connection
        connection_path = (
            game_dir /
            "asset_connection.json"
        )

        if connection_path.exists():
            try:
                connection = json.loads(
                    connection_path.read_text(
                        encoding="utf-8"
                    )
                )

                if not connection.get(
                    "runtime_connected"
                ):
                    result["valid"] = False

                    result["errors"].append(
                        "Asset runtime is not connected."
                    )

            except Exception as exc:
                result["valid"] = False

                result["errors"].append(
                    f"Invalid asset connection: {exc}"
                )

        # Asset registry
        asset_dir = (
            self.assets_root /
            f"game_{game_id:02d}"
        )

        for filename in self.REQUIRED_ASSET_FILES:
            path = asset_dir / filename

            if not path.exists():
                result["valid"] = False

                result["errors"].append(
                    f"Missing asset file: "
                    f"{filename}"
                )

        result["metadata"] = metadata

        return result

    # ---------------------------------------------------------
    # FINAL RUNTIME SUPPORT
    # ---------------------------------------------------------

    def create_completion_runtime(self):
        """
        Browser-side final safety/runtime layer.

        It does not replace game.js.
        It sits beside the existing runtime.
        """

        return r"""
(() => {
    "use strict";

    if (window.__AJVYRA_FINAL_RUNTIME__) {
        return;
    }

    window.__AJVYRA_FINAL_RUNTIME__ = true;

    const state = {
        startedAt: performance.now(),
        errors: 0,
        visible: true,
        fps: 60
    };

    window.AJVYRA_FINAL_RUNTIME_STATE = state;

    /*
     * Runtime error guard.
     */

    window.addEventListener(
        "error",
        () => {
            state.errors += 1;
        }
    );

    window.addEventListener(
        "unhandledrejection",
        () => {
            state.errors += 1;
        }
    );

    /*
     * Mobile visibility handling.
     */

    document.addEventListener(
        "visibilitychange",
        () => {
            state.visible =
                !document.hidden;

            window.dispatchEvent(
                new CustomEvent(
                    "ajvyra:visibility",
                    {
                        detail: {
                            visible:
                                state.visible
                        }
                    }
                )
            );
        }
    );

    /*
     * Performance monitor.
     */

    let previous =
        performance.now();

    let frames = 0;

    function performanceLoop(now) {
        frames += 1;

        const elapsed =
            now - previous;

        if (elapsed >= 1000) {
            state.fps = frames;

            frames = 0;
            previous = now;

            window.dispatchEvent(
                new CustomEvent(
                    "ajvyra:performance",
                    {
                        detail: {
                            fps: state.fps
                        }
                    }
                )
            );
        }

        requestAnimationFrame(
            performanceLoop
        );
    }

    requestAnimationFrame(
        performanceLoop
    );

    /*
     * Fullscreen helper.
     */

    window.AJVYRA_FULLSCREEN = async () => {
        try {
            if (
                !document.fullscreenElement &&
                document.documentElement.requestFullscreen
            ) {
                await document.documentElement
                    .requestFullscreen();

                return true;
            }
        } catch (_) {}

        return false;
    };

    /*
     * Safe vibration.
     */

    window.AJVYRA_VIBRATE = (
        pattern = 20
    ) => {
        try {
            if (
                "vibrate" in navigator
            ) {
                navigator.vibrate(
                    pattern
                );

                return true;
            }
        } catch (_) {}

        return false;
    };

    /*
     * Audio readiness.

       Web Audio is initialized only after
       user interaction because browsers
       commonly require a user gesture.
    */

    let audioContext = null;

    window.AJVYRA_AUDIO = {
        getContext() {
            if (!audioContext) {
                const AudioContext =
                    window.AudioContext ||
                    window.webkitAudioContext;

                if (AudioContext) {
                    audioContext =
                        new AudioContext();
                }
            }

            return audioContext;
        },

        async resume() {
            const context =
                this.getContext();

            if (!context) {
                return false;
            }

            try {
                if (
                    context.state ===
                    "suspended"
                ) {
                    await context.resume();
                }

                return true;
            } catch (_) {
                return false;
            }
        }
    };

    /*
     * Asset readiness helper.
     */

    window.AJVYRA_WAIT_FOR_ASSETS =
        async (
            timeout = 10000
        ) => {
            const start =
                performance.now();

            while (
                !window.AJVYRA_ASSETS_READY &&
                performance.now() - start <
                    timeout
            ) {
                await new Promise(
                    resolve =>
                        setTimeout(
                            resolve,
                            50
                        )
                );
            }

            return Boolean(
                window.AJVYRA_ASSETS_READY
            );
        };

    /*
     * Final runtime information.
     */

    window.AJVYRA_RUNTIME_INFO = () => ({
        version: "1.0.0-FINAL",
        mobile:
            /Android|iPhone|iPad|iPod/i
                .test(
                    navigator.userAgent
                ),
        canvas:
            Boolean(
                document.querySelector(
                    "canvas"
                )
            ),
        audio:
            Boolean(
                window.AudioContext ||
                window.webkitAudioContext
            ),
        serviceWorker:
            "serviceWorker" in navigator,
        indexedDB:
            "indexedDB" in window,
        localStorage:
            (() => {
                try {
                    return Boolean(
                        window.localStorage
                    );
                } catch (_) {
                    return false;
                }
            })()
    });
})();
"""

    # ---------------------------------------------------------
    # SERVICE WORKER
    # ---------------------------------------------------------

    def create_service_worker(self):
        return r"""
const CACHE_NAME =
    "ajvyra-games-final-v1";

const CORE_FILES = [
    "./",
    "./index.html",
    "./game.js",
    "./game.css",
    "./metadata.json",
    "./production.json",
    "./asset_connection.json"
];

self.addEventListener(
    "install",
    event => {
        event.waitUntil(
            caches.open(
                CACHE_NAME
            ).then(
                cache =>
                    cache.addAll(
                        CORE_FILES
                    )
            ).catch(
                () => {}
            )
        );

        self.skipWaiting();
    }
);

self.addEventListener(
    "activate",
    event => {
        event.waitUntil(
            caches.keys().then(
                keys =>
                    Promise.all(
                        keys
                            .filter(
                                key =>
                                    key !==
                                    CACHE_NAME
                            )
                            .map(
                                key =>
                                    caches.delete(
                                        key
                                    )
                            )
                    )
            )
        );

        self.clients.claim();
    }
);

self.addEventListener(
    "fetch",
    event => {
        const request =
            event.request;

        if (
            request.method !== "GET"
        ) {
            return;
        }

        event.respondWith(
            caches.match(request)
                .then(
                    cached => {
                        if (cached) {
                            return cached;
                        }

                        return fetch(
                            request
                        ).then(
                            response => {
                                if (
                                    response &&
                                    response.ok
                                ) {
                                    const clone =
                                        response.clone();

                                    caches.open(
                                        CACHE_NAME
                                    ).then(
                                        cache =>
                                            cache.put(
                                                request,
                                                clone
                                            )
                                    );
                                }

                                return response;
                            }
                        );
                    }
                )
                .catch(
                    () =>
                        caches.match(
                            "./index.html"
                        )
                )
        );
    }
);
"""

    # ---------------------------------------------------------
    # INDEX PATCH
    # ---------------------------------------------------------

    def patch_index(self, game_dir: Path):
        index = game_dir / "index.html"

        if not index.exists():
            return False

        content = index.read_text(
            encoding="utf-8"
        )

        runtime_tag = (
            '<script src="ajvyra_final_runtime.js"></script>'
        )

        if runtime_tag not in content:
            content = content.replace(
                "</head>",
                f"{runtime_tag}\n</head>"
            )

        service_worker = """
<script>
if ("serviceWorker" in navigator) {
    window.addEventListener(
        "load",
        () => {
            navigator.serviceWorker
                .register("./sw.js")
                .catch(() => {});
        }
    );
}
</script>
"""

        marker = (
            "AJVYRA_FINAL_SERVICE_WORKER"
        )

        if marker not in content:
            service_worker = (
                f"<!-- {marker} -->\n"
                + service_worker
            )

            content = content.replace(
                "</body>",
                service_worker +
                "\n</body>"
            )

        self._write(
            index,
            content,
        )

        return True

    # ---------------------------------------------------------
    # FINALIZE ONE GAME
    # ---------------------------------------------------------

    def finalize_game(self, game_id):
        result = self.validate_game(
            game_id
        )

        game_dir = (
            self.games_root /
            f"game_{game_id:02d}"
        )

        if not result["valid"]:
            return result

        # Final runtime
        self._write(
            game_dir /
            "ajvyra_final_runtime.js",
            self.create_completion_runtime(),
        )

        # Offline worker
        self._write(
            game_dir /
            "sw.js",
            self.create_service_worker(),
        )

        # PWA manifest
        metadata = result.get(
            "metadata",
            {}
        )

        manifest = {
            "name": metadata.get(
                "title",
                f"AJVYRA Game {game_id}",
            ),
            "short_name": metadata.get(
                "title",
                f"Game {game_id}",
            ),
            "start_url": "./index.html",
            "display": "fullscreen",
            "orientation": "any",
            "background_color": "#080a10",
            "theme_color": "#080a10",
            "description": metadata.get(
                "objective",
                "AJVYRA playable game",
            ),
        }

        self._write(
            game_dir /
            "manifest.webmanifest",
            json.dumps(
                manifest,
                ensure_ascii=False,
                indent=2,
            ),
        )

        # Patch HTML
        self.patch_index(
            game_dir
        )

        # Runtime checksum
        checksums = {}

        for path in game_dir.rglob("*"):
            if (
                path.is_file() and
                path.name !=
                "checksums.json"
            ):
                checksums[
                    str(
                        path.relative_to(
                            game_dir
                        )
                    )
                ] = self._sha256(
                    path
                )

        self._write(
            game_dir /
            "checksums.json",
            json.dumps(
                checksums,
                ensure_ascii=False,
                indent=2,
            ),
        )

        result["finalized"] = True
        result["offline"] = True
        result["pwa"] = True
        result["runtime_guard"] = True
        result["checksums"] = True

        return result

    # ---------------------------------------------------------
    # FINAL RELEASE
    # ---------------------------------------------------------

    def build_release_manifest(
        self,
        results,
    ):
        games = []

        for result in results:
            if not result.get(
                "finalized"
            ):
                continue

            metadata = result.get(
                "metadata",
                {}
            )

            games.append({
                "id": result["game_id"],
                "title": metadata.get(
                    "title"
                ),
                "genre": metadata.get(
                    "genre"
                ),
                "path":
                    f"game_"
                    f"{result['game_id']:02d}/"
                    f"index.html",
                "playable": True,
                "offline": True,
                "pwa": True,
            })

        manifest = {
            "project": "AJVYRA",
            "release": "FINAL",
            "system":
                "GAMES_CLOSED",
            "version": self.VERSION,
            "generated_at": self._now(),
            "total_games": len(games),
            "games": games,
        }

        return manifest

    # ---------------------------------------------------------
    # MAIN FINALIZATION
    # ---------------------------------------------------------

    def run(self):
        if not self.games_root.exists():
            raise FileNotFoundError(
                f"Missing games root: "
                f"{self.games_root}"
            )

        self.release_root.mkdir(
            parents=True,
            exist_ok=True,
        )

        results = []

        for game_id in range(
            1,
            self.EXPECTED_GAMES + 1
        ):
            try:
                result = self.finalize_game(
                    game_id
                )

            except Exception as exc:
                result = {
                    "game_id": game_id,
                    "valid": False,
                    "finalized": False,
                    "errors": [
                        str(exc)
                    ],
                }

            results.append(result)

        finalized = [
            r for r in results
            if r.get("finalized")
        ]

        failed = [
            r for r in results
            if not r.get("finalized")
        ]

        release_manifest = (
            self.build_release_manifest(
                results
            )
        )

        # Release manifest
        self._write(
            self.release_root /
            "release_manifest.json",
            json.dumps(
                release_manifest,
                ensure_ascii=False,
                indent=2,
            ),
        )

        # Final health report
        self.report["games"] = results
        self.report["finished_at"] = (
            self._now()
        )
        self.report["finalized_games"] = (
            len(finalized)
        )
        self.report["failed_games"] = (
            len(failed)
        )
        self.report["complete"] = (
            len(finalized) ==
            self.EXPECTED_GAMES
        )

        self._write(
            self.games_root /
            "FINAL_GAME_HEALTH_REPORT.json",
            json.dumps(
                self.report,
                ensure_ascii=False,
                indent=2,
            ),
        )

        # Final marker
        if self.report["complete"]:
            self._write(
                self.games_root /
                "GAMES_CORE_CLOSED.txt",
                (
                    "AJVYRA GAMES CORE CLOSED\n"
                    f"Version: {self.VERSION}\n"
                    f"Games: {self.EXPECTED_GAMES}\n"
                    "Runtime: COMPLETE\n"
                    "Assets: CONNECTED\n"
                    "Offline: ENABLED\n"
                    "PWA: ENABLED\n"
                    "Health: PASS\n"
                ),
            )

        return self.report


if __name__ == "__main__":
    system = AJVYRAGamesFinalClosure()

    result = system.run()

    print()
    print("=" * 60)
    print("AJVYRA GAMES FINAL CLOSURE")
    print("=" * 60)
    print(
        f"Games finalized: "
        f"{result['finalized_games']}/70"
    )
    print(
        f"Games failed: "
        f"{result['failed_games']}"
    )
    print(
        f"COMPLETE: "
        f"{result['complete']}"
    )
    print("=" * 60)
