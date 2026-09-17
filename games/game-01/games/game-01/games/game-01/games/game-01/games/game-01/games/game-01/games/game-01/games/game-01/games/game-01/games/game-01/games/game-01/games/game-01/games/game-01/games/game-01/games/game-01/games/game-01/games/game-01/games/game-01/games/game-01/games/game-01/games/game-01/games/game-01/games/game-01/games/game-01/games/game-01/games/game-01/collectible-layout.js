const COLLECTIBLE_LAYOUT = [

    {
        x: 180,
        y: 470
    },

    {
        x: 560,
        y: 390
    },

    {
        x: 900,
        y: 300
    },

    {
        x: 1250,
        y: 420
    },

    {
        x: 1600,
        y: 330
    },

    {
        x: 1940,
        y: 250
    },

    {
        x: 2220,
        y: 390
    }
];


function createCollectibleLayout(
    scene,
    group
) {

    COLLECTIBLE_LAYOUT.forEach(
        position => {

            const coin =
                createCoin(
                    scene,
                    position.x,
                    position.y
                );

            group.add(coin);
        }
    );
}
