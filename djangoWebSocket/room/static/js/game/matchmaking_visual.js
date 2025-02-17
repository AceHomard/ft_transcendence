function waitGame(data)
{
    join("match");
    waiting_time = data["waiting_time"]
    /*
    if (data["status"] === true)
    {
        join("match");
        waiting_time = data["waiting_time"]
    }
    */

}

function waitTour(data)
{
    join("tournament");
        waiting_time = data["waiting_time"]
    /*
    if (data["status"] === true)
    {
        join("tournament");
        waiting_time = data["waiting_time"]
    }
    */
}

function waitCancel()
{
    document.getElementById("play_page_buttons").style.display = "flex";
    document.getElementById("play_page_queue").style.display = "none";
    clearInterval(waitingInterval);
    waiting_time = 0;
}