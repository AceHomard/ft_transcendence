let waiting_time = 0;
var waitingInterval = 0;

function join(type)
{
    document.getElementById("play_page_buttons").style.display = "none";
    document.getElementById("play_page_queue").style.display = "flex";

    if (type === "match")
    {
        document.getElementById("play_page_queue_buttons").style.width = "200px";
		document.getElementById("play_page_queue_title_tournament").style.display = "none";
        document.getElementById("play_page_queue_title_match").style.display = "flex";

	}
    else
    {
        document.getElementById("play_page_queue_buttons").style.width = "260px";
        document.getElementById("play_page_queue_title_match").style.display = "none";
        document.getElementById("play_page_queue_title_tournament").style.display = "flex";
    }
}

function joinBot()
{
    isBotGame = true;
    matchmaking.botGame()
}

function joinMatch()
{
    matchmaking.findGame()
}

function joinTour()
{
    matchmaking.findTour();
}



function cancelMM()
{
    matchmaking.cancelMM()
}



function digitNumber(number)
{
    return number < 10 ? '0' + number : '' + number;
}

function getUnixTime()
{
    let date = new Date();

    let offsetParis = 60;
    let offsetCurrentTimezone = date.getTimezoneOffset();
    let offsetTotal = offsetCurrentTimezone + offsetParis;
    date.setMinutes(date.getMinutes() + offsetTotal);
    let unixTimeUTCParis = date.getTime() / 1000;
    return (unixTimeUTCParis)
}

function waitingTime()
{
    const d = new Date();

    waiting_time += 1
    let minutes = Math.floor(waiting_time / 60);
    let secondes = waiting_time % 60;

    document.getElementById("play_page_queue_waiting").innerHTML = digitNumber(minutes)+":"+digitNumber(secondes);
}