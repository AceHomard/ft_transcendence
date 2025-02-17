/* ==================== RoomRequest ==================== */

class RoomRequest {
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
            //console.log('ROOM Data:', data)

            if (data["type"] === "create_room")
                visual_addRoom(data);
            else if (data["type"] === "remove")
                visual_removeRoom(data);
            else if (data["type"] === "join_room")
                visual_editRoom(data);
            else if (data["type"] === "connection_etalished")
                this.#sendAuth();
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

    createRoom()
    {
        this.#socket.send(JSON.stringify({
            type: "create_room",
            "ia_game": "none",
            player_id: player_id
        }))
    }

    joinRoom(room_id)
    {
        this.#socket.send(JSON.stringify({
            type: "join_room",
            room_id: room_id,
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