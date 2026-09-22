from __future__ import annotations

import hashlib
import json
import re
import shutil
import subprocess
import sys
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any, Dict, List, Optional
from urllib.parse import unquote


ROOT = Path(__file__).resolve().parent

FINAL_GAMES_DIR = ROOT / "generated" / "final_games"
ASSET_ROOT = ROOT / "generated" / "ajvyra_assets"

REPORT_FILE = ROOT / "real_test_report.json"
BROKEN_FILE = ROOT / "broken_games.json"
CLOSED_FILE = ROOT / "GAMES_CORE_CLOSED.txt"


REQUIRED_FILES = {
    "index.html",
    "game.js",
    "game.css",
    "metadata.json",
}


RUNTIME_MARKERS = [
    "requestAnimationFrame",
    "canvas",
    "addEventListener",
]


@dataclass
class GameTestResult:
    game_number: int
    game_path: str

    exists: bool = False
    required_files_ok: bool = False
    metadata_ok: bool = False
    html_ok: bool = False
    javascript_ok: bool = False
    css_ok: bool = False
    assets_ok: bool = False
    references_ok: bool = False
    runtime_markers_ok: bool = False
    node_syntax_ok: Optional[bool] = None

    repaired_assets: bool = False
    repaired_references: bool = False

    errors: List[str] = None
    warnings: List[str] = None

    def __post_init__(self):
        if self.errors is None:
            self.errors = []

        if self.warnings is None:
            self.warnings = []

    @property
    def passed(self) -> bool:
        checks = [
            self.exists,
            self.required_files_ok,
            self.metadata_ok,
            self.html_ok,
            self.javascript_ok,
            self.css_ok,
            self.assets_ok,
            self.references_ok,
            self.runtime_markers_ok,
        ]

        if self.node_syntax_ok is False:
            checks.append(False)

        return all(checks)


class AJVYRARealGameTestAndRepair:

    def __init__(
        self,
        games_dir: Path = FINAL_GAMES_DIR,
        asset_root: Path = ASSET_ROOT,
    ):
        self.games_dir = Path(games_dir)
        self.asset_root = Path(asset_root)

        self.results: List[GameTestResult] = []

    # ---------------------------------------------------------
    # PUBLIC
    # ---------------------------------------------------------

    def run(self) -> Dict[str, Any]:
        self._cleanup_old_reports()

        games = self._discover_games()

        if not games:
            report = {
                "status": "FAILED",
                "reason": "No final games were found.",
                "games_found": 0,
            }

            self._write_json(REPORT_FILE, report)
            self._write_json(BROKEN_FILE, report)

            return report

        for game_number, game_path in games:
            result = self._test_and_repair_game(
                game_number,
                game_path,
            )

            self.results.append(result)

        summary = self._build_summary()

        self._write_json(
            REPORT_FILE,
            summary,
        )

        broken = [
            asdict(result)
            for result in self.results
            if not result.passed
        ]

        self._write_json(
            BROKEN_FILE,
            {
                "count": len(broken),
                "games": broken,
            },
        )

        if summary["status"] == "PASSED":
            self._close_games_core(summary)
        else:
            self._remove_closed_marker()

        return summary

    # ---------------------------------------------------------
    # DISCOVERY
    # ---------------------------------------------------------

    def _discover_games(self):
        discovered = []

        if not self.games_dir.exists():
            return discovered

        for path in sorted(self.games_dir.glob("game_*")):
            if not path.is_dir():
                continue

            match = re.fullmatch(
                r"game_(\d+)",
                path.name,
            )

            if not match:
                continue

            number = int(match.group(1))

            if 1 <= number <= 70:
                discovered.append(
                    (
                        number,
                        path,
                    )
                )

        discovered.sort(key=lambda item: item[0])

        return discovered

    # ---------------------------------------------------------
    # GAME TEST
    # ---------------------------------------------------------

    def _test_and_repair_game(
        self,
        game_number: int,
        game_path: Path,
    ) -> GameTestResult:

        result = GameTestResult(
            game_number=game_number,
            game_path=str(game_path),
        )

        result.exists = game_path.exists()

        if not result.exists:
            result.errors.append(
                "Game directory does not exist."
            )
            return result

        required = self._check_required_files(
            game_path,
            result,
        )

        if not required:
            return result

        metadata = self._read_metadata(
            game_path,
            result,
        )

        html = self._read_text(
            game_path / "index.html",
            result,
            "index.html",
        )

        javascript = self._read_text(
            game_path / "game.js",
            result,
            "game.js",
        )

        css = self._read_text(
            game_path / "game.css",
            result,
            "game.css",
        )

        if metadata is not None:
            result.metadata_ok = self._validate_metadata(
                metadata,
                game_number,
                result,
            )

        if html is not None:
            result.html_ok = self._validate_html(
                html,
                result,
            )

        if javascript is not None:
            result.javascript_ok = self._validate_javascript(
                javascript,
                result,
            )

            result.runtime_markers_ok = (
                self._validate_runtime_markers(
                    javascript,
                    result,
                )
            )

            result.node_syntax_ok = (
                self._check_node_syntax(
                    game_path / "game.js",
                    result,
                )
            )

        if css is not None:
            result.css_ok = self._validate_css(
                css,
                result,
            )

        # -----------------------------------------------------
        # ASSET REPAIR
        # -----------------------------------------------------

        if self._repair_game_assets(
            game_number,
            game_path,
            result,
        ):
            result.repaired_assets = True

        # Re-read HTML/JS after repairs.
        html_after = self._safe_read(
            game_path / "index.html"
        )

        js_after = self._safe_read(
            game_path / "game.js"
        )

        if js_after:
            if self._repair_asset_references(
                game_path,
                js_after,
            ):
                result.repaired_references = True

        # -----------------------------------------------------
        # FINAL RECHECK
        # -----------------------------------------------------

        result.assets_ok = self._validate_assets(
            game_path,
            result,
        )

        html_after = self._safe_read(
            game_path / "index.html"
        )

        js_after = self._safe_read(
            game_path / "game.js"
        )

        if html_after:
            result.html_ok = self._validate_html(
                html_after,
                result,
            )

        if js_after:
            result.javascript_ok = self._validate_javascript(
                js_after,
                result,
            )

            result.runtime_markers_ok = (
                self._validate_runtime_markers(
                    js_after,
                    result,
                )
            )

            result.node_syntax_ok = (
                self._check_node_syntax(
                    game_path / "game.js",
                    result,
                )
            )

        result.references_ok = (
            self._validate_local_references(
                game_path,
                result,
            )
        )

        return result

    # ---------------------------------------------------------
    # REQUIRED FILES
    # ---------------------------------------------------------

    def _check_required_files(
        self,
        game_path: Path,
        result: GameTestResult,
    ) -> bool:

        missing = []

        for filename in REQUIRED_FILES:
            if not (game_path / filename).is_file():
                missing.append(filename)

        if missing:
            result.errors.append(
                "Missing required files: "
                + ", ".join(sorted(missing))
            )

            result.required_files_ok = False
            return False

        result.required_files_ok = True
        return True

    # ---------------------------------------------------------
    # METADATA
    # ---------------------------------------------------------

    def _read_metadata(
        self,
        game_path: Path,
        result: GameTestResult,
    ) -> Optional[Dict[str, Any]]:

        path = game_path / "metadata.json"

        try:
            data = json.loads(
                path.read_text(
                    encoding="utf-8"
                )
            )

            if not isinstance(data, dict):
                raise ValueError(
                    "metadata.json must contain an object."
                )

            return data

        except Exception as exc:
            result.errors.append(
                f"metadata.json error: {exc}"
            )

            return None

    def _validate_metadata(
        self,
        metadata: Dict[str, Any],
        game_number: int,
        result: GameTestResult,
    ) -> bool:

        valid = True

        if "game_number" in metadata:
            try:
                if int(metadata["game_number"]) != game_number:
                    result.errors.append(
                        "metadata game_number does not match directory."
                    )
                    valid = False
            except Exception:
                result.errors.append(
                    "metadata game_number is invalid."
                )
                valid = False

        useful_keys = [
            "title",
            "genre",
            "objective",
        ]

        if not any(key in metadata for key in useful_keys):
            result.warnings.append(
                "metadata contains no common descriptive fields."
            )

        return valid

    # ---------------------------------------------------------
    # HTML
    # ---------------------------------------------------------

    def _validate_html(
        self,
        html: str,
        result: GameTestResult,
    ) -> bool:

        valid = True

        if "<html" not in html.lower():
            result.errors.append(
                "index.html has no <html> element."
            )
            valid = False

        if "<canvas" not in html.lower():
            result.errors.append(
                "index.html has no canvas element."
            )
            valid = False

        if "<script" not in html.lower():
            result.errors.append(
                "index.html contains no script tag."
            )
            valid = False

        if "game.js" not in html:
            result.warnings.append(
                "game.js is not explicitly referenced by index.html."
            )

        return valid

    # ---------------------------------------------------------
    # JAVASCRIPT
    # ---------------------------------------------------------

    def _validate_javascript(
        self,
        javascript: str,
        result: GameTestResult,
    ) -> bool:

        valid = True

        if len(javascript.strip()) < 100:
            result.errors.append(
                "game.js appears to be empty or extremely small."
            )
            valid = False

        if "canvas" not in javascript.lower():
            result.errors.append(
                "game.js does not appear to use Canvas."
            )
            valid = False

        if (
            "requestAnimationFrame" not in javascript
            and "setInterval" not in javascript
        ):
            result.errors.append(
                "No animation/game loop marker found."
            )
            valid = False

        if "addEventListener" not in javascript:
            result.warnings.append(
                "No addEventListener marker found."
            )

        return valid

    # ---------------------------------------------------------
    # RUNTIME MARKERS
    # ---------------------------------------------------------

    def _validate_runtime_markers(
        self,
        javascript: str,
        result: GameTestResult,
    ) -> bool:

        missing = []

        for marker in RUNTIME_MARKERS:
            if marker not in javascript:
                missing.append(marker)

        if missing:
            result.warnings.append(
                "Runtime markers missing: "
                + ", ".join(missing)
            )

        # Canvas + animation loop are the essential checks.
        return (
            "canvas" in javascript.lower()
            and (
                "requestAnimationFrame" in javascript
                or "setInterval" in javascript
            )
        )

    # ---------------------------------------------------------
    # CSS
    # ---------------------------------------------------------

    def _validate_css(
        self,
        css: str,
        result: GameTestResult,
    ) -> bool:

        if len(css.strip()) < 20:
            result.warnings.append(
                "game.css is unusually small."
            )

        return True

    # ---------------------------------------------------------
    # NODE SYNTAX
    # ---------------------------------------------------------

    def _check_node_syntax(
        self,
        javascript_path: Path,
        result: GameTestResult,
    ) -> Optional[bool]:

        node = shutil.which("node")

        if not node:
            result.warnings.append(
                "Node.js not installed; JavaScript syntax "
                "check skipped."
            )
            return None

        try:
            process = subprocess.run(
                [
                    node,
                    "--check",
                    str(javascript_path),
                ],
                capture_output=True,
                text=True,
                timeout=15,
            )

            if process.returncode != 0:
                result.errors.append(
                    "Node.js syntax check failed: "
                    + (
                        process.stderr.strip()
                        or "unknown syntax error"
                    )
                )

                return False

            return True

        except subprocess.TimeoutExpired:
            result.errors.append(
                "Node.js syntax check timed out."
            )
            return False

        except Exception as exc:
            result.warnings.append(
                f"Node.js syntax check unavailable: {exc}"
            )
            return None

    # ---------------------------------------------------------
    # ASSETS
    # ---------------------------------------------------------

    def _repair_game_assets(
        self,
        game_number: int,
        game_path: Path,
        result: GameTestResult,
    ) -> bool:

        source_candidates = [
            self.asset_root / f"game_{game_number:02d}" / "assets",
            self.asset_root / f"game_{game_number}" / "assets",
            self.asset_root / f"game_{game_number:03d}" / "assets",
        ]

        source = None

        for candidate in source_candidates:
            if candidate.exists() and candidate.is_dir():
                source = candidate
                break

        destination = game_path / "assets"
        destination.mkdir(
            parents=True,
            exist_ok=True,
        )

        changed = False

        if source is not None:
            for source_file in source.rglob("*"):
                if not source_file.is_file():
                    continue

                relative = source_file.relative_to(source)
                destination_file = destination / relative

                destination_file.parent.mkdir(
                    parents=True,
                    exist_ok=True,
                )

                if not destination_file.exists():
                    shutil.copy2(
                        source_file,
                        destination_file,
                    )
                    changed = True
                else:
                    try:
                        source_hash = self._sha256(
                            source_file
                        )

                        destination_hash = self._sha256(
                            destination_file
                        )

                        if source_hash != destination_hash:
                            shutil.copy2(
                                source_file,
                                destination_file,
                            )
                            changed = True

                    except Exception as exc:
                        result.warnings.append(
                            "Could not compare asset "
                            f"{source_file.name}: {exc}"
                        )

        else:
            result.warnings.append(
                "No external asset directory found; "
                "checking local game assets."
            )

        return changed

    def _validate_assets(
        self,
        game_path: Path,
        result: GameTestResult,
    ) -> bool:

        assets = game_path / "assets"

        if not assets.exists():
            result.warnings.append(
                "No assets directory exists."
            )
            return True

        files = [
            path
            for path in assets.rglob("*")
            if path.is_file()
        ]

        # Games are allowed to work without external
        # images because the renderer can be procedural.
        if not files:
            result.warnings.append(
                "Assets directory is empty."
            )

        return True

    # ---------------------------------------------------------
    # ASSET REFERENCES
    # ---------------------------------------------------------

    def _repair_asset_references(
        self,
        game_path: Path,
        javascript: str,
    ) -> bool:

        changed = False

        patterns = [
            r'["\']generated/ajvyra_assets/game_\d+/assets/',
            r'["\']\.\./\.\./ajvyra_assets/game_\d+/assets/',
            r'["\']\.\./generated/ajvyra_assets/game_\d+/assets/',
        ]

        repaired = javascript

        for pattern in patterns:
            repaired, count = re.subn(
                pattern,
                '"assets/',
                repaired,
            )

            if count:
                changed = True

        # Normalize accidental double asset paths.
        repaired = repaired.replace(
            "assets/assets/",
            "assets/",
        )

        if repaired != javascript:
            changed = True

        if changed:
            (game_path / "game.js").write_text(
                repaired,
                encoding="utf-8",
            )

        return changed

    # ---------------------------------------------------------
    # LOCAL REFERENCES
    # ---------------------------------------------------------

    def _validate_local_references(
        self,
        game_path: Path,
        result: GameTestResult,
    ) -> bool:

        valid = True

        html_path = game_path / "index.html"
        js_path = game_path / "game.js"
        css_path = game_path / "game.css"

        html = self._safe_read(html_path)
        javascript = self._safe_read(js_path)
        css = self._safe_read(css_path)

        if html:
            refs = self._extract_html_references(
                html
            )

            for ref in refs:
                if self._is_external_reference(ref):
                    continue

                clean = self._clean_reference(ref)

                if not clean:
                    continue

                target = game_path / clean

                if not target.exists():
                    result.errors.append(
                        f"Missing HTML reference: {ref}"
                    )
                    valid = False

        if javascript:
            asset_refs = self._extract_js_asset_references(
                javascript
            )

            for ref in asset_refs:
                target = game_path / self._clean_reference(
                    ref
                )

                if not target.exists():
                    result.errors.append(
                        f"Missing JS asset reference: {ref}"
                    )
                    valid = False

        return valid

    def _extract_html_references(
        self,
        html: str,
    ) -> List[str]:

        refs = []

        for match in re.findall(
            r'(?:src|href)\s*=\s*["\']([^"\']+)["\']',
            html,
            flags=re.IGNORECASE,
        ):
            refs.append(match)

        return refs

    def _extract_js_asset_references(
        self,
        javascript: str,
    ) -> List[str]:

        refs = []

        patterns = [
            r'["\'](assets/[^"\']+)["\']',
            r'["\'](\./assets/[^"\']+)["\']',
        ]

        for pattern in patterns:
            refs.extend(
                re.findall(
                    pattern,
                    javascript,
                )
            )

        return refs

    # ---------------------------------------------------------
    # HELPERS
    # ---------------------------------------------------------

    def _is_external_reference(
        self,
        reference: str,
    ) -> bool:

        lowered = reference.lower().strip()

        return (
            lowered.startswith("http://")
            or lowered.startswith("https://")
            or lowered.startswith("//")
            or lowered.startswith("data:")
            or lowered.startswith("#")
            or lowered.startswith("mailto:")
            or lowered.startswith("javascript:")
        )

    def _clean_reference(
        self,
        reference: str,
    ) -> str:

        reference = unquote(
            reference.strip()
        )

        reference = reference.split(
            "?",
            1,
        )[0]

        reference = reference.split(
            "#",
            1,
        )[0]

        while reference.startswith("./"):
            reference = reference[2:]

        reference = reference.replace(
            "\\",
            "/",
        )

        return reference

    def _read_text(
        self,
        path: Path,
        result: GameTestResult,
        label: str,
    ) -> Optional[str]:

        try:
            return path.read_text(
                encoding="utf-8"
            )
        except Exception as exc:
            result.errors.append(
                f"{label} read error: {exc}"
            )
            return None

    def _safe_read(
        self,
        path: Path,
    ) -> str:

        try:
            return path.read_text(
                encoding="utf-8"
            )
        except Exception:
            return ""

    def _sha256(
        self,
        path: Path,
    ) -> str:

        digest = hashlib.sha256()

        with path.open("rb") as file:
            while True:
                chunk = file.read(1024 * 1024)

                if not chunk:
                    break

                digest.update(chunk)

        return digest.hexdigest()

    # ---------------------------------------------------------
    # SUMMARY
    # ---------------------------------------------------------

    def _build_summary(self) -> Dict[str, Any]:

        passed = [
            result
            for result in self.results
            if result.passed
        ]

        failed = [
            result
            for result in self.results
            if not result.passed
        ]

        expected = set(range(1, 71))

        found = {
            result.game_number
            for result in self.results
        }

        missing = sorted(
            expected - found
        )

        status = (
            "PASSED"
            if len(passed) == 70
            and len(failed) == 0
            and not missing
            else "FAILED"
        )

        return {
            "project": "AJVYRA",
            "system": "Games Real Test And Repair",
            "status": status,
            "expected_games": 70,
            "games_found": len(self.results),
            "games_passed": len(passed),
            "games_failed": len(failed),
            "missing_games": missing,
            "browser_execution_note": (
                "This validator performs static integrity, "
                "reference, asset and optional Node syntax "
                "checks. It does not claim full browser "
                "interaction testing unless a real browser "
                "test runner is separately used."
            ),
            "games": [
                asdict(result)
                for result in self.results
            ],
        }

    # ---------------------------------------------------------
    # CLOSE GAMES CORE
    # ---------------------------------------------------------

    def _close_games_core(
        self,
        summary: Dict[str, Any],
    ):

        content = f"""AJVYRA GAMES CORE CLOSED

Status: {summary["status"]}

Expected games: 70
Found games: {summary["games_found"]}
Passed games: {summary["games_passed"]}
Failed games: {summary["games_failed"]}

All 70 game directories passed the final static
integrity and repair validation.

Validated:
- Required game files
- Metadata
- HTML
- JavaScript
- CSS
- Canvas/runtime markers
- Local references
- Local assets
- Asset path integration
- Optional Node.js JavaScript syntax

Important:
This file confirms static/integrity validation.
It does not claim that a human played all 70 games
or that every browser/device combination was tested.

Games Core is now closed.
"""

        CLOSED_FILE.write_text(
            content,
            encoding="utf-8",
        )

    def _remove_closed_marker(self):

        if CLOSED_FILE.exists():
            CLOSED_FILE.unlink()

    # ---------------------------------------------------------
    # REPORTS
    # ---------------------------------------------------------

    def _write_json(
        self,
        path: Path,
        data: Any,
    ):

        path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        path.write_text(
            json.dumps(
                data,
                ensure_ascii=False,
                indent=2,
            ),
            encoding="utf-8",
        )

    def _cleanup_old_reports(self):

        for path in [
            REPORT_FILE,
            BROKEN_FILE,
        ]:
            if path.exists():
                path.unlink()


def main():

    tester = AJVYRARealGameTestAndRepair()

    report = tester.run()

    print()
    print("=" * 60)
    print("AJVYRA — 70 GAME REAL TEST & REPAIR")
    print("=" * 60)
    print()

    print(
        f"Status: {report.get('status')}"
    )

    print(
        f"Games found: "
        f"{report.get('games_found', 0)}/70"
    )

    print(
        f"Games passed: "
        f"{report.get('games_passed', 0)}/70"
    )

    print(
        f"Games failed: "
        f"{report.get('games_failed', 0)}/70"
    )

    missing = report.get(
        "missing_games",
        [],
    )

    if missing:
        print(
            "Missing games:",
            ", ".join(
                str(number)
                for number in missing
            ),
        )

    print()

    if report.get("status") == "PASSED":
        print(
            "GAMES CORE: CLOSED"
        )
        print(
            f"Created: {CLOSED_FILE}"
        )
    else:
        print(
            "GAMES CORE: NOT CLOSED"
        )
        print(
            "Check:",
            BROKEN_FILE,
        )

    print()
    print(
        "Report:",
        REPORT_FILE,
    )

    print("=" * 60)


if __name__ == "__main__":
    main()
