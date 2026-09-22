(function (global) {
    "use strict";

    class AJVYRAWebGameStoryRuntime {
        constructor(profile, container) {
            this.profile = profile;
            this.container = container;

            this.completedObjectives = 0;
            this.totalObjectives = 1;

            this.storyStarted = false;

            this.render();
        }

        render() {
            if (!this.container) {
                return;
            }

            this.container.innerHTML = "";

            const panel =
                document.createElement("div");

            panel.className =
                "ajvyra-story-panel";

            panel.style.padding =
                "18px";

            panel.style.color =
                "#ffffff";

            panel.style.background =
                "rgba(5,5,8,.90)";

            panel.style.border =
                "1px solid rgba(255,255,255,.10)";

            const title =
                document.createElement("h2");

            title.textContent =
                this.profile.title;

            title.style.margin =
                "0 0 8px";

            const story =
                document.createElement("p");

            story.textContent =
                this.profile.story;

            story.style.opacity =
                ".72";

            story.style.lineHeight =
                "1.6";

            const objective =
                document.createElement("p");

            objective.innerHTML =
                `<strong>Objective:</strong> ${
                    this.profile.objective
                }`;

            objective.style.lineHeight =
                "1.5";

            panel.appendChild(title);
            panel.appendChild(story);
            panel.appendChild(objective);

            this.container.appendChild(
                panel
            );
        }

        start() {
            this.storyStarted = true;

            this.container.dispatchEvent(
                new CustomEvent(
                    "ajvyra:story-started",
                    {
                        bubbles: true,
                        detail: {
                            title:
                                this.profile.title
                        }
                    }
                )
            );
        }

        completeObjective() {
            this.completedObjectives =
                Math.min(
                    this.totalObjectives,
                    this.completedObjectives + 1
                );

            if (
                this.completedObjectives >=
                this.totalObjectives
            ) {
                this.container.dispatchEvent(
                    new CustomEvent(
                        "ajvyra:story-complete",
                        {
                            bubbles: true,
                            detail: {
                                title:
                                    this.profile.title
                            }
                        }
                    )
                );
            }
        }
    }

    global.AJVYRAWebGameStoryRuntime =
        AJVYRAWebGameStoryRuntime;

})(window);
