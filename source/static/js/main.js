function splitAreas() {
    Split(['#left', '#bot'], {
        sizes:      [70, 30],
        minSize:    [550, 450],
        gutterSize: 5,
        cursor:     'col-resize'
    })

    Split(['#arch', '#content'], {
        sizes:      [65, 35],
        minSize:    [600, 50],
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

function populateArchitectures() {
    const fillSelect = function (arches) {
        const select = $("#graph-selection");
        $.each(arches, function (_, g) {
            const o = $("<option />").val(g["name"]).text(g["name"]);
            select.append(o);
        });
    }

    fetch("api/archlist/")
        .then(response => response.json())
        .then(arches => fillSelect(arches));
}

/**
 * Constants
 */
const DEBUG   = false;
let graph     = null;
let chat      = null;
let content   = null;
let scenarios = null;

window.onload   = onLoad;

/**
 * Runs on page load.
 */
function onLoad() {
    splitAreas();
    populateArchitectures();

    content = new Content("#content");
    graph   = new Graph("#graph", "#context-menu", {nodes: {}, edges: {}, analysis: {}});
    chat    = new Chat("#chat", "#user-input");

    $('[data-toggle="tooltip"]').tooltip();

    Config.loadConfig();
    Config.setStorage("uuid", Config.getStorage("uuid") || uuid.v4());

    chat.ws.event("e-welcome");
}
