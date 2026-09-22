class AJVYRAWebTouchControls {
    constructor(options = {}) {
        this.input =
            options.input || null;

        this.container =
            options.container || null;

        this.visible =
            options.visible !== false;

        this.buttons = new Map();

        this.layout = {
            left: {
                x: 70,
                y: 70
            },
            right: {
                x: 170,
                y: 70
            },
            jump: {
                x: 75,
                y: 35
            },
            attack: {
                x: 85,
                y: 55
            },
            special: {
                x: 95,
                y: 35
            }
        };
    }

    mount(container) {
        if (!container) {
            throw new Error(
                "Touch controls container is required."
            );
        }

        this.container = container;

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
            "ajvyra-touch-controls";

        root.style.position = "absolute";
        root.style.inset = "0";
        root.style.pointerEvents = "none";
        root.style.touchAction = "none";

        for (
            const [action, position]
            of Object.entries(this.layout)
        ) {
            const button =
                document.createElement("button");

            button.type = "button";

            button.textContent =
                this.getLabel(action);

            button.dataset.action = action;

            button.style.position = "absolute";
            button.style.left =
                `${position.x}%`;
            button.style.bottom =
                `${position.y}%`;
            button.style.width = "64px";
            button.style.height = "64px";
            button.style.borderRadius = "50%";
            button.style.pointerEvents = "auto";
            button.style.touchAction = "none";

            this.bindButton(
                button,
                action
            );

            this.buttons.set(
                action,
                button
            );

            root.appendChild(button);
        }

        this.container.appendChild(root);

        if (!this.visible) {
            this.hide();
        }
    }

    bindButton(button, action) {
        const start = event => {
            event.preventDefault();

            if (this.input) {
                this.input.setTouchAction(
                    action,
                    true
                );
            }

            button.dataset.pressed = "true";
        };

        const end = event => {
            event.preventDefault();

            if (this.input) {
                this.input.setTouchAction(
                    action,
                    false
                );
            }

            delete button.dataset.pressed;
        };

        button.addEventListener(
            "pointerdown",
            start
        );

        button.addEventListener(
            "pointerup",
            end
        );

        button.addEventListener(
            "pointercancel",
            end
        );

        button.addEventListener(
            "pointerleave",
            end
        );
    }

    getLabel(action) {
        const labels = {
            left: "←",
            right: "→",
            jump: "JUMP",
            attack: "ATK",
            special: "SP"
        };

        return labels[action] || action;
    }

    show() {
        this.visible = true;

        if (this.container) {
            this.container.style.display =
                "block";
        }
    }

    hide() {
        this.visible = false;

        if (this.container) {
            this.container.style.display =
                "none";
        }
    }
}

if (typeof window !== "undefined") {
    window.AJVYRAWebTouchControls =
        AJVYRAWebTouchControls;
}
