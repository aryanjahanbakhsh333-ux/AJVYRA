class AJVYRAWebRPGItem {
    constructor(data = {}) {
        this.id = String(data.id || "");
        this.name = String(data.name || "Unknown Item");
        this.type = String(data.type || "misc");
        this.description = String(data.description || "");
        this.quantity = Math.max(
            0,
            Math.floor(Number(data.quantity) || 1)
        );
        this.maxStack = Math.max(
            1,
            Math.floor(Number(data.maxStack) || 99)
        );
        this.value = Math.max(
            0,
            Number(data.value) || 0
        );
        this.metadata = data.metadata || {};
    }

    clone() {
        return new AJVYRAWebRPGItem(this.toJSON());
    }

    toJSON() {
        return {
            id: this.id,
            name: this.name,
            type: this.type,
            description: this.description,
            quantity: this.quantity,
            maxStack: this.maxStack,
            value: this.value,
            metadata: this.metadata
        };
    }
}


class AJVYRAWebRPGInventory {
    constructor(options = {}) {
        this.capacity = Math.max(
            1,
            Math.floor(Number(options.capacity) || 30)
        );

        this.items = new Map();
    }

    get size() {
        return this.items.size;
    }

    has(itemId) {
        return this.items.has(String(itemId));
    }

    get(itemId) {
        return this.items.get(String(itemId)) || null;
    }

    add(itemData, quantity = 1) {
        const item = itemData instanceof AJVYRAWebRPGItem
            ? itemData.clone()
            : new AJVYRAWebRPGItem(itemData);

        const amount = Math.max(
            1,
            Math.floor(Number(quantity) || 1)
        );

        const existing = this.items.get(item.id);

        if (existing) {
            existing.quantity = Math.min(
                existing.maxStack,
                existing.quantity + amount
            );

            return existing;
        }

        if (this.items.size >= this.capacity) {
            return null;
        }

        item.quantity = Math.min(
            item.maxStack,
            amount
        );

        this.items.set(item.id, item);

        return item;
    }

    remove(itemId, quantity = 1) {
        const item = this.get(itemId);

        if (!item) {
            return false;
        }

        const amount = Math.max(
            1,
            Math.floor(Number(quantity) || 1)
        );

        item.quantity -= amount;

        if (item.quantity <= 0) {
            this.items.delete(item.id);
        }

        return true;
    }

    consume(itemId, quantity = 1) {
        const item = this.get(itemId);

        if (!item || item.quantity < quantity) {
            return null;
        }

        this.remove(itemId, quantity);

        return item;
    }

    clear() {
        this.items.clear();
    }

    toJSON() {
        return {
            capacity: this.capacity,
            items: Array.from(this.items.values()).map(
                item => item.toJSON()
            )
        };
    }

    fromJSON(data = {}) {
        this.capacity = Math.max(
            1,
            Math.floor(Number(data.capacity) || 30)
        );

        this.items.clear();

        for (const rawItem of Array.isArray(data.items)
            ? data.items
            : []) {

            const item = new AJVYRAWebRPGItem(rawItem);

            if (item.id) {
                this.items.set(item.id, item);
            }
        }

        return this;
    }
}
