class AJVYRAWebProfessionalGameHost {

    constructor() {
        this.root = null;
        this.engine = null;
        this.input = null;
        this.hud = null;
        this.screen = null;

        this.enemyDirector = null;
        this.levelDirector = null;
    }

    mount(root) {
        if (!root) {
            throw new Error(
                "Professional game root is required."
            );
        }

        this.root = root;

        root.innerHTML = "";

        root.style.position =
            "relative";

        root.style.width =
            "100%";

        root.style.background =
            "#050505";

        const canvas =
            document.createElement("canvas");

        canvas.width = 1280;
        canvas.height = 720;

        canvas.style.width =
            "100%";

        canvas.style.display =
            "block";

        canvas.style.touchAction =
            "none";

        const hud =
            document.createElement("div");

        hud.style.position =
            "absolute";

        hud.style.inset = "0";

        const touch =
            document.createElement("div");

        touch.style.position =
            "absolute";

        touch.style.inset = "0";

        const screen =
            document.createElement("div");

        screen.style.position =
            "absolute";

        screen.style.inset = "0";

        root.append(
            canvas,
            hud,
            touch,
            screen
        );

        this.input =
            new AJVYRAWebGameInputBridge();

        this.input.attachTouchControls(
            touch
        );

        this.hud =
            new AJVYRAWebGameHUD();

        this.hud.mount(hud);

        this.screen =
            new AJVYRAWebGameStateScreen();

        this.screen.mount(screen);

        this.engine =
            new AJVYRAWebProfessionalGameEngine({
                canvas,
                input: this.input,
                hud: this.hud,
                screen: this.screen
            });

        this.enemyDirector =
            new AJVYRAWebGameEnemyDirector(
                this.engine
            );

        this.levelDirector =
            new AJVYRAWebGameLevelDirector(
                this.engine
            );

        this.screen.onRestart =
            () => this.restart();

        this.screen.onResume =
            () => this.engine.resume();

        this.screen.onExit =
            () => this.stop();

        return this;
    }

    load(game) {
        const scenario =
            AJVYRAWeb30GameScenarios.get(
                game.id
            );

        if (!scenario) {
            throw new Error(
                `No professional scenario for ${game.id}`
            );
        }

        const definition = {
            ...game,
            ...scenario
        };

        this.engine.load(
            definition
        );

        this.levelDirector.load();

        this.startDirectors();

        this.engine.start();

        return this.engine;
    }

    startDirectors() {
        if (this.directorLoop) {
            cancelAnimationFrame(
                this.directorLoop
            );
        }

        const tick = () => {
            if (
                !this.engine ||
                !this.engine.running
            ) {
                return;
            }

            if (
                !this.engine.paused &&
                this.engine.state.status ===
                "playing"
            ) {
                this.enemyDirector.update(
                    1 / 60
                );

                this.levelDirector.update();
            }

            this.directorLoop =
                requestAnimationFrame(tick);
        };

        this.directorLoop =
            requestAnimationFrame(tick);
    }

    restart() {
        if (!this.engine) {
            return;
        }

        const game =
            this.engine.definition;

        this.load(game);
    }

    stop() {
        this.engine?.stop();

        if (this.directorLoop) {
            cancelAnimationFrame(
                this.directorLoop
            );

            this.directorLoop = 0;
        }

        if (this.root) {
            this.root.innerHTML = "";
        }
    }
}

window.AJVYRAWebProfessionalGameHost =
    AJVYRAWebProfessionalGameHost;
