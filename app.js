console.log("AJVYRA is online.");

const buttons = document.querySelectorAll(".button");

buttons.forEach((button) => {
    button.addEventListener("click", () => {
        console.log("AJVYRA navigation:", button.textContent.trim());
    });
});
