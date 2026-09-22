(function (global) {
  "use strict";

  const ACTIONS = {
    "shadow-runner": {
      primary: "dash",
      secondary: "attack",
      utility: "interact"
    },

    "neon-drift": {
      primary: "boost",
      secondary: "drift",
      utility: "checkpoint"
    },

    "void-arena": {
      primary: "attack",
      secondary: "combo",
      utility: "dodge"
    },

    "lost-realm": {
      primary: "attack",
      secondary: "interact",
      utility: "quest"
    },

    "night-hunt": {
      primary: "attack",
      secondary: "heal",
      utility: "survive"
    },

    "cyber-strike": {
      primary: "shoot",
      secondary: "reload",
      utility: "interact"
    },

    "frostbound": {
      primary: "attack",
      secondary: "ability",
      utility: "survive"
    },

    "sky-raiders": {
      primary: "fire",
      secondary: "boost",
      utility: "maneuver"
    },

    "dungeon-zero": {
      primary: "attack",
      secondary: "interact",
      utility: "ability"
    },

    "pulse-breaker": {
      primary: "pulse",
      secondary: "dash",
      utility: "combo"
    },

    "shadow-duel": {
      primary: "attack",
      secondary: "parry",
      utility: "dodge"
    },

    "crystal-quest": {
      primary: "collect",
      secondary: "interact",
      utility: "ability"
    },

    "iron-frontier": {
      primary: "build",
      secondary: "attack-base",
      utility: "upgrade"
    },

    "ghost-signal": {
      primary: "scan",
      secondary: "hide",
      utility: "interact"
    },

    "bladefall": {
      primary: "slash",
      secondary: "heavy-slash",
      utility: "dodge"
    },

    "orbit-zero": {
      primary: "shoot",
      secondary: "boost",
      utility: "lock-target"
    },

    "wildfire": {
      primary: "attack",
      secondary: "escape",
      utility: "survive"
    },

    "rune-knight": {
      primary: "attack",
      secondary: "cast",
      utility: "quest"
    },

    "dark-circuit": {
      primary: "accelerate",
      secondary: "drift",
      utility: "boost"
    },

    "titan-core": {
      primary: "damage-boss",
      secondary: "dodge",
      utility: "target-core"
    },

    "moonfall": {
      primary: "explore",
      secondary: "collect",
      utility: "interact"
    },

    "last-fortress": {
      primary: "build",
      secondary: "attack-base",
      utility: "repair"
    },

    "phantom-chase": {
      primary: "accelerate",
      secondary: "brake",
      utility: "boost"
    },

    "abyss-walker": {
      primary: "scan",
      secondary: "attack",
      utility: "hide"
    },

    "starbreaker": {
      primary: "shoot",
      secondary: "missile",
      utility: "boost"
    },

    "kingdom-ashes": {
      primary: "attack",
      secondary: "ability",
      utility: "quest"
    },

    "zero-hour": {
      primary: "attack",
      secondary: "dash",
      utility: "timer"
    },

    "echo-maze": {
      primary: "choose",
      secondary: "interact",
      utility: "reset"
    },

    "final-horizon": {
      primary: "explore",
      secondary: "collect",
      utility: "interact"
    },

    "ajvyra-genesis": {
      primary: "attack",
      secondary: "ability",
      utility: "quest"
    }
  };

  class AJVYRAUniqueActionAdapter {
    constructor(runtime, gameId) {
      this.runtime = runtime;
      this.gameId = gameId;
      this.actions = ACTIONS[gameId] || {};
    }

    getActions() {
      return { ...this.actions };
    }

    callRuntime(method, ...args) {
      if (!this.runtime) {
        return false;
      }

      if (typeof this.runtime[method] !== "function") {
        return false;
      }

      this.runtime[method](...args);
      return true;
    }

    execute(action, payload = {}) {
      switch (action) {
        case "damage-boss":
        case "target-core":
          return this.callRuntime(
            "damageBoss",
            Number(payload.amount || 10)
          );

        case "attack-base":
          return this.callRuntime(
            "attackEnemyBase",
            Number(payload.damage || 10)
          );

        case "collect":
          return this.callRuntime(
            "collectItem",
            payload.item || {
              id: "runtime-item",
              name: "Collected Item"
            }
          );

        case "quest":
          return this.callRuntime(
            "advanceQuest",
            payload.questId || "main"
          );

        case "choose":
          return this.callRuntime(
            "submitPuzzle",
            payload.answer ?? payload.value ?? 0
          );

        case "attack":
        case "slash":
        case "heavy-slash":
        case "shoot":
        case "fire":
        case "pulse":
        case "cast":
        case "ability":
        case "combo":
        case "dash":
        case "dodge":
        case "parry":
        case "boost":
        case "reload":
        case "drift":
        case "accelerate":
        case "brake":
        case "scan":
        case "hide":
        case "explore":
        case "interact":
        case "build":
        case "upgrade":
        case "repair":
        case "escape":
        case "survive":
        case "maneuver":
        case "lock-target":
        case "missile":
        case "timer":
        case "reset":
        default:
          return this.genericAction(action, payload);
      }
    }

    genericAction(action, payload) {
      if (!this.runtime) {
        return false;
      }

      if (typeof this.runtime.handleAction === "function") {
        this.runtime.handleAction(action, payload);
        return true;
      }

      if (typeof this.runtime.dispatchAction === "function") {
        this.runtime.dispatchAction(action, payload);
        return true;
      }

      if (typeof this.runtime.emitAction === "function") {
        this.runtime.emitAction(action, payload);
        return true;
      }

      return false;
    }

    bind(element) {
      if (!element) {
        return;
      }

      element.addEventListener("ajvyra:unique-control", (event) => {
        const detail = event.detail || {};

        if (!detail.action) {
          return;
        }

        this.execute(detail.action, detail);
      });
    }
  }

  global.AJVYRAUniqueActionAdapter =
    AJVYRAUniqueActionAdapter;

  global.AJVYRAUniqueGameActions = ACTIONS;
})(window);
