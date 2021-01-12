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

    dialogflow_response(data) {
        chat.removePending();
        for (const i in data) {
            const type = data[i].type;
            const payload = data[i].payload;

            switch (type) {
                case 'text':
                    chat.add(new ChatMessage(Chat.Bot, payload));
                    break;
                case 'quick_reply':
                    chat.add(new ChatQuickReply(payload));
                    break;
                case 'card':
                    chat.add(new ChatCard(payload));
                    break;
                case 'accordion':
                    chat.add(new ChatAccordion(payload));
                    break;
                default:
                    debug("Unknown data type '" + type + "'.")
            }
        }
        chat.scroll();
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
        this.chat       = document.getElementById(chat_id);
        this.chat_input = document.getElementById(chat_input_id);
        this.chat_input.addEventListener("keyup", this.send);
    }

    scroll() {
        this.chat.scrollTop = this.chat.scrollHeight - this.chat.clientHeight;
    }

    add(what) {
        this.chat.innerHTML += what.html();
    }

    setPending() {
        this.add(new ChatPendingMessage());
    }

    removePending() {
        document.getElementsByClassName("pending-message")[0].parentElement.parentElement.remove();
    }

    append(what) {
        this.chat.innerHTML += what;
    }

    send(e) {
        if (e.keyCode === 13) {
            e.preventDefault();
            Chat.CHAT.add(new ChatMessage(Chat.User, this.value));
            Chat.CHAT.ws.send(this.value);
            Chat.CHAT.scroll();
            this.value = "";
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
            <div class="card shadow ${this.actor} pending-message">
              <div class="card-body">
                <p class="card-text">...</p>              
              </div>
            </div>`);
    }
}

class ChatMessage extends ChatElement {
    constructor(actor, message) {
        super(actor);
        this.message = message;
    }

    html() {
        return super.html().format(`
            <div class="card shadow ${this.actor}">
              <div class="card-body">
                <p class="card-text">${this.message}</p>              
              </div>
            </div>`);
    }
}

class ChatCard extends ChatElement {
    constructor(card) {
        super(Chat.Rich);
        this.title   = card.title;
        this.message = card.message;
        this.image   = card.image || null;
        this.href    = card.link || null;
    }

    html() {
        let image = this.image ? `<img class="card-img-top" src='${this.image}' alt=""/>` : "";
        let link  = this.href ? `<a class="btn btn-primary text-white">${this.href}</a>` : "";

        return super.html().format(`
            <div class="card shadow">
              <div class="card-body">
                <h5 class="card-title">${this.title}</h5>
                ${image}
                <p class="card-text">${this.message}</p>
                ${link}
              </div>
            </div>`);
    }
}

class ChatQuickReply extends ChatElement {
    constructor(titles) {
        super(Chat.Rich);
        this.titles = titles;
    }

    html() {
        let content = "";
        for (const title in this.titles) {
            content += `<button type="button" class="btn btn-secondary shadow quick-reply">${this.titles[title]}</button>`;
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
        for (const section in this.sections) {
            content += "" +
                `<div class="card rounded-0">
                    <div class="card-header rounded-0" 
                         id="accordion-${ChatAccordion.ID}-${section}-button">
                        <h5 class="mb-0">
                            <button class="btn btn-link w-100 text-left"
                                    data-toggle="collapse"
                                    data-target="#${ChatAccordion.ID}-${section}"
                                    aria-expanded="false" 
                                    aria-controls="${ChatAccordion.ID}-${section}">
                                <i class="arrow"></i>
                                &nbsp;&nbsp;${this.sections[section].title}
                            </button>
                        </h5>
                    </div>
                    <div id="${ChatAccordion.ID}-${section}" 
                         class="collapse" 
                         aria-labelledby="accordion-${ChatAccordion.ID}-${section}-button" 
                         data-parent="#accordion">
                        <div class="card-body">
                            ${this.sections[section].content}
                        </div>
                    </div>
                </div>`;
        }

        return super.html().format(`<div class="accordion w-100 shadow">${content}</div>`);
    }
}
