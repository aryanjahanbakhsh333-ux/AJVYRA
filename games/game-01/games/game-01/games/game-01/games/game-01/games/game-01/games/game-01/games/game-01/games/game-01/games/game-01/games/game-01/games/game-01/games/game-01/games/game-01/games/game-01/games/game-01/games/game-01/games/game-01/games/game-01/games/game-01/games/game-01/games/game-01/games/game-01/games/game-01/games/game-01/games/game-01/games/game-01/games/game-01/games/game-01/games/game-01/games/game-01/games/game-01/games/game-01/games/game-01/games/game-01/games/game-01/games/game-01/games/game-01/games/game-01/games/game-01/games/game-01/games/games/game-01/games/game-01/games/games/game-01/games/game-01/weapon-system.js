const WEAPON_STATE = {

    equipped: "shadow-blade",

    damage: 25,

    range: 90,

    cooldown: 350
};


function equipWeapon(
    weaponId,
    damage,
    range,
    cooldown
) {

    WEAPON_STATE.equipped =
        weaponId;

    WEAPON_STATE.damage =
        damage;

    WEAPON_STATE.range =
        range;

    WEAPON_STATE.cooldown =
        cooldown;
}


function getEquippedWeapon() {

    return {
        ...WEAPON_STATE
    };
}
