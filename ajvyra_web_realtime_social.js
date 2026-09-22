class AJVYRAWebRealtimeSocial {
    constructor(options = {}) {
        this.maxMessages = Math.max(
            10,
            options.maxMessages || 100
        );

        this.messages = [];
        this.listeners = new Map();
    }

    on(event, callback) {
        if (!this.listeners.has(event)) {
            this.listeners.set(event, new Set());
        }

        this.listeners.get(event).add(callback);

        return () => {
            this.listeners.get(event)?.delete(callback);
        };
    }

    emit(event, data) {
        const listeners = this.listeners.get(event);

        if (!listeners) {
            return;
        }

        for (const callback of [...listeners]) {
            callback(data);
        }
    }

    addChatMessage(message) {
        if (!message) {
            return false;
        }

        const text = String(message.text || "").trim();

        if (!text) {
            return false;
        }

        const entry = {
            id: message.id || crypto.randomUUID?.() || `${Date.now()}-${Math.random()}`,
            playerId: message.playerId || "unknown",
            text: text.slice(0, 500),
            timestamp: message.timestamp || Date.now()
        };

        this.messages.push(entry);

        if (this.messages.length > this.maxMessages) {
            this.messages.splice(
                0,
                this.messages.length - this.maxMessages
            );
        }

        this.emit("message", entry);

        return true;
    }

    clear() {
        this.messages.length = 0;
        this.emit("cleared");
    }

    getMessages() {
        return [...this.messages];
    }

    createPresence(player) {
        return {
            playerId: player.id,
            displayName:
                player.displayName ||
                player.name ||
                "Player",
            online: true,
            timestamp: Date.now()
        };
    }

    createSystemMessage(text) {
        return {
            playerId: "system",
            text: String(text).slice(0, 500),
            timestamp: Date.now()
        };
    }
}

if (typeof window !== "undefined") {
    window.AJVYRAWebRealtimeSocial =
        AJVYRAWebRealtimeSocial;
}
