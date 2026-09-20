function createItemPickup(
    scene,
    x,
    y,
    itemId,
    amount = 1
) {

    const definition =
        getItemDefinition(
            itemId
        );

    if (!definition) {
        return null;
    }

    const item =
        scene.add.circle(
            x,
            y,
            11,
            0xffffff
        );

    scene.physics.add.existing(
        item
    );

    item.body.setAllowGravity(
        false
    );

    item.itemId = itemId;

    item.amount = amount;

    return item;
}


function collectItemPickup(
    playerObject,
    itemObject
) {

    if (
        !itemObject ||
        !itemObject.active
    ) {
        return;
    }

    const definition =
        getItemDefinition(
            itemObject.itemId
        );

    if (!definition) {
        return;
    }

    const current =
        INVENTORY.items[
            itemObject.itemId
        ] || 0;

    const remaining =
        definition.maxStack -
        current;

    const amount =
        Math.min(
            itemObject.amount,
            remaining
        );

    if (amount <= 0) {
        return;
    }

    addItem(
        itemObject.itemId,
        amount
    );

    itemObject.destroy();
}
