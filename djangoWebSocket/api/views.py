from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import status
from rest_framework.decorators import api_view

from Log.Log import Log
from room.RoomManager import room_manager
from room.TournamentManager import tournament_manager
from room.UniqId import Uniqid
from .PostRequest import post_request
from .decode import decrypt_routine
from .serializer import MatchResultSerializer


# Create your views here.
@api_view(['POST'])
def match_result(request):
    data = MatchResultSerializer(data=request.data)
    if not decrypt_routine(request):
        error_message = "Bad Token"
        return Response(error_message, status=status.HTTP_401_UNAUTHORIZED)
    if data.is_valid():
        valid_data = data.validated_data
        if valid_data["tournament_id"] == 0:
            if not room_manager.isRoomIdExist(str(valid_data["match_id"])):
                error_message = "Unknown match id"
                return Response(error_message, status=status.HTTP_400_BAD_REQUEST)
            valid_data["timestamp"] = Uniqid.getUnixTimeStamp()
            room_manager.removeRoomById(str(valid_data["match_id"]))
            #FOR DEBUG
            post_request.addPostResultMatch(valid_data)
            return Response(data=data.data, status=status.HTTP_200_OK)
        else:
            if not tournament_manager.isTournamentIdExist(str(valid_data["tournament_id"])):
                error_message = "Unknown tournament id"
                return Response(error_message, status=status.HTTP_400_BAD_REQUEST)
            tour = tournament_manager.getTournamentById(str(valid_data["tournament_id"]))

            if not tour.isRoomExistsById(str(valid_data["match_id"])):
                error_message = "Unknown match id"
                return Response(error_message, status=status.HTTP_400_BAD_REQUEST)
            valid_data["timestamp"] = Uniqid.getUnixTimeStamp()
            async_to_sync(tour.setRoomResult(str(valid_data["match_id"]), valid_data))
            if tour.status == 4:
                tournament_manager.removeTournamentById(str(valid_data["tournament_id"]))
            return Response(data=data.data, status=status.HTTP_200_OK)
    else:
        return Response(data.errors, status=status.HTTP_400_BAD_REQUEST)
