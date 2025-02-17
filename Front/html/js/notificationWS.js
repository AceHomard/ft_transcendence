class NotificationWS {
    #socket_url;
    #socket;
    #message_queue;
    #notification;

    constructor() {
        this.#socket_url = `wss://${window.location.host}/ws/notif/`
        this.#socket = new WebSocket(this.#socket_url);
        this.#message_queue = [];
        this.#notification = new Notification();

        this.#socketListen();
        this.#onOpenTrigger();
    }

    #onOpenTrigger()
    {
        this.#socket.onopen = () => {
            this.#flushQueue();
        };
    }


    // -------------- RECEIVE --------------

    #socketListen()
    {
        this.#socket.onmessage = (e) => {
            let data = JSON.parse(e.data);
            //console.log('NOTIF Data:', data)
            if (data["type"] === "notification")
            {
                if (data["status"] == "error")
                    this.#notification.error(data["title"], data["message"]);
                else if (data["status"] == "info")
                    this.#notification.info(data["title"], data["message"]);
            }
        };
    }

    #flushQueue()
    {
        while (this.#message_queue.length > 0)
        {
            const message = this.#message_queue.shift();
            if (message.type == 1)
                this.sendAuth();
            else if (message.type == 2)
                this.sendLang(message.language);
            else if (message.type == 5)
                this.sendDisconnect()
        }
    }


    // -------------- SEND --------------


    sendAuth()
    {
        if (this.#socket.readyState === WebSocket.OPEN)
        {
            this.#socket.send(JSON.stringify({
                type: "auth",
                session_id: getCookie("notif_id"),
                player_id: getCookie("notif_id")
            }));
        }
        else
        {
            this.#message_queue.push({type: 1});
        }
    }

    sendDisconnect()
    {
        if (this.#socket.readyState === WebSocket.OPEN)
        {
            this.#socket.send(JSON.stringify({
                type: "disconnect"
            }));
        }
        else
        {
            this.#message_queue.push({type: 5});
        }
    }


    sendLang(lang)
    {
        if (this.#socket.readyState === WebSocket.OPEN)
        {
            this.#socket.send(JSON.stringify({
                type: "lang",
                language: lang
            }));
        }
        else
        {
            this.#message_queue.push({type: 2, language: lang});
        }
    }
}
