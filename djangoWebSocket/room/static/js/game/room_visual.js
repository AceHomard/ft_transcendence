function visual_addRoom(data)
{
    let liElement = document.createElement('li');

    liElement.textContent = data["player_nb"]+" Player - ("+data["room_id"]+")";
    liElement.setAttribute("room_id", data["room_id"]);
    liElement.setAttribute('onclick', 'room_request.joinRoom("'+data["room_id"]+'")');
    liElement.id = data["room_id"]
    document.getElementById("game_list").appendChild(liElement);
}

function visual_removeRoom(data)
{
    let element = document.getElementById(data["room_id"]);
    if (element)
         element.parentNode.removeChild(element);
}

function visual_editRoom(data)
{
    let element = document.getElementById(data["room_id"]);
    if (element)
         element.textContent = data["player_nb"]+" Player - ("+data["room_id"]+")";
}