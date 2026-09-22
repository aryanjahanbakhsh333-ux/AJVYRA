/* AJVYRA — Story & Choice Runtime
 * New file.
 */

class AJVYRAStoryChoiceRuntime {

    constructor(story) {
        if (!story || !Array.isArray(story.chapters) || story.chapters.length === 0) {
            throw new Error("Invalid AJVYRA story.");
        }

        this.story = story;
        this.chapters = story.chapters;

        this.currentIndex = 0;
        this.currentChapter = this.chapters[0];

        this.choiceHistory = [];
        this.dialogueIndex = 0;

        this.active = false;
        this.finished = false;

        this.ending = null;

        this.listeners = new Map();
    }

    on(event, callback) {
        if (!this.listeners.has(event)) {
            this.listeners.set(event, []);
        }

        this.listeners.get(event).push(callback);
        return this;
    }

    emit(event, payload = {}) {
        const listeners = this.listeners.get(event) || [];

        for (const callback of listeners) {
            try {
                callback(payload);
            } catch (error) {
                console.error("[AJVYRA Story]", error);
            }
        }
    }

    start() {
        this.active = true;
        this.finished = false;
        this.currentIndex = 0;
        this.choiceHistory = [];
        this.dialogueIndex = 0;
        this.ending = null;

        this.currentChapter = this.chapters[0];

        this.emit("story-started", {
            chapter: this.currentChapter
        });

        return this.getState();
    }

    getDialogue() {
        return this.currentChapter.dialogue || [];
    }

    getCurrentDialogue() {
        const dialogue = this.getDialogue();

        if (!dialogue.length) {
            return null;
        }

        return dialogue[this.dialogueIndex] || null;
    }

    advanceDialogue() {
        if (!this.active || this.finished) {
            return false;
        }

        const dialogue = this.getDialogue();

        if (!dialogue.length) {
            return true;
        }

        if (this.dialogueIndex < dialogue.length - 1) {
            this.dialogueIndex++;

            this.emit("dialogue-advanced", {
                dialogue: this.getCurrentDialogue()
            });

            return true;
        }

        this.emit("dialogue-finished", {
            chapter: this.currentChapter
        });

        return true;
    }

    getChoices() {
        return this.currentChapter.choices || [];
    }

    choose(choiceId) {
        if (!this.active || this.finished) {
            return false;
        }

        const choice = this.getChoices().find(
            item => item.id === choiceId
        );

        if (!choice) {
            return false;
        }

        this.choiceHistory.push({
            chapter: this.currentChapter.id,
            choice: choice.id,
            text: choice.text
        });

        this.emit("choice-made", {
            chapter: this.currentChapter,
            choice
        });

        if (!choice.next) {
            this.finish("choice");
            return true;
        }

        const nextIndex = this.chapters.findIndex(
            chapter => chapter.id === choice.next
        );

        if (nextIndex === -1) {
            this.finish("missing-next");
            return false;
        }

        this.currentIndex = nextIndex;
        this.currentChapter = this.chapters[nextIndex];
        this.dialogueIndex = 0;

        if (
            this.currentIndex === this.chapters.length - 1 &&
            this.getChoices().length === 0
        ) {
            this.ending = this.currentChapter;
        }

        this.emit("chapter-changed", {
            chapter: this.currentChapter
        });

        return true;
    }

    completeCurrentChapter() {
        if (!this.active || this.finished) {
            return false;
        }

        const choices = this.getChoices();

        if (choices.length > 0) {
            return false;
        }

        if (this.currentIndex >= this.chapters.length - 1) {
            this.finish("story-complete");
            return true;
        }

        this.currentIndex++;
        this.currentChapter = this.chapters[this.currentIndex];
        this.dialogueIndex = 0;

        this.emit("chapter-changed", {
            chapter: this.currentChapter
        });

        return true;
    }

    finish(reason = "complete") {
        this.active = false;
        this.finished = true;

        this.ending = this.currentChapter;

        this.emit("story-finished", {
            reason,
            ending: this.ending,
            choices: this.choiceHistory
        });

        return this.getState();
    }

    getState() {
        return {
            active: this.active,
            finished: this.finished,
            currentIndex: this.currentIndex,
            currentChapter: this.currentChapter,
            dialogue: this.getCurrentDialogue(),
            choices: this.getChoices(),
            choiceHistory: [...this.choiceHistory],
            ending: this.ending
        };
    }
}

globalThis.AJVYRAStoryChoiceRuntime = AJVYRAStoryChoiceRuntime;
