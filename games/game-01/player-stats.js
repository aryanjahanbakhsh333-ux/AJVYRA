const PLAYER_STATS = {
    maxHealth: 100,
    health: 100,
    speed: 280,
    jumpPower: 500,
    damage: 25,
    invincibleTime: 1000
};

function resetPlayerStats() {
    PLAYER_STATS.health = PLAYER_STATS.maxHealth;
}

function damagePlayerHealth(amount) {
    PLAYER_STATS.health = Math.max(
        0,
        PLAYER_STATS.health - amount
    );

    return PLAYER_STATS.health;
}

function healPlayer(amount) {
    PLAYER_STATS.health = Math.min(
        PLAYER_STATS.maxHealth,
        PLAYER_STATS.health + amount
    );
}
