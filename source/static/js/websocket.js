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
        console.log('Open Websocket ', e)
    }

    onClose(e) {
        console.log('Close Websocket ', e)
    }

    onError(e) {
        console.log('Error Websocket ', e)
    }

    onMessage(e) {
        console.log('On Message ', e)

        const message = JSON.parse(e.data);

        if (message.type in CustomWebSocket.WS) {
            CustomWebSocket.WS[message.type](message.data);
        } else {
            console.log("No handler function for '" + message.type + "'.")
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
                    console.log("Unknown data type '" + type + "'.")
            }
        }
        chat.scroll();
    }
}
