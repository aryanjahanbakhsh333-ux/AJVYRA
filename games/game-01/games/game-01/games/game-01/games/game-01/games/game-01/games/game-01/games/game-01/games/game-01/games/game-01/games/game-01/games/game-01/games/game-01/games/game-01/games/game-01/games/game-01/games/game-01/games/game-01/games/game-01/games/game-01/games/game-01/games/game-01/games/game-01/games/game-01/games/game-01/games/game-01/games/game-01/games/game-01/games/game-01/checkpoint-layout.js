const CHECKPOINT_LAYOUT = [

    {
        x: 80,
        y: 600,
        id: "start"
    },

    {
        x: 900,
        y: 300,
        id: "checkpoint-01"
    },

    {
        x: 1600,
        y: 330,
        id: "checkpoint-02"
    }
];


function getCheckpointById(id) {

    return CHECKPOINT_LAYOUT.find(
        checkpoint =>
            checkpoint.id === id
    );
}


function activateCheckpoint(id) {

    const selected =
        getCheckpointById(id);


    if (!selected) {
        return;
    }


    setCheckpoint(
        selected.x,
        selected.y
    );
}
