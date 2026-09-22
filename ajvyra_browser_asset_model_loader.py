from pathlib import Path
import json


class AJVYRAAssetBrowserLoader:

    def __init__(self):
        pass

    def build_loader_js(
        self,
        game_id,
        asset_manifest,
    ):
        assets = {}

        for item in asset_manifest["generated_assets"]:
            assets[item["type"]] = item["path"]

        payload = json.dumps(
            assets,
            ensure_ascii=False,
        )

        return f"""
window.AJVYRA_ASSETS = {payload};

window.AJVYRAAssetLoader = {{
    cache: {{}},

    async load(name) {{
        const path = window.AJVYRA_ASSETS[name];

        if (!path) {{
            return null;
        }}

        if (this.cache[name]) {{
            return this.cache[name];
        }}

        const image = new Image();

        image.src = path;

        await new Promise((resolve, reject) => {{
            image.onload = resolve;
            image.onerror = reject;
        }});

        this.cache[name] = image;

        return image;
    }},

    async preload() {{
        const names =
            Object.keys(window.AJVYRA_ASSETS);

        await Promise.all(
            names.map(name => this.load(name))
        );

        return this.cache;
    }},

    draw(
        ctx,
        name,
        x,
        y,
        width,
        height
    ) {{
        const image = this.cache[name];

        if (!image) {{
            return false;
        }}

        ctx.drawImage(
            image,
            x,
            y,
            width,
            height
        );

        return true;
    }}
}};
"""

    def inject_into_game(
        self,
        game_directory,
        game_id,
        asset_manifest,
    ):
        root = Path(game_directory)

        game_js = root / "game.js"

        if not game_js.exists():
            raise FileNotFoundError(
                f"Missing game.js: {game_js}"
            )

        original = game_js.read_text(
            encoding="utf-8"
        )

        loader = self.build_loader_js(
            game_id,
            asset_manifest,
        )

        bootstrap = """
(async () => {
    try {
        await window.AJVYRAAssetLoader.preload();
        window.AJVYRA_ASSETS_READY = true;
    } catch (error) {
        console.warn(
            "AJVYRA asset preload failed",
            error
        );
    }
})();
"""

        marker = (
            "/* AJVYRA_ASSET_RUNTIME */"
        )

        if marker not in original:
            original = (
                marker +
                "\n" +
                loader +
                "\n" +
                bootstrap +
                "\n" +
                original
            )

        game_js.write_text(
            original,
            encoding="utf-8",
        )

        return game_js
