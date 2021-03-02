class CustomWebSocket {
    static WS = null;

    constructor(ws_name) {
        CustomWebSocket.WS = this;
        const protocol     = window.location.protocol === "https:" ? "wss" : "ws";
        this.socket        = new WebSocket("{}://{}/{}".format(protocol, window.location.host, ws_name));

        this.socket.onopen    = this.onOpen
        this.socket.onclose   = this.onClose
        this.socket.onerror   = this.onError
        this.socket.onmessage = this.onMessage
    }

    onOpen(e) {
        chat.chat_input.attr("placeholder", "Type something and press enter...");
        chat.chat_input.removeAttr("disabled");
    }

    onClose(e) {
        chat.chat_input.attr("placeholder", "Connection lost...");
        chat.chat_input.attr("disabled", "disabled");
    }

    onError(e) { console.debug('Error Websocket ', e) }

    onMessage(e) {
        console.debug('On Message ', e)

        const message = JSON.parse(e.data);

        if (message.type in CustomWebSocket.WS) {
            CustomWebSocket.WS[message.type](message.data);
        } else {
            console.warn("No handler function for '" + message.type + "'.")
        }
    }
}

class DFWebSocket extends CustomWebSocket {
    constructor() { super("ws/df/"); }

    static isReady() {
        return new Promise(resolve => {
            function checkSocketState() {
                if (DFWebSocket.WS.socket.readyState === DFWebSocket.WS.socket.OPEN) {
                    resolve();
                } else {
                    window.setTimeout(checkSocketState, 100);
                }
            }

            checkSocketState();
        });
    }

    async send(data, contexts) {
        await DFWebSocket.isReady().then(function () {
            chat.setPending();
            const content = JSON.stringify({
                'type':     'dialogflow_text_input',
                'data':     data,
                'contexts': contexts || []
            });
            DFWebSocket.WS.socket.send(content);
            console.debug('On send ', content);
        });
    }

    async event(data, contexts) {
        await DFWebSocket.isReady().then(function () {
            const content = JSON.stringify({
                'type':     'dialogflow_event_input',
                'data':     data,
                'contexts': contexts || []
            });
            DFWebSocket.WS.socket.send(content);
            console.debug('On event ', content);
        });
    }

    /**
     * Receives a dialogflow response. The response type defines the processing.
     * @param data: Object  Take a look at existing response types.
     */
    dialogflow_response(data) {
        chat.removePending();
        for (const [key, val] of data._entries()) {
            const intent = val.intent;
            const type   = val.type;
            let payload  = val.payload;

            switch (type) {
                case 'empty':
                    break;
                case 'action':
                    chat.commands.call(payload.action, payload.values)
                    break;
                case 'text':
                    chat.add(new ChatMessage(Chat.Bot, payload.text));
                    break;
                case 'card':
                    chat.add(new ChatCard(payload));
                    break;
                case 'quick_reply':
                    chat.add(new ChatQuickReply(payload.values));
                    break;
                case 'accordion':
                    chat.add(new ChatAccordion(payload.values));
                    break;
                default:
                    console.debug("Unknown data type '" + type + "'.")
            }
        }
        chat.scroll();
    }
}

class History {
    constructor() {
        this.inputs = [];
        this.index  = 0;
        this.max    = 10;
    }

    set(input) {
        this.inputs.push(input);
        if (this.inputs.length === this.max) {
            this.inputs.shift();
        }
        this.index = this.inputs.length - 1;
    }

    get() {
        if (this.inputs.length > 0) {
            return this.inputs[this.index];
        }
        return "";
    }

    prev() {
        this.index -= 1;
        if (this.index === -1) {
            this.index = Math.min(this.inputs.length - 1, this.max);
        }
    }

    next() {
        this.index += 1;
        if (this.index === Math.min(this.inputs.length, this.max)) {
            this.index = 0;
        }
    }
}


class Chat {
    static User = "user";
    static Bot  = "bot";
    static Rich = "rich";
    static CHAT = null;

    constructor(chat_id, chat_input_id) {
        Chat.CHAT       = this;
        this.ws         = new DFWebSocket();
        this.history    = new History();
        this.commands   = new Commands();
        this.chat       = $(chat_id);
        this.chat_input = $(chat_input_id);
        this.chat_input.on("keyup", Chat.send);
    }

    static get this() { return Chat.CHAT; }

    scroll() {
        this.chat.animate({scrollTop: this.chat.prop("scrollHeight")}, 300);
    }

    add(what) {
        this.chat.append(what.html());
        this.scroll();
    }

    setPending() {
        this.add(new ChatPendingMessage());
    }

    removePending() {
        for (const el of document.getElementsByClassName("pending-message")) {
            el.parentElement.parentElement.remove();
        }
    }

    append(what) {
        this.add(what);
    }

    static addUserMessage(message) {
        Chat.this.add(new ChatMessage(Chat.User, message));
    }

    static send(e) {
        const chat = Chat.this;

        if (e.keyCode === 13) {
            e.preventDefault();

            const text = this.value.substr(0, this.value.length - 1);

            chat.history.set(text);
            chat.add(new ChatMessage(Chat.User, text));
            chat.scroll();

            chat.ws.send(text);
            this.value = "";
        } else if (e.keyCode === 38) {
            e.preventDefault();

            chat.history.prev();
            chat.chat_input.focus().val(chat.history.get());
        } else if (e.keyCode === 40) {
            e.preventDefault();

            chat.history.next();
            chat.chat_input.focus().val(chat.history.get());
        }
    }
}

class ChatElement {
    constructor(actor = Chat.Bot) {
        this.actor = actor;
    }

    html(wrap = false) {
        if (!wrap) {
            let alignment = this.actor === Chat.Rich ? "" : this.actor === Chat.User ? "flex-row-reverse" : "flex-row";

            return "" +
                `<div class="chat-content">
                  <div class="${this.actor}-content d-flex ${alignment}">
                    {}
                  </div>
                </div>`;
        } else {
            return "" +
                `<div class="chat-content">
                  <div class="${this.actor}-content wrap">
                    {}
                  </div>
                </div>`;
        }
    }
}

class ChatPendingMessage extends ChatElement {
    constructor() {
        super(Chat.Bot);
    }

    html() {
        return super.html().format(`
            <div class="card ${this.actor} pending-message">
              <div class="card-body">
                <p class="card-text">...</p>              
              </div>
            </div>`);
    }
}

class ChatMessage extends ChatElement {
    constructor(actor, text) {
        super(actor);
        this.text = text;
    }

    html() {
        return super.html().format(`
            <div class="card ${this.actor}">
              <div class="card-body">
                <p class="card-text">${this.text}</p>              
              </div>
            </div>`);
    }
}

class ChatCard extends ChatElement {
    constructor(card) {
        super(Chat.Rich);
        this.title = card.title;
        this.text  = card.text || "";
        this.image = card.image || null;
        this.link  = card.link || null;
    }

    html() {
        let image = this.image ? `<img class="card-img-top mb-3" src='${this.image}' alt=""/>` : "";
        let link  = this.link ? `
            <a href="${this.link.url}" target="_blank">
              <button class="btn" type="button">${this.link.text}</button>
            </a>` : "";

        return super.html().format(`
            <div class="card ${this.actor}">
              <div class="card-body">
                <h5 class="card-title">${this.title}</h5>
                ${image}
                <p class="card-text">${this.text}</p>
                ${link}
              </div>
            </div>`);
    }
}

class ChatQuickReply extends ChatElement {
    constructor(replies) {
        super(Chat.Rich);
        this.replies = replies;
    }

    html() {
        let content = "";
        for (const [_, reply] of this.replies._entries()) {
            const args = JSON.stringify([].concat(reply.action || []).concat(reply.values || []));
            //chat.commands.call("command", args);
            content += `<button type="button" class="btn m-md-1 quick-reply" 
                                onclick='chat.commands.call("command", ${args})'>${reply.text}</button>`;
        }

        return super.html(true).format(content);
    }
}

class ChatAccordion extends ChatElement {
    static ID = 0;

    constructor(sections) {
        super(Chat.Rich);
        this.sections = sections;
        ChatAccordion.ID += 1;
    }

    html() {
        let content = "";
        for (const [index, section] of this.sections._entries()) {
            content += "" +
                `<div class="card ${this.actor} no-shadow">
                    <div class="card-header" id="accordion-${ChatAccordion.ID}-${index}-header">
                        <h5 class="mb-0">
                            <button class="btn btn-link w-100 text-left"
                                    data-toggle="collapse"
                                    aria-expanded="false"
                                    data-target="#accordion-${ChatAccordion.ID}-${index}-body" 
                                    aria-controls="accordion-${ChatAccordion.ID}-${index}-body">
                                <i class="arrow"></i>&nbsp;&nbsp;${section.title}
                            </button>
                        </h5>
                    </div>
                    <div class="collapse card-body"
                         id="accordion-${ChatAccordion.ID}-${index}-body" 
                         aria-labelledby="accordion-${ChatAccordion.ID}-${index}-header" 
                         data-parent="#accordion-${ChatAccordion.ID}-${index}-header">
                        <div class="card-body">${section.text}</div>
                    </div>
                </div>`;
        }

        return super.html().format(`<div class="accordion w-100">${content}</div>`);
    }
}
