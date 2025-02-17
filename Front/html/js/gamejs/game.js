'use strict';

class GameWebSocket {
    #socket_url;
    #socket;
    #message_queue;

    constructor() {
        this.#socket_url = `wss://${window.location.host}/ws/game/`;
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
            //console.log('GM Data:', data);
        }

        if (data.action === 'movement_correction')
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
            if(isBotGame === true && data.winner_id == "Unknown")
            {
                end_status_subtitle = "BOT";
            }
            isBotGame = false;
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
        else if (data.action === "game_side_info")
        {
            img_a.src = data.info.player1_avatar;
            img_b.src = data.info.player2_avatar;
            player_a_name = data.info.player1_name;
            player_b_name = data.info.player2_name;
            if (isBotGame)
            {
                img_b.src = "/media/bot.png";
                player_b_name = "BOT";
            }
        }
        else if (data.action === "game_info_timer")
        {
            document.getElementById("tree_array").style.display = "none";
            document.getElementById("canvas_game").style.display = "flex";
            //document.getElementById("cli-input").style.display = "flex";
            game_timer_value = data.time;
            //document.getElementById("tree_array").style.display = "none";
        }
        else
        {
            //console.log('GM Data:', data)
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
                this.sendPlayerMovement(message.mov);
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
                action: "auth",
                session_id: player_id,
                player_id: player_id
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
            this.#message_queue.push({type: 2, mov: movement});
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