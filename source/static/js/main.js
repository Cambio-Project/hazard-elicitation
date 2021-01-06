String.prototype.format = function () {
    let i = 0, args = arguments;
    return this.replace(/{}/g, function () {
        return typeof args[i] != 'undefined' ? args[i++] : '';
    });
};

function setDarkTheme(value) {
    localStorage.setItem("dark-theme", value ? "1" : "0");
    document.documentElement.className = value ? "dark-theme" : "light-theme";
}

function loadTheme() {
    let dark_mode                            = localStorage.getItem("dark-theme") !== "0";
    document.getElementById("theme").checked = dark_mode;
    setDarkTheme(dark_mode);
}
