(function (global) {
    "use strict";

    class AJVYRAStoryChoiceRuntime {
        constructor(runtime, story = {}) {
            this.runtime = runtime;

            this.story = story;

            this.chapter = 0;
            this.choiceIndex = 0;

            this.flags = {};
            this.history = [];

            this.active = false;
            this.finished = false;

            this.currentNode = null;
        }

        start() {
            this.chapter = 0;
            this.choiceIndex = 0;
            this.flags = {};
            this.history = [];

            this.active = true;
            this.finished = false;

            this.loadChapter(0);

            return this.currentNode;
        }

        loadChapter(index) {
            const chapters =
                this.story.chapters || [];

            if (
                index < 0 ||
                index >= chapters.length
            ) {
                this.finish();
                return;
            }

            this.chapter = index;
            this.choiceIndex = 0;

            this.currentNode =
                chapters[index];

            return this.currentNode;
        }

        choose(index) {
            if (
                !this.active ||
                this.finished ||
                !this.currentNode
            ) {
                return false;
            }

            const choices =
                this.currentNode.choices || [];

            const choice =
                choices[index];

            if (!choice) {
                return false;
            }

            if (
                choice.requiredFlag &&
                !this.flags[
                    choice.requiredFlag
                ]
            ) {
                return false;
            }

            this.history.push({
                chapter: this.chapter,
                choice: index,
                id: choice.id || null
            });

            if (choice.setFlag) {
                this.flags[
                    choice.setFlag
                ] = true;
            }

            if (choice.clearFlag) {
                delete this.flags[
                    choice.clearFlag
                ];
            }

            if (
                typeof choice.score === "number"
            ) {
                this.addScore(choice.score);
            }

            if (
                choice.nextChapter !== undefined
            ) {
                this.loadChapter(
                    choice.nextChapter
                );
            } else {
                this.advance();
            }

            return true;
        }

        advance() {
            const next =
                this.chapter + 1;

            if (
                next >=
                (this.story.chapters || []).length
            ) {
                this.finish();
                return;
            }

            this.loadChapter(next);
        }

        addScore(value) {
            const core =
                this.runtime &&
                this.runtime.core;

            if (!core) {
                return;
            }

            if (
                typeof core.addScore ===
                "function"
            ) {
                core.addScore(value);
            } else {
                core.score =
                    (core.score || 0) +
                    value;
            }
        }

        finish() {
            this.active = false;
            this.finished = true;

            const core =
                this.runtime &&
                this.runtime.core;

            if (core) {
                core.storyFinished = true;
            }
        }

        getCurrentDialogue() {
            if (!this.currentNode) {
                return null;
            }

            return {
                speaker:
                    this.currentNode.speaker ||
                    "",
                text:
                    this.currentNode.text ||
                    "",
                choices:
                    this.currentNode.choices ||
                    []
            };
        }

        getState() {
            return {
                chapter: this.chapter,
                active: this.active,
                finished: this.finished,
                flags: {
                    ...this.flags
                },
                history: [
                    ...this.history
                ],
                current:
                    this.getCurrentDialogue()
            };
        }
    }

    global.AJVYRAStoryChoiceRuntime =
        AJVYRAStoryChoiceRuntime;

})(window);
