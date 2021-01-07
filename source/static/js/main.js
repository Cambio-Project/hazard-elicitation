let graph        = null;
let df_websocket = null;
let chat         = null;

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

function splitAreas() {
    Split(['#left', '#bot'], {
        sizes:      [75, 25],
        minSize:    [525, 375],
        gutterSize: 5
    })

    Split(['#arch', '#content'], {
        sizes:      [75, 25],
        minSize:    [600, 300],
        gutterSize: 5,
        direction:  'vertical'
    })

    Split(['#chat', '#chat-input'], {
        sizes:      [90, 10],
        minSize:    [500, 100],
        gutterSize: 5,
        direction:  'vertical'
    })
}

function onLoad() {
    loadTheme();
    splitAreas();

    graph        = new Graph("#graph", sample_graph)
    df_websocket = new DFWebSocket();
    chat         = new Chat(df_websocket, "chat", "user-input");
}
