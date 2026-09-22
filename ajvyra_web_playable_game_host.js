class AJVYRAWebPlayableGameHost {
    constructor() {
        this.root = null;
        this.engine = null;
        this.input = null;
        this.hud = null;
        this.screen = null;
    }

    mount(root) {
        if (!root) {
            throw new Error(
                "AJVYRA game root is required."
            );
        }

        this.root = root;

        root.innerHTML = "";
        root.style.position = "relative";
        root.style.width = "100%";

        const canvas =
            document.createElement("canvas");

        canvas.width = 960;
        canvas.height = 540;

        canvas.style.width = "100%";
        canvas.style.display = "block";
        canvas.style.background = "#080808";

        const hudLayer =
            document.createElement("div");

        hudLayer.style.position = "absolute";
        hudLayer.style.inset = "0";

        const touchLayer =
            document.createElement("div");

        touchLayer.style.position = "absolute";
        touchLayer.style.inset = "0";

        const screenLayer =
            document.createElement("div");

        screenLayer.style.position = "absolute";
        screenLayer.style.inset = "0";

        root.append(
            canvas,
            hudLayer,
            touchLayer,
            screenLayer
        );

        this.input =
            new AJVYRAWebGameInputBridge();

        this.input.attachTouchControls(
            touchLayer
        );

        this.hud =
            new AJVYRAWebGameHUD();

        this.hud.mount(hudLayer);

        this.screen =
            new AJVYRAWebGameStateScreen();

        this.screen.mount(screenLayer);

        this.engine =
            new AJVYRAWebPlayableGameEngine({
                canvas,
                input: this.input,
                hud: this.hud,
                screen: this.screen
            });

        this.screen.onRestart =
            () => this.engine.restart();

        this.screen.onResume =
            () => this.engine.resume();

        this.screen.onExit =
            () => this.stop();

        return this;
    }

    load(game) {
        if (!this.engine) {
            throw new Error(
                "Game host has not been mounted."
            );
        }

        this.engine.load(game);
        this.engine.start();

        return this.engine;
    }

    stop() {
        this.engine?.stop();

        if (this.root) {
            this.root.innerHTML = "";
        }
    }
}

window.AJVYRAWebPlayableGameHost =
    AJVYRAWebPlayableGameHost;
