const UI_THEME = {
    font: "Arial, Helvetica, sans-serif",

    primary: "#ffffff",
    secondary: "#aaaaaa",
    muted: "#666666",
    panel: "#0b0b0b",
    border: "#292929",

    transition: 180
};


function createUIText(
    scene,
    x,
    y,
    text,
    size = 18
) {

    return scene.add.text(
        x,
        y,
        text,
        {
            fontFamily: UI_THEME.font,
            fontSize: `${size}px`,
            color: UI_THEME.primary
        }
    );
}
