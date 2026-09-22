class AJVYRAWebCombatDamage {
    static calculate(options = {}) {
        const attack = Math.max(0, Number(options.attack) || 0);
        const defense = Math.max(0, Number(options.defense) || 0);
        const multiplier = Math.max(
            0,
            Number(options.multiplier) || 1
        );

        const critical = Boolean(options.critical);

        const criticalMultiplier = critical
            ? Math.max(1, Number(options.criticalMultiplier) || 1.5)
            : 1;

        const penetration = Math.max(
            0,
            Math.min(1, Number(options.penetration) || 0)
        );

        const effectiveDefense = defense * (1 - penetration);

        const baseDamage = Math.max(
            1,
            attack * multiplier - effectiveDefense
        );

        const finalDamage = Math.max(
            1,
            Math.floor(baseDamage * criticalMultiplier)
        );

        return {
            damage: finalDamage,
            critical,
            effectiveDefense,
            multiplier,
            penetration
        };
    }

    static heal(options = {}) {
        return Math.max(
            0,
            Math.floor(Number(options.amount) || 0)
        );
    }

    static rollCritical(chance = 0) {
        const value = Math.max(
            0,
            Math.min(1, Number(chance) || 0)
        );

        return Math.random() < value;
    }

    static calculateFromStats(attacker, defender, weapon = {}) {
        const attackStats = attacker?.stats || {};
        const defenseStats = defender?.stats || {};

        const weaponPower = Math.max(
            0,
            Number(weapon.power) || 0
        );

        const attack =
            (Number(attackStats.strength) || 0) +
            weaponPower;

        const defense =
            Number(defenseStats.defense) || 0;

        const criticalChance =
            Number(weapon.criticalChance) ||
            Number(attackStats.luck) * 0.005 ||
            0;

        const critical = this.rollCritical(
            Math.min(1, criticalChance)
        );

        return this.calculate({
            attack,
            defense,
            multiplier: Number(weapon.multiplier) || 1,
            critical,
            criticalMultiplier:
                Number(weapon.criticalMultiplier) || 1.5,
            penetration:
                Number(weapon.penetration) || 0
        });
    }
}
