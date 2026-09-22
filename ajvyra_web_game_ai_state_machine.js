"use strict";

class AJVYRAWebAIState {
    constructor(name, options = {}) {
        this.name = name;

        this.enter =
            typeof options.enter === "function"
                ? options.enter
                : () => {};

        this.update =
            typeof options.update === "function"
                ? options.update
                : () => {};

        this.exit =
            typeof options.exit === "function"
                ? options.exit
                : () => {};
    }
}


class AJVYRAWebAIStateMachine {
    constructor(owner) {
        this.owner = owner;

        this.states = new Map();

        this.currentState = null;

        this.currentStateName = null;
    }

    addState(state) {
        if (
            !(state instanceof AJVYRAWebAIState)
        ) {
            throw new TypeError(
                "Invalid AI state."
            );
        }

        this.states.set(
            state.name,
            state
        );

        return this;
    }

    hasState(name) {
        return this.states.has(name);
    }

    changeState(name, context = {}) {
        const next =
            this.states.get(name);

        if (!next) {
            throw new Error(
                `AI state not found: ${name}`
            );
        }

        if (
            this.currentStateName === name
        ) {
            return false;
        }

        if (this.currentState) {
            this.currentState.exit(
                this.owner,
                context
            );
        }

        this.currentState = next;
        this.currentStateName = name;

        this.currentState.enter(
            this.owner,
            context
        );

        return true;
    }

    update(delta, context = {}) {
        if (!this.currentState) {
            return;
        }

        this.currentState.update(
            this.owner,
            {
                ...context,
                delta,
                state: this.currentStateName
            }
        );
    }

    getState() {
        return this.currentStateName;
    }

    reset() {
        if (this.currentState) {
            this.currentState.exit(
                this.owner,
                {}
            );
        }

        this.currentState = null;
        this.currentStateName = null;
    }
}


window.AJVYRAWebAIState =
    AJVYRAWebAIState;

window.AJVYRAWebAIStateMachine =
    AJVYRAWebAIStateMachine;
