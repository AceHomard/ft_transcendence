/* ==================== Matchmaking ==================== */

class Matchmaking {
    #socket_url;
    #socket;

    constructor() {
        this.#socket_url = `ws://${window.location.host}/ws/room/`;
        this.#socket = new WebSocket(this.#socket_url);

        this.#socketListen();
    }


    // -------------- RECEIVE --------------

    #socketListen()
    {
        this.#socket.onmessage = (e) => {
            let data = JSON.parse(e.data);
            //console.log('MM Data:', data)

            if (data["type"] === "connection_etalished")
                this.#sendAuth();
            else if (data["type"] === "waiting_match")
                waitGame(data);
            else if (data["type"] === "waiting_tour")
                waitTour(data);
            else if (data["type"] === "matchmaking_canceled")
                waitCancel()
            else if (data["type"] === "notification")
            {
                if (data["category"] === "error")
                    notification.error(data["title"], data["message"]);
            }
            else
            {
                //console.log('Home Data:', data)
            }
        };
    }


    // -------------- SEND --------------

    findGame()
    {
        this.#socket.send(JSON.stringify({
            type: "matchmaking",
            action: "find_game",
            "ia_game": "none",
            player_id: player_id
        }))
    }

    findTour()
    {
        this.#socket.send(JSON.stringify({
            type: "matchmaking",
            action: "find_tournament",
            player_id: player_id
        }))
    }

    cancelMM()
    {
        this.#socket.send(JSON.stringify({
            type: "matchmaking",
            action: "cancel",
            player_id: player_id
        }))
    }

    #sendAuth()
    {
        this.#socket.send(JSON.stringify({
            type: "auth",
            session_id: player_id,
            player_id: player_id
        }))
    }
}