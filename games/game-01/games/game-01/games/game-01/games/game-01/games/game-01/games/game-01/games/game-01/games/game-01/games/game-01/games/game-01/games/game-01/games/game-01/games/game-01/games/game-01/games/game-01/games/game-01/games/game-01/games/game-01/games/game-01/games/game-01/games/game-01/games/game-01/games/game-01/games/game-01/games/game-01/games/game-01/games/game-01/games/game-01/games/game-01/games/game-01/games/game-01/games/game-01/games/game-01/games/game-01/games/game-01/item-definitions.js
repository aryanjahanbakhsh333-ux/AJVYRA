const ITEM_DEFINITIONS = {

    energy_core: {
        id: "energy_core",
        name: "Energy Core",
        type: "quest",
        stackable: true,
        maxStack: 99
    },

    shadow_key: {
        id: "shadow_key",
        name: "Shadow Key",
        type: "key",
        stackable: false,
        maxStack: 1
    },

    health_fragment: {
        id: "health_fragment",
        name: "Health Fragment",
        type: "consumable",
        stackable: true,
        maxStack: 10
    }
};


function getItemDefinition(
    itemId
) {

    return ITEM_DEFINITIONS[
        itemId
    ] || null;
}
