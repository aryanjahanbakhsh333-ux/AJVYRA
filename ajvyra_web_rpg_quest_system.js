class AJVYRAWebRPGQuest {
    constructor(data = {}) {
        this.id = String(data.id || "");
        this.title = String(data.title || "Quest");
        this.description = String(data.description || "");

        this.status = data.status || "available";

        this.objectives = Array.isArray(data.objectives)
            ? data.objectives.map(objective => ({
                id: String(objective.id || ""),
                description: String(objective.description || ""),
                current: Math.max(
                    0,
                    Number(objective.current) || 0
                ),
                required: Math.max(
                    1,
                    Number(objective.required) || 1
                )
            }))
            : [];

        this.rewards = data.rewards || {
            experience: 0,
            currency: 0,
            items: []
        };
    }

    updateObjective(id, amount = 1) {
        const objective = this.objectives.find(
            item => item.id === String(id)
        );

        if (!objective) {
            return false;
        }

        objective.current = Math.min(
            objective.required,
            objective.current + Math.max(0, Number(amount) || 0)
        );

        this.checkCompletion();

        return true;
    }

    checkCompletion() {
        const complete = this.objectives.length > 0 &&
            this.objectives.every(
                objective => objective.current >= objective.required
            );

        if (complete) {
            this.status = "completed";
        }

        return complete;
    }

    claim() {
        if (this.status !== "completed") {
            return null;
        }

        this.status = "claimed";

        return {
            experience: Number(this.rewards.experience) || 0,
            currency: Number(this.rewards.currency) || 0,
            items: Array.isArray(this.rewards.items)
                ? this.rewards.items
                : []
        };
    }

    toJSON() {
        return {
            id: this.id,
            title: this.title,
            description: this.description,
            status: this.status,
            objectives: this.objectives,
            rewards: this.rewards
        };
    }
}


class AJVYRAWebRPGQuestSystem {
    constructor() {
        this.quests = new Map();
    }

    addQuest(data) {
        const quest = data instanceof AJVYRAWebRPGQuest
            ? data
            : new AJVYRAWebRPGQuest(data);

        if (!quest.id) {
            return null;
        }

        this.quests.set(quest.id, quest);

        return quest;
    }

    getQuest(id) {
        return this.quests.get(String(id)) || null;
    }

    updateObjective(questId, objectiveId, amount = 1) {
        const quest = this.getQuest(questId);

        if (!quest) {
            return false;
        }

        return quest.updateObjective(objectiveId, amount);
    }

    getActiveQuests() {
        return Array.from(this.quests.values()).filter(
            quest =>
                quest.status === "available" ||
                quest.status === "active"
        );
    }

    getCompletedQuests() {
        return Array.from(this.quests.values()).filter(
            quest => quest.status === "completed"
        );
    }

    toJSON() {
        return Array.from(this.quests.values()).map(
            quest => quest.toJSON()
        );
    }

    fromJSON(data = []) {
        this.quests.clear();

        for (const questData of Array.isArray(data) ? data : []) {
            this.addQuest(questData);
        }

        return this;
    }
}
