from django.conf import settings
from .StoreInDB import (tournament_routine_db, match_routine_db, get_tx_from_db, get_match_and_tournament_by_playerId)
from rest_framework.response import Response
from .serializers import Matchserializer, Tournament_group_data, SendDbMatchToSerializer
from rest_framework import status
from rest_framework.decorators import api_view
from .loger_config import setup_logger
from .decrypt_token import decrypt_routine
from .utils import process_matches
logger = setup_logger(__name__)


@api_view(['GET'])
def match_get_api(request, match_id):
    storescore = settings.STORE_SCORE
    match = storescore.get_match_by_id(match_id)
    if match is None:
        return Response({"error": f"No match found with id {match_id}"}, status=status.HTTP_404_NOT_FOUND)
    match_json = SendDbMatchToSerializer(match)
    if match_json.is_valid():
        return Response(match_json.data, status=status.HTTP_200_OK)
    return Response(match_json.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def match_post_api(request):
    storescore = settings.STORE_SCORE
    if not decrypt_routine(request):
        return Response(status=status.HTTP_401_UNAUTHORIZED)
    match_data = Matchserializer(data=request.data)
    if not match_data.is_valid():
        return Response(match_data.errors, status=status.HTTP_400_BAD_REQUEST)
    validated_data = match_data.validated_data
    match_routine_db(storescore)
    return storescore.add_match(validated_data, False)

@api_view(['GET'])
def tournament_get_api(request, tournament_id):
    storescore = settings.STORE_SCORE
    tournament = storescore.get_tournament_by_id(tournament_id)
    tournament_json = []
    if tournament is not None:
        for match in tournament:
            match_json = SendDbMatchToSerializer(match)
            if match_json.is_valid():
                tournament_json.append(match_json.data)
        return Response(tournament_json, status=status.HTTP_200_OK)
    else:
        return Response({"error": f"No tournament found with id {tournament_id}"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def tournament_post_api(request):
    storescore = settings.STORE_SCORE
    if not decrypt_routine(request):
        return Response(status=status.HTTP_401_UNAUTHORIZED)
    raw_tournament = Matchserializer(data=request.data, many=True)
    if raw_tournament.is_valid():
        validated_data = raw_tournament.validated_data
        tournament_data = Tournament_group_data(validated_data)
        tournament_routine_db(storescore)
        return storescore.add_tournament(tournament_data, False)
    else:
        return Response(raw_tournament.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def GetMatchByPlayerApi(request, player_id):
    storescore = settings.STORE_SCORE
    matchs_from_BC = storescore.get_match_by_player(player_id)
    matchs_from_DB = get_match_and_tournament_by_playerId(player_id)
    if not matchs_from_BC and not matchs_from_DB:
        return Response({"error": f"No matches found with player_id {player_id}"}, status=status.HTTP_400_BAD_REQUEST)
    return_matchs = process_matches(matchs_from_BC, matchs_from_DB)
    return Response(return_matchs, status=status.HTTP_200_OK)


@api_view(['get'])
def test(request):
    try:
        storescore = settings.STORE_SCORE
        storescore.get_gas_price_by_api()
        return Response("ok", status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": str(e).lower()}, status=status.HTTP_400_BAD_REQUEST)
