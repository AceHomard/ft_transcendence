from django.shortcuts import render

from room.RoomClientManager import room_client_manager
from room.RoomManager import room_manager
from room.TournamentManager import tournament_manager


# Create your views here.
def lobby(request):
    rooms = room_manager.getRooms()
    for room in rooms:
        print("{VIEW} " + room.getId())
    return render(request, "room/play.html",
                  {"rooms": rooms})


def debug_room(request):
    waiting_room = room_manager.getWaitingRoom()
    in_game_room = []
    rooms = room_manager.getRooms()
    for room in rooms:
        if room.getId() != waiting_room:
            in_game_room.append(room)
    if waiting_room:
        waiting_room = room_manager.getRoomById(waiting_room)
    return render(request, "chat/debug_room.html",
                  {
                      "in_game_room": in_game_room,
                      "waiting_room": waiting_room
                  })


def debug_client(request):
    clients = room_client_manager.getClients()
    clients_lst = []
    for client in clients:
        ch_ad = str(hex(id(client.getChannels())))
        ch = str(hex(id(client)))
        clients_lst.append({
            "client": client,
            "channels": client.getChannels(),
            "adress": ch,
            "adress_c": ch_ad
        })

    return render(request, "chat/debug_client.html",
                  {
                      "clients_lst": clients_lst,
                  })


def debug_tournament(request):
    waiting_tour = tournament_manager.getWaitingTournament()
    in_game_tour = []
    tours = tournament_manager.getTournaments()
    for tour in tours:
        if tour.getId() != waiting_tour:
            in_game_tour.append(tour)
    if waiting_tour:
        waiting_tour = tournament_manager.getTournamentById(waiting_tour)
    return render(request, "chat/debug_tournament.html",
                  {
                      "in_game_tour": in_game_tour,
                      "waiting_tour": waiting_tour
                  })
