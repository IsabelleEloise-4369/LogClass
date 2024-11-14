document.addEventListener("DOMContentLoaded", function () {
    const menuToggle = document.getElementById("menu-toggle");
    const mainMenu = document.getElementById("main-menu");

    menuToggle.addEventListener("click", function () {
        mainMenu.classList.toggle("show");
    });
});