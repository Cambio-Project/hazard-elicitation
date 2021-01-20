class CustomWebSocket {
    static WS = null;

    constructor(ws_name) {
        CustomWebSocket.WS = this;
        this.socket        = new WebSocket("ws://" + window.location.host + "/" + ws_name);

        this.socket.onopen    = this.onOpen
        this.socket.onclose   = this.onClose
        this.socket.onerror   = this.onError
        this.socket.onmessage = this.onMessage
    }

    onOpen(e) {
        debug('Open Websocket ', e)
    }

    onClose(e) {
        debug('Close Websocket ', e)
    }

    onError(e) {
        debug('Error Websocket ', e)
    }

    onMessage(e) {
        debug('On Message ', e)

        const message = JSON.parse(e.data);

        if (message.type in CustomWebSocket.WS) {
            CustomWebSocket.WS[message.type](message.data);
        } else {
            warn("No handler function for '" + message.type + "'.")
        }
    }
}

class DFWebSocket extends CustomWebSocket {
    constructor() {
        super("ws/df/");
    }

    send(data) {
        chat.setPending();
        this.socket.send(JSON.stringify({
            'type': 'dialogflow_request',
            'data': data
        }))
    }

    event(data) {
        chat.setPending();
        this.socket.send(JSON.stringify({
            'type': 'dialogflow_request',
            'data': data
        }))
    }

    dialogflow_response(data) {
        chat.removePending();
        for (const [key, val] of data._entries()) {
            const intent = val.intent;
            const type   = val.type;
            let payload  = val.payload;

            if (intent === "1-elicitation-question" && isString(payload)) {
                payload = payload.format("FRONTEND");
            }

            switch (type) {
                case 'empty':
                    break;
                case 'action':
                    chat.Commands.call(payload.action, payload.values)
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
                    debug("Unknown data type '" + type + "'.")
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

    get History() {
        return this.history;
    }

    get Commands() {
        return this.commands;
    }

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
        document.getElementsByClassName("pending-message")[0].parentElement.parentElement.remove();
    }

    append(what) {
        this.add(what);
    }

    static send(e) {
        const chat = Chat.CHAT;

        if (e.keyCode === 13) {
            e.preventDefault();

            const text = this.value.substr(0, this.value.length - 1);

            chat.History.set(text);
            chat.add(new ChatMessage(Chat.User, text));
            chat.scroll();

            chat.ws.send(text);
            this.value = "";
        } else if (e.keyCode === 38) {
            e.preventDefault();

            chat.History.prev();
            chat.chat_input.focus().val(chat.History.get());
        } else if (e.keyCode === 40) {
            e.preventDefault();

            chat.History.next();
            chat.chat_input.focus().val(chat.History.get());
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
            // TODO const action = reply.action;
            content += `<button type="button" class="btn m-md-1 quick-reply">${reply.text}</button>`;
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
                    <div class="card-header" id="accordion-${ChatAccordion.ID}-${index}-button">
                        <h5 class="mb-0">
                            <button class="btn btn-link w-100 text-left"
                                    data-toggle="collapse"
                                    data-target="#${ChatAccordion.ID}-${index}"
                                    aria-expanded="false" 
                                    aria-controls="${ChatAccordion.ID}-${index}">
                                <i class="arrow"></i>
                                &nbsp;&nbsp;${section.title}
                            </button>
                        </h5>
                    </div>
                    <div id="${ChatAccordion.ID}-${index}" 
                         class="collapse card-body" 
                         aria-labelledby="accordion-${ChatAccordion.ID}-${index}-button" 
                         data-parent="#accordion">
                        <div class="card-body">
                            ${section.text}
                        </div>
                    </div>
                </div>`;
        }

        return super.html().format(`<div class="accordion w-100">${content}</div>`);
    }
}
