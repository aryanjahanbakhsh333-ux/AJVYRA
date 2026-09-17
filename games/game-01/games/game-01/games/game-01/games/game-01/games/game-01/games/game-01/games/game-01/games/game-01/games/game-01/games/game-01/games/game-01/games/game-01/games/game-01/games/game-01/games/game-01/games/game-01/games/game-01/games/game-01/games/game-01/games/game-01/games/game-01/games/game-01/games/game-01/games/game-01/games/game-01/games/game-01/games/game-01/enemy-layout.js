const ENEMY_LAYOUT = [

    {
        x: 560,
        y: 395,
        minX: 470,
        maxX: 650
    },

    {
        x: 1250,
        y: 425,
        minX: 1120,
        maxX: 1380
    },

    {
        x: 1940,
        y: 255,
        minX: 1810,
        maxX: 2070
    }
];


function createEnemyLayout(
    scene,
    group
) {

    ENEMY_LAYOUT.forEach(
        data => {

            const enemy =
                createEnemy(
                    scene,
                    data.x,
                    data.y,
                    data.minX,
                    data.maxX
                );

            group.add(enemy);
        }
    );
}
