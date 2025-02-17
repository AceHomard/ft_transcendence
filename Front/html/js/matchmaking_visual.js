function waitGame(data)
{
    if (in_game_data == true)
        return ;
    if (data["status"] === true)
    {
        join("match");
    }
    else
    {
        loadContent(`https://${raw_url}/front/game/on`);
        clearInterval(waitingInterval);
        waiting_time = 0;
    }

}

function waitTour(data)
{
    if (in_game_data == true)
        return ;
    if (data["status"] === true)
    {
        join("tournament");
    }
    else
    {
        loadContent(`https://${raw_url}/front/game/on`);
        clearInterval(waitingInterval);
        waiting_time = 0;
    }
    
}

function waitingFinalTourGame()
{
    if (document.getElementById("play_page_final_waiting_game") != null)
        document.getElementById("play_page_final_waiting_game").remove();
    const waitingmain = document.createElement('div');
    waitingmain.className = 'play-page-queue-box unselectable play-page-waiting-final';
    waitingmain.id = "play_page_final_waiting_game";

    const waitingbox = document.createElement('div');
    waitingbox.className = 'play-page-waiting-final-flex';


    const waitingspan = document.createElement('span');
    waitingspan.className = 'play-page-queue-title play-page-waiting-marge';
    waitingspan.id = "play_page_final_waiting_game_span";
    waitingspan.textContent = "En attente de la 2eme partie";

    const loaderbox = document.createElement('div');
    loaderbox.className = 'loader';

    waitingmain.appendChild(waitingbox);
    waitingbox.appendChild(waitingspan);
    waitingbox.appendChild(loaderbox);
    eElement = document.getElementById("play_page_content");
    eElement.insertBefore(waitingmain, eElement.firstChild);
}

function waitTime(data)
{
    waiting_time = data["waiting_time"];
    if (document.getElementById("play_page_queue_waiting") != null)
        document.getElementById("play_page_queue_waiting").innerHTML = "00:00";
    waitingInterval = setInterval(waitingTime, 1000);
}

function clearWaitingPlayers()
{
    if (document.getElementById("players_nb_waiting") != null)
    {
        let players_nb_waiting = document.getElementById("players_nb_waiting");
        players_nb_waiting.innerHTML = '';
    }
}

function addWaitingPlayers(status)
{
    if (document.getElementById("players_nb_waiting") == null)
        return ;
    const waiting_player = document.createElement("img");
    if (status)
    {
        waiting_player.src = "img/player_on.svg";
        waiting_player.className = "play-player-nb";
    }
    else
    {
        waiting_player.src = "img/player_off.svg";
        waiting_player.className = "play-player-nb play-player-nb-off";
    }
    document.getElementById("players_nb_waiting").appendChild(waiting_player);
}

function waitingPlayers(max_players, online_players)
{
    if (online_players > max_players)
        online_players = max_players;

    clearWaitingPlayers();

    let i = 0;

    while (i < online_players)
    {
        addWaitingPlayers(true);
        i++;
    }
    while (i < max_players)
    {
        addWaitingPlayers(false);
        i++;
    }
}

function waitCancel()
{
    if (in_game_data == true)
        return ;
    document.getElementById("play_page_buttons").style.display = "flex";
    document.getElementById("play_page_queue").style.display = "none";
    clearWaitingPlayers();
    clearInterval(waitingInterval);
    waiting_time = 0;
}