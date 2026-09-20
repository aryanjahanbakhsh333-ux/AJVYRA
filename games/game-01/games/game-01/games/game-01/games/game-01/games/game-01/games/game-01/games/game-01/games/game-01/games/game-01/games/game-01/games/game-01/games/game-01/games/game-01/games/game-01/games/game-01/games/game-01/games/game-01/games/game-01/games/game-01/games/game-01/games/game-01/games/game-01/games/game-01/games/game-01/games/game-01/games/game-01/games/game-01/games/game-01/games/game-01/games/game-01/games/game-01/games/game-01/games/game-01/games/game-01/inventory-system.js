const INVENTORY = {
    items: {}
};


function addItem(
    itemId,
    amount = 1
) {

    if (!INVENTORY.items[itemId]) {

        INVENTORY.items[itemId] = 0;
    }

    INVENTORY.items[itemId] +=
        Math.max(
            0,
            amount
        );
}


function removeItem(
    itemId,
    amount = 1
) {

    if (!INVENTORY.items[itemId]) {
        return false;
    }

    if (
        INVENTORY.items[itemId] <
        amount
    ) {
        return false;
    }

    INVENTORY.items[itemId] -=
        amount;

    if (
        INVENTORY.items[itemId] <= 0
    ) {

        delete INVENTORY.items[
            itemId
        ];
    }

    return true;
}


function hasItem(
    itemId,
    amount = 1
) {

    return (
        (INVENTORY.items[itemId] || 0)
        >= amount
    );
}


function getInventory() {

    return {
        ...INVENTORY.items
    };
}
