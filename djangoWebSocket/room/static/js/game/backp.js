
    //?id=04e780a1-1a8a-4b41-b971-1f50ebe7fbc1
    //?id=87ec604d-6271-46ef-9faa-82383a710835
    const queryString = window.location.search;
    const urlParams = new URLSearchParams(queryString);
    const player_id = urlParams.get('id')


    let game_url = `ws://${window.location.host}/ws/socket-server/`
    let home_url = `ws://${window.location.host}/ws/home/`

    const chatSocket = new WebSocket(game_url)
    const homeSocket = new WebSocket(home_url)

    chatSocket.onmessage = function(e){
        let data = JSON.parse(e.data)
        //console.log('Data:', data)
    }

    homeSocket.onmessage = function(e){
        let data = JSON.parse(e.data)

        if (data["type"] === "room_action")
        {
            if (data["action"] === "add")
            {
                let liElement = document.createElement('li');
                liElement.textContent = data["player_nb"]+" Player - ("+data["room_id"]+")";
                liElement.setAttribute("room_id", data["room_id"]);
                liElement.setAttribute('onclick', 'joinRoom("'+data["room_id"]+'")');
                liElement.id = data["room_id"]
                document.getElementById("game_list").appendChild(liElement);
            }
            else if (data["action"] === "remove")
            {
               let element = document.getElementById(data["room_id"]);
               if (element)
                    element.parentNode.removeChild(element);
            }
            else if (data["action"] === "player_join")
            {
                //Log.log(data["room_id"]);
               document.getElementById(data["room_id"]).textContent = data["player_nb"]+" Player - ("+data["room_id"]+")";
            }
        }
        else
        {
            //console.log('Home Data:', data)
        }
    }

    function sendMessage(message)
    {
        chatSocket.send(JSON.stringify({
            type: "'message",
            'message':message
        }))
    }

    // ============== SEND ==============

    function createRoom()
    {
        homeSocket.send(JSON.stringify({
            type: "create_room"
        }))
    }

    function joinRoom(room_id)
    {
        homeSocket.send(JSON.stringify({
            type: "join_room",
            room_id: room_id,
            player_id: player_id
        }))
    }

    // ============== RECEIVED ==============


/* ==================== Notification ==================== */
//duree des notifs info ou si il faut les fermer
//duree des notifs error ou si il faut les fermer


class Notification {

    /* in millisecondes */
    #duration_info = 4000;
    #duration_error = 4000;

    #notification;
    #notification_title;
    #notification_message;

    #active = false;
    #active_time;

    constructor() {
        this.#notification = document.getElementById("notification");
        this.#notification_title = document.getElementById("notification_title");
        this.#notification_message = document.getElementById("notification_message");
        this.reset();
    }

    reset()
    {
        //console.log("here");
        if (this.#active === true)
            clearTimeout(this.#active_time);
        this.#active = false;
        this.#notification.classList.remove("active");
        this.#notification.classList.remove("notification-error");
        this.#notification.classList.remove("notification-info");
        this.#notification_title.innerHTML = "None";
        this.#notification_message.innerHTML = "None";
    }

    #setTimeOut(time)
    {
        this.#active_time = setTimeout(function() {
            notification.reset();
        }, time);
    }

    info(title, message)
    {
        this.reset();
        this.#active = true;
        this.#notification.classList.add("active");
        this.#notification.classList.add("notification-info");
        this.#notification_title.innerHTML = title;
        this.#notification_message.innerHTML = message;
        this.#setTimeOut(this.#duration_info);
    }

     error(title, message)
    {
        this.reset();
        this.#active = true;
        this.#notification.classList.add("active");
        this.#notification.classList.add("notification-error");
        this.#notification_title.innerHTML = title;
        this.#notification_message.innerHTML = message;
        this.#setTimeOut(this.#duration_error);
    }

}