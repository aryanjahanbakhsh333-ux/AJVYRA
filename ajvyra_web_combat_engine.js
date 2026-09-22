class AJVYRAWebCombatEngine {
    constructor(options = {}) {
        this.weaponSystem =
            options.weaponSystem ||
            new AJVYRAWebCombatWeaponSystem();

        this.skillSystem =
            options.skillSystem ||
            new AJVYRAWebCombatSkillSystem();

        this.statusManager =
            options.statusManager ||
            new AJVYRAWebCombatStatusManager();

        this.events = [];
    }

    emit(event) {
        this.events.push({
            timestamp: Date.now(),
            ...event
        });

        if (this.events.length > 500) {
            this.events.shift();
        }
    }

    attack(attacker, defender, weaponId, now = Date.now()) {
        if (!attacker || !defender) {
            return {
                success: false,
                reason: "invalid_entities"
            };
        }

        if (
            attacker.health !== undefined &&
            attacker.health <= 0
        ) {
            return {
                success: false,
                reason: "attacker_dead"
            };
        }

        if (
            defender.health !== undefined &&
            defender.health <= 0
        ) {
            return {
                success: false,
                reason: "defender_dead"
            };
        }

        const weaponResult =
            this.weaponSystem.use(
                attacker.id,
                weaponId,
                now
            );

        if (!weaponResult.success) {
            return weaponResult;
        }

        const weapon = weaponResult.weapon;

        const result =
            AJVYRAWebCombatDamage.calculateFromStats(
                attacker,
                defender,
                weapon
            );

        const damage = result.damage;

        if (typeof defender.takeDamage === "function") {
            defender.takeDamage(damage);
        } else if (
            typeof defender.health === "number"
        ) {
            defender.health = Math.max(
                0,
                defender.health - damage
            );
        }

        const event = {
            type: "attack",
            attackerId: attacker.id,
            defenderId: defender.id,
            weaponId: weapon.id,
            damage,
            critical: result.critical
        };

        this.emit(event);

        return {
            success: true,
            ...event
        };
    }

    useSkill(attacker, defender, skillId, now = Date.now()) {
        if (!attacker || !defender) {
            return {
                success: false,
                reason: "invalid_entities"
            };
        }

        const result =
            this.skillSystem.use(
                attacker,
                skillId,
                now
            );

        if (!result.allowed) {
            return {
                success: false,
                reason: result.reason
            };
        }

        const skill = result.skill;

        if (skill.type === "heal") {
            if (typeof attacker.heal === "function") {
                attacker.heal(skill.power);
            }

            const event = {
                type: "skill_heal",
                attackerId: attacker.id,
                skillId: skill.id,
                amount: skill.power
            };

            this.emit(event);

            return {
                success: true,
                ...event
            };
        }

        const attackerStats =
            attacker.stats || {};

        const defenderStats =
            defender.stats || {};

        const resultDamage =
            AJVYRAWebCombatDamage.calculate({
                attack:
                    (Number(attackerStats.magic) || 0) +
                    skill.power,

                defense:
                    Number(defenderStats.defense) || 0,

                multiplier:
                    Number(skill.metadata.multiplier) || 1,

                critical:
                    Boolean(skill.metadata.critical),

                penetration:
                    Number(skill.metadata.penetration) || 0
            });

        if (typeof defender.takeDamage === "function") {
            defender.takeDamage(resultDamage.damage);
        } else if (
            typeof defender.health === "number"
        ) {
            defender.health = Math.max(
                0,
                defender.health - resultDamage.damage
            );
        }

        if (skill.metadata.status) {
            this.statusManager.apply(
                defender.id,
                skill.metadata.status
            );
        }

        const event = {
            type: "skill_attack",
            attackerId: attacker.id,
            defenderId: defender.id,
            skillId: skill.id,
            damage: resultDamage.damage
        };

        this.emit(event);

        return {
            success: true,
            ...event
        };
    }

    update(delta, entities = []) {
        for (const entity of entities) {
            if (!entity || entity.id === undefined) {
                continue;
            }

            this.statusManager.update(
                entity.id,
                delta,
                entity
            );
        }
    }

    getRecentEvents() {
        return [...this.events];
    }

    clearEvents() {
        this.events.length = 0;
    }
}
