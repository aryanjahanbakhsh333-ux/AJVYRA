class AJVYRAWebGameHUD {
    constructor(options = {}) {
        this.container =
            options.container || null;

        this.state = {
            health: 100,
            maxHealth: 100,
            mana: 100,
            maxMana: 100,
            stamina: 100,
            maxStamina: 100,
            score: 0,
            level: 1,
            lives: null,
            time: null
        };
    }

    mount(container) {
        this.container = container;

        this.render();
    }

    update(state = {}) {
        this.state = {
            ...this.state,
            ...state
        };

        this.render();
    }

    render() {
        if (!this.container) {
            return;
        }

        this.container.innerHTML = "";

        const root =
            document.createElement("div");

        root.className =
            "ajvyra-game-hud";

        const health =
            this.createBar(
                "HP",
                this.state.health,
                this.state.maxHealth
            );

        root.appendChild(health);

        if (
            this.state.maxMana > 0
        ) {
            root.appendChild(
                this.createBar(
                    "MP",
                    this.state.mana,
                    this.state.maxMana
                )
            );
        }

        if (
            this.state.maxStamina > 0
        ) {
            root.appendChild(
                this.createBar(
                    "ST",
                    this.state.stamina,
                    this.state.maxStamina
                )
            );
        }

        const info =
            document.createElement("div");

        info.className =
            "ajvyra-game-hud-info";

        info.textContent =
            `LV ${this.state.level}  |  SCORE ${this.state.score}`;

        if (this.state.lives !== null) {
            info.textContent +=
                `  |  LIVES ${this.state.lives}`;
        }

        if (this.state.time !== null) {
            info.textContent +=
                `  |  TIME ${Math.ceil(this.state.time)}`;
        }

        root.appendChild(info);

        this.container.appendChild(root);
    }

    createBar(label, value, max) {
        const wrapper =
            document.createElement("div");

        const title =
            document.createElement("span");

        title.textContent = label;

        const track =
            document.createElement("div");

        const fill =
            document.createElement("div");

        const safeMax =
            Math.max(1, Number(max) || 1);

        const percentage =
            Math.max(
                0,
                Math.min(
                    100,
                    ((Number(value) || 0) /
                        safeMax) * 100
                )
            );

        fill.style.width =
            `${percentage}%`;

        track.appendChild(fill);

        wrapper.append(
            title,
            track
        );

        return wrapper;
    }
}

if (typeof window !== "undefined") {
    window.AJVYRAWebGameHUD =
        AJVYRAWebGameHUD;
}
