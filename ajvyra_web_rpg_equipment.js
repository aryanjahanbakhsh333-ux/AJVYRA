class AJVYRAWebRPGEquipment {
    constructor() {
        this.slots = {
            weapon: null,
            offhand: null,
            helmet: null,
            armor: null,
            boots: null,
            accessory1: null,
            accessory2: null
        };
    }

    equip(item) {
        if (!item || !item.id) {
            return false;
        }

        const slot = String(item.slot || item.type || "");

        if (!Object.prototype.hasOwnProperty.call(this.slots, slot)) {
            return false;
        }

        this.slots[slot] = {
            id: item.id,
            name: item.name || item.id,
            slot,
            bonuses: {
                strength: Number(item.bonuses?.strength) || 0,
                defense: Number(item.bonuses?.defense) || 0,
                speed: Number(item.bonuses?.speed) || 0,
                magic: Number(item.bonuses?.magic) || 0,
                luck: Number(item.bonuses?.luck) || 0
            }
        };

        return true;
    }

    unequip(slot) {
        if (!Object.prototype.hasOwnProperty.call(this.slots, slot)) {
            return null;
        }

        const previous = this.slots[slot];
        this.slots[slot] = null;

        return previous;
    }

    get(slot) {
        return this.slots[slot] || null;
    }

    getTotalBonuses() {
        const total = {
            strength: 0,
            defense: 0,
            speed: 0,
            magic: 0,
            luck: 0
        };

        for (const item of Object.values(this.slots)) {
            if (!item || !item.bonuses) {
                continue;
            }

            for (const stat of Object.keys(total)) {
                total[stat] += Number(item.bonuses[stat]) || 0;
            }
        }

        return total;
    }

    getEffectiveStats(baseStats = {}) {
        const bonuses = this.getTotalBonuses();

        return {
            strength: (Number(baseStats.strength) || 0) + bonuses.strength,
            defense: (Number(baseStats.defense) || 0) + bonuses.defense,
            speed: (Number(baseStats.speed) || 0) + bonuses.speed,
            magic: (Number(baseStats.magic) || 0) + bonuses.magic,
            luck: (Number(baseStats.luck) || 0) + bonuses.luck
        };
    }

    toJSON() {
        return {
            slots: structuredClone
                ? structuredClone(this.slots)
                : JSON.parse(JSON.stringify(this.slots))
        };
    }

    fromJSON(data = {}) {
        if (!data.slots || typeof data.slots !== "object") {
            return this;
        }

        for (const slot of Object.keys(this.slots)) {
            this.slots[slot] = data.slots[slot] || null;
        }

        return this;
    }
}
