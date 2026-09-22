class AJVYRAWebGameStateScreen {
    constructor(options = {}) {
        this.container =
            options.container || null;

        this.onResume =
            options.onResume || (() => {});

        this.onRestart =
            options.onRestart || (() => {});

        this.onExit =
            options.onExit || (() => {});

        this.current = null;
    }

    mount(container) {
        this.container = container;

        this.hide();
    }

    show(type, data = {}) {
        if (!this.container) {
            return;
        }

        this.current = type;

        this.container.innerHTML = "";

        const panel =
            document.createElement("div");

        panel.className =
            "ajvyra-game-state-screen";

        const title =
            document.createElement("h2");

        const message =
            document.createElement("p");

        if (type === "pause") {
            title.textContent = "PAUSED";
            message.textContent =
                "Game paused.";
        }

        if (type === "victory") {
            title.textContent = "VICTORY";
            message.textContent =
                "Mission complete.";
        }

        if (type === "defeat") {
            title.textContent = "GAME OVER";
            message.textContent =
                "Try again.";
        }

        if (type === "loading") {
            title.textContent = "LOADING";
            message.textContent =
                "Preparing game...";
        }

        panel.append(
            title,
            message
        );

        if (
            type === "pause" ||
            type === "victory" ||
            type === "defeat"
        ) {
            const restart =
                this.createButton(
                    "RESTART",
                    () => this.onRestart()
                );

            panel.appendChild(restart);
        }

        if (type === "pause") {
            const resume =
                this.createButton(
                    "RESUME",
                    () => {
                        this.hide();
                        this.onResume();
                    }
                );

            panel.appendChild(resume);
        }

        if (
            type === "victory" ||
            type === "defeat"
        ) {
            const exit =
                this.createButton(
                    "EXIT",
                    () => this.onExit()
                );

            panel.appendChild(exit);
        }

        this.container.appendChild(panel);
        this.container.style.display =
            "flex";
    }

    createButton(label, callback) {
        const button =
            document.createElement("button");

        button.type = "button";
        button.textContent = label;

        button.addEventListener(
            "click",
            callback
        );

        return button;
    }

    hide() {
        if (this.container) {
            this.container.innerHTML = "";
            this.container.style.display =
                "none";
        }

        this.current = null;
    }
}

if (typeof window !== "undefined") {
    window.AJVYRAWebGameStateScreen =
        AJVYRAWebGameStateScreen;
}
