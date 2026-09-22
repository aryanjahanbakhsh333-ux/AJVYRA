(function (global) {
    "use strict";

    class AJVYRAUniqueGameControls {
        constructor(profile, root) {
            this.profile = profile;
            this.root = root;

            this.buttons = new Map();
            this.listeners = new Map();

            this.create();
        }

        create() {
            if (!this.root) {
                return;
            }

            this.root.innerHTML = "";

            const controls =
                this.profile.controls || {};

            Object.entries(controls).forEach(
                ([action, label]) => {
                    const button =
                        document.createElement("button");

                    button.type = "button";

                    button.dataset.action =
                        action;

                    button.textContent =
                        label;

                    button.className =
                        "ajvyra-game-control";

                    button.style.minWidth =
                        "72px";

                    button.style.minHeight =
                        "52px";

                    button.style.padding =
                        "8px 12px";

                    button.style.borderRadius =
                        "14px";

                    button.style.border =
                        "1px solid rgba(255,255,255,.20)";

                    button.style.background =
                        "rgba(10,10,14,.78)";

                    button.style.color =
                        "#ffffff";

                    button.style.touchAction =
                        "none";

                    const down = (event) => {
                        event.preventDefault();

                        this.emit(
                            action,
                            true
                        );
                    };

                    const up = (event) => {
                        event.preventDefault();

                        this.emit(
                            action,
                            false
                        );
                    };

                    button.addEventListener(
                        "pointerdown",
                        down
                    );

                    button.addEventListener(
                        "pointerup",
                        up
                    );

                    button.addEventListener(
                        "pointercancel",
                        up
                    );

                    button.addEventListener(
                        "pointerleave",
                        up
                    );

                    this.root.appendChild(
                        button
                    );

                    this.buttons.set(
                        action,
                        button
                    );

                    this.listeners.set(
                        action,
                        {
                            down,
                            up
                        }
                    );
                }
            );
        }

        emit(action, pressed) {
            this.root.dispatchEvent(
                new CustomEvent(
                    "ajvyra:unique-control",
                    {
                        bubbles: true,
                        detail: {
                            action,
                            pressed,
                            game:
                                this.profile.title
                        }
                    }
                )
            );
        }

        setEnabled(action, enabled) {
            const button =
                this.buttons.get(action);

            if (button) {
                button.disabled =
                    !Boolean(enabled);
            }
        }

        destroy() {
            this.buttons.clear();
            this.listeners.clear();

            if (this.root) {
                this.root.innerHTML = "";
            }
        }
    }

    global.AJVYRAUniqueGameControls =
        AJVYRAUniqueGameControls;

})(window);
