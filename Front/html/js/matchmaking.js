/* ==================== Matchmaking ==================== */

class Matchmaking {
    #socket_url;
    #socket;
    #message_queue;

    constructor() {
        let raw_url = window.location.host.split(":");
        let url = raw_url[0] + ":8443";
        this.#socket_url = `wss://${url}/ws/room/`;
        this.#socket = new WebSocket(this.#socket_url);
        this.#message_queue = [];

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
            if (data.action != "movement_ball" && data.action != "movement_correction")
            {
                //console.log('MM RCV:', data)
            }
            if (data["type"] === "waiting_match")
                waitGame(data);
            else if (data["type"] === "waiting_tour")
                waitTour(data);
            else if (data["type"] === "waiting_time")
                waitTime(data);
            else if (data["type"] === "tour_final_waiting")
                waitingFinalTourGame();
            else if (data["type"] === "join_status_match")
                waitingPlayers(2, data.players);
            else if (data["type"] === "join_status_tour")
                waitingPlayers(4, data.players);
            else if (data["type"] === "matchmaking_canceled")
                waitCancel()
            else if (data["type"] === "game_info_tree")
            {
                in_tree = true;
                if (document.getElementById("tree_array") != null)
                    document.getElementById("tree_array").style.display = "flex";
                if (document.getElementById("play_page_queue") != null)
                    document.getElementById("play_page_queue").style.display = "none";
                
                if (document.getElementById("play_page_final_waiting_game") != null)
                    document.getElementById("play_page_final_waiting_game").remove();
                
                clearWaitingPlayers();
                clearInterval(waitingInterval);
                waiting_time = 0;
        
                let treeVisual = new TreeVisual();
        
                if (data.category == 0)
                {
                    //console.log("Match");
                    treeVisual.setMatchObj(data.info)
                    treeVisual.matchArrayInit();
                    treeVisual.matchArrayAnimation();
                }
                else if (data.category == 1)
                {
                    //console.log("Tournament");
                    treeVisual.seTourObj(data.info)
                    treeVisual.tournamentArrayInit();
                    treeVisual.tournamentArrayAnimation();
                }
            }
            else if (data["type"] === "social")
            {
                if (data["category"] === "update_global_count")
                {
                    let element = document.getElementById("social_online_nb");

                    if (element == null)
                        return ;
                    element.innerHTML = "("+data["player_count"]+")";
                }
                else if (data["category"] === "online_connect")
                    social.addPlayer(false, data["player_id"], data["name"], data["status"]);
                else if (data["category"] === "friends_connect")
                    social.addPlayer(true, data["player_id"], data["name"], data["status"]);
                else if (data["category"] === "friends_leave")
                    social.updateFriends(data["player_id"], data["status"]);
                else if (data["category"] === "online_leave")
                    social.leavePlayer(data["player_id"]);
                else if (data["category"] === "add_friend")
                    social.changeRelation(true, data["player_id"], data["name"], data["name"], data["status"]);
                else if (data["category"] === "remove_friend")
                    social.changeRelation(false, data["player_id"], data["name"], data["name"], data["status"]);
            }
            else if (data["type"] === "notification")
            {
                if (data["title"] === "error_auth_invalid")
                {
                    setCookie("token", "", -10);
                    setCookie("uniqid", "", -10);
                    location.reload()
                }
            }
            else if (data.action === 'movement_correction')
            {
                i++
                processMovementCorrection(data);
            }
            else if (data.type === "player_side")
            {
                player_side = data.side;

                document.getElementById("tree_array").style.display = "none";
                document.getElementById("canvas_game").style.display = "flex";
                //document.getElementById("cli-input").style.display = "flex";
            }
            else if (data.action === "start_game")
            {
                //console.log("--- START ---");
                document.getElementById("tree_array").style.display = "none";
                in_game_data = true;
            }
            else if (data.action === "end_game")
            {
                //console.log("--- END ---");
                in_game_data = false;
                CancelGame();
                //endGameDisplay(data.winner_id)
                end_status_win = true;
                FireworkInit();
                end_status_subtitle = data.winner_id;
                setTimeout(redirhome, 5000);
            }
            else if (data.action === "movement_ball")
            {
                game_data.ball.x = data.ball_x;
                game_data.ball.y = data.ball_y;
                game_data.ball.speed = data.ball_speed;
                in_game_data = true;
                if (in_tree == false)
                    document.getElementById("canvas_game").style.display = "flex";
                //document.getElementById("cli-input").style.display = "flex";
            }
            else if (data.action === "score_game")
            {
                game_data.player.score = data.score_player_a;
                game_data.player2.score = data.score_player_b;
            }
            else if (data.action === "game_info_timer")
            {
                if (data.time == "3")
                    in_tree = false;           
                document.getElementById("tree_array").style.display = "none";
                document.getElementById("canvas_game").style.display = "flex";
                //document.getElementById("cli-input").style.display = "flex";
                game_timer_value = data.time;
                //document.getElementById("tree_array").style.display = "none";
            }
            else
            {
                ////console.log('Home Data:', data)
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
            else if (message.type == 4)
                this.sendPlayerMovement(message.mov);
            else if (message.type == 5)
                this.sendDisconnect()
        }
    }


    // -------------- SEND --------------

    botGame()
    {
        this.#socket.send(JSON.stringify({
            type: "matchmaking",
            action: "find_game",
            "ia_game": "true"
        }))
    }

    findGame()
    {
        this.#socket.send(JSON.stringify({
            type: "matchmaking",
            action: "find_game",
            "ia_game": "none"
        }))
    }

    findTour()
    {
        this.#socket.send(JSON.stringify({
            type: "matchmaking",
            action: "find_tournament"
        }))
    }

    cancelMM()
    {
        this.#socket.send(JSON.stringify({
            type: "matchmaking",
            action: "cancel"
        }))
    }

    getActualState()
    {
        this.#socket.send(JSON.stringify({
            type: "client_status"
        }))
    }

    addFriend(user_id)
    {
        this.#socket.send(JSON.stringify({
            type: "social",
            category: "add_friend",
            user_id: user_id,
        }));
    }

    removeFriend(user_id)
    {
        this.#socket.send(JSON.stringify({
            type: "social",
            category: "remove_friend",
            user_id: user_id,
        }));
    }

    sendAuth()
    {
        if (this.#socket.readyState === WebSocket.OPEN)
        {
            this.#socket.send(JSON.stringify({
                type: "auth",
                session_id: player_id,
                player_id: player_id,
                notif_id: getCookie("notif_id")
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

    sendPlayerMovement(movement)
    {
        if (this.#socket.readyState === WebSocket.OPEN)
        {
            const data = {
                action: 'move_paddle',
                mouvement: movement
            }
            this.#socket.send(JSON.stringify(data));
        }
        else
        {
            this.#message_queue.push({type: 4, mov: movement});
        }
    }
}

function redirhome()
{
	loadContent(`https://${raw_url}/front/pong/`);
    toggleButtonsVisibility();
    end_status_loose = false;
    end_status_win = false;
    end_status_title = "";
}