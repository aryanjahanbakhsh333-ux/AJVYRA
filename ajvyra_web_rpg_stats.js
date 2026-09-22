class AJVYRAWebRPGStats {
    constructor(initial = {}) {
        this.level = this.safeNumber(initial.level, 1);
        this.experience = this.safeNumber(initial.experience, 0);
        this.experienceToNext = this.safeNumber(initial.experienceToNext, 100);

        this.strength = this.safeNumber(initial.strength, 10);
        this.defense = this.safeNumber(initial.defense, 10);
        this.speed = this.safeNumber(initial.speed, 10);
        this.magic = this.safeNumber(initial.magic, 10);
        this.luck = this.safeNumber(initial.luck, 5);

        this.maxHealth = this.safeNumber(initial.maxHealth, 100);
        this.health = this.safeNumber(initial.health, this.maxHealth);

        this.maxMana = this.safeNumber(initial.maxMana, 50);
        this.mana = this.safeNumber(initial.mana, this.maxMana);

        this.maxStamina = this.safeNumber(initial.maxStamina, 100);
        this.stamina = this.safeNumber(initial.stamina, this.maxStamina);

        this.skillPoints = this.safeNumber(initial.skillPoints, 0);
    }

    safeNumber(value, fallback) {
        const number = Number(value);
        return Number.isFinite(number) ? number : fallback;
    }

    addExperience(amount) {
        const gained = Math.max(0, this.safeNumber(amount, 0));
        this.experience += gained;

        const levelUps = [];

        while (this.experience >= this.experienceToNext) {
            this.experience -= this.experienceToNext;
            this.level += 1;
            this.skillPoints += 1;

            this.maxHealth += 10;
            this.maxMana += 5;
            this.maxStamina += 5;

            this.health = this.maxHealth;
            this.mana = this.maxMana;
            this.stamina = this.maxStamina;

            this.experienceToNext = Math.floor(
                this.experienceToNext * 1.2
            );

            levelUps.push(this.level);
        }

        return {
            gained,
            levelUps,
            level: this.level,
            experience: this.experience,
            experienceToNext: this.experienceToNext
        };
    }

    upgrade(stat, amount = 1) {
        if (this.skillPoints <= 0) {
            return false;
        }

        const allowed = [
            "strength",
            "defense",
            "speed",
            "magic",
            "luck"
        ];

        if (!allowed.includes(stat)) {
            return false;
        }

        const value = Math.max(1, Math.floor(Number(amount) || 1));

        if (value > this.skillPoints) {
            return false;
        }

        this[stat] += value;
        this.skillPoints -= value;

        return true;
    }

    damage(amount) {
        this.health = Math.max(
            0,
            this.health - Math.max(0, Number(amount) || 0)
        );

        return this.health;
    }

    heal(amount) {
        this.health = Math.min(
            this.maxHealth,
            this.health + Math.max(0, Number(amount) || 0)
        );

        return this.health;
    }

    restoreMana(amount) {
        this.mana = Math.min(
            this.maxMana,
            this.mana + Math.max(0, Number(amount) || 0)
        );

        return this.mana;
    }

    restoreStamina(amount) {
        this.stamina = Math.min(
            this.maxStamina,
            this.stamina + Math.max(0, Number(amount) || 0)
        );

        return this.stamina;
    }

    toJSON() {
        return {
            level: this.level,
            experience: this.experience,
            experienceToNext: this.experienceToNext,
            strength: this.strength,
            defense: this.defense,
            speed: this.speed,
            magic: this.magic,
            luck: this.luck,
            maxHealth: this.maxHealth,
            health: this.health,
            maxMana: this.maxMana,
            mana: this.mana,
            maxStamina: this.maxStamina,
            stamina: this.stamina,
            skillPoints: this.skillPoints
        };
    }
}
