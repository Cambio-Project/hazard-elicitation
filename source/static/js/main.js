function time(date) {
    return "{}-{}-{} {}:{}:{}".format(
        date.getUTCFullYear(), date.getUTCMonth(), date.getUTCDate(),
        date.getUTCHours(), date.getUTCMinutes(), date.getUTCSeconds())
}

function formattedStack(...args) {
    const date   = new Date();
    const stack  = new Error().stack.split("\n");
    const parent = stack[stack.length - 2];
    const start  = parent.lastIndexOf("/") + 1;
    const file   = parent.substr(start, parent.length - start - 1);
    return ["{} [{}] | {}:".format(time(date), file, args[0]), ...args.slice(1)];
}

function dir() {
    console.dir(...formattedStack("DEBUG  ", ...arguments))
}

function debug() {
    console.debug(...formattedStack("DEBUG  ", ...arguments))
}

function info() {
    console.info(...formattedStack("INFO   ", ...arguments))
}

function warn() {
    console.warn(...formattedStack("WARNING", ...arguments))
}

function error(what) {
    console.error(...formattedStack("ERROR  ", ...arguments))
}


function splitAreas() {
    Split(['#left', '#bot'], {
        sizes:      [75, 25],
        minSize:    [525, 375],
        gutterSize: 5,
        cursor:     'col-resize'
    })

    Split(['#arch', '#content'], {
        sizes:      [65, 35],
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

function addChatExamples() {
    chat.add(new ChatMessage(Chat.Bot, "Hello I am a chatbot and I can help you with:"
        + "<ul>"
        + "<li>...</li>"
        + "<li>...</li>"
        + "</ul>"));
    chat.add(new ChatMessage(Chat.User, "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud "));
    chat.add(new ChatMessage(Chat.Bot, "Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui ."));
    chat.add(new ChatMessage(Chat.User, "Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium, totam rem aperiam, eaque ipsa quae ab illo inventore veritatis et quasi ."));
    chat.add(new ChatMessage(Chat.Bot, "Here you have some options ..."));
    chat.add(new ChatQuickReply([
        {"text": "finish", "action": "reply", values: ["finish"]},
        {"text": "continue", "action": "reply", values: ["continue"]},
        {"text": "another option", "action": "reply", values: ["another option"]}
    ]));
    chat.add(new ChatCard({
        "title": "Some Fact",
        "text":  "velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat"
    }));
    chat.add(new ChatCard({
        "title": "More Cards",
        "image": "https://i.ytimg.com/vi/WhIqfqPJ_kY/maxresdefault.jpg",
        "text":  "velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat",
        "link":  {
            "text": "See image in full size",
            "url":  "https://i.ytimg.com/vi/WhIqfqPJ_kY/maxresdefault.jpg"
        }
    }));
    chat.add(new ChatAccordion([{
        "title": "Some Fact",
        "text":  "velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat"
    }, {
        "title": "AnotherFact",
        "text":  "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt "
    }]));
    chat.scroll();
}

function addContentExamples() {
    content.addTab({
        "title":   "secret",
        "content": "secret"
    }, "advanced");
}

/**
 * Constants
 */
const DEBUG = true;
let graph   = null;
let chat    = null;
let content = null;

window.onload   = onLoad;
window.onunload = onUnLoad;

/**
 * Runs on page load.
 */
function onLoad() {
    splitAreas();

    graph   = new Graph("#graph", "#context-menu", sample_graph);
    chat    = new Chat("#chat", "#user-input");
    content = new Content("#content");

    if (DEBUG) {
        addChatExamples()
        addContentExamples();
    }

    Config.loadConfig();

    chat.ws.event("welcome");
}

/**
 * Runs when page is left.
 */
function onUnLoad() {
    Config.storeConfig();
}
