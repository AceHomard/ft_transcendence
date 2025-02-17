from .models import Match, Tournament, TxHash
from .serializers import Matchserializer, serialize_match_data
import json
from django.db.models import Q
from tabulate import tabulate
from .loger_config import setup_logger

logger = setup_logger(__name__)


def add_tournament_to_db(tournament_data):
    if not Tournament.objects.filter(tournament_id=tournament_data['tournament_id']).exists():
        logger.info(f'saving tournament {tournament_data["tournament_id"]} in DB')
        new_tournament = Tournament(**tournament_data)
        new_tournament.save()
    else:
        logger.debug(f"tournament {tournament_data['tournament_id']} already exists, no save needed")


def delete_tournament_from_db(tournament_id):
    if Tournament.objects.filter(tournament_id=tournament_id).exists():
        tournament = Tournament.objects.get(tournament_id=tournament_id)
        tournament.delete()
        logger.info(f"tournament {tournament_id} removed from DB")
    else:
        logger.debug(f"tournament {tournament_id} isn't in DB, no removal needed")


def add_match_to_db(match_data):
    if not Match.objects.filter(match_id=match_data['match_id']).exists():
        logger.info(f'saving match {match_data["match_id"]} in DB')
        new_match = Match(**match_data)
        new_match.save()
    else:
        logger.debug(f"match {match_data['match_id']} already exists, no save needed")


def delete_match_from_db(match_id):
    if Match.objects.filter(match_id=match_id).exists():
        match = Match.objects.get(match_id=match_id)
        match.delete()
        logger.info(f"match {match_id} removed from DB")
    else:
        logger.debug(f"match {match_id} isn't in DB, no removal needed")


def tournament_routine_db(storescore):
    if Tournament.objects.exists():
        logger.info(f" there is  {Tournament.objects.count()} tournament in DB, trying to push them")
        for tournament in Tournament.objects.all():
            tournament_dict = tournament.__dict__
            tournament_dict.pop('_state')
            tournament_dict.pop('id')
            return_code = storescore.add_tournament(tournament_dict, True)
            if return_code is True:
                logger.info(f"TX for tournament {tournament.tournament_id} is a success")
                delete_tournament_from_db(tournament.tournament_id)


def  match_routine_db(storescore):
    if Match.objects.exists():
        logger.info(f" there is {Match.objects.count()} match in DB, trying to push them")
        for match in Match.objects.all():
            match_dict = match.__dict__
            match_dict.pop('_state')
            match_dict.pop('id')
            return_code = storescore.add_match(match_dict, True)
            if return_code is True:
                logger.info(f"TX for match {match.match_id} is a success")
                delete_match_from_db(match.match_id)
            elif return_code is False:
                logger.info(f"je break")
                break


def get_match_by_playerId_db(playerId):
    matches = Match.objects.filter(Q(player1_id=playerId) | Q(player2_id=playerId))
    if matches.exists():
        match_list = list(matches.values())
        serialize = Matchserializer(data=match_list, many=True)
        if serialize.is_valid():
            validate_data = serialize.validated_data
            for match in validate_data:
                match['from_blockchain'] = False
            logger.debug(tabulate(validate_data, headers="keys", tablefmt="grid"))
            return validate_data
    else:
        return []


def get_tournament_match_by_playerId_db(playerId):
    tournaments_with_player = Tournament.objects.filter(
        Q(player1_ids__contains=[playerId]) | Q(player2_ids__contains=[playerId])
    ).all()
    if not tournaments_with_player:
        return []
    final_match_list = []
    for tournament in tournaments_with_player:
        indexs = [i for i, x in enumerate(tournament.player1_ids) if x == playerId]
        indexs.extend([i for i, x in enumerate(tournament.player2_ids) if x == playerId])
        for index in indexs:
            match_data = construct_match_data_from_tournament(tournament, index)
            validate_match = serialize_match_data(match_data)
            if validate_match:
                final_match_list.append(validate_match)
            else:
                logger.debug(validate_match.errors)
    return final_match_list


def construct_match_data_from_tournament(tournament, index):
    return {
        'match_id': tournament.match_ids[index],
        'tournament_id': tournament.tournament_id,
        'timestamp': tournament.timestamps[index],
        'player1_id': tournament.player1_ids[index],
        'player2_id': tournament.player2_ids[index],
        'player1_score': tournament.player1_scores[index],
        'player2_score': tournament.player2_scores[index],
        'winner_id': tournament.winner_ids[index]
    }
def get_match_and_tournament_by_playerId(playerId):
    matchs = get_match_by_playerId_db(playerId)
    tournament_matchs = get_tournament_match_by_playerId_db(playerId)
    result = matchs + tournament_matchs
    return result


def add_tx_to_db(match_id, tournament_id, tx):
    if match_id != 0:
        TxHash.objects.update_or_create(match_id=match_id, defaults={'tournament_id': tournament_id, 'tx_hash': tx})
    else:
        TxHash.objects.update_or_create(tournament_id=tournament_id, defaults={'match_id': match_id, 'tx_hash': tx})


def get_tx_from_db(data):
    if data['tournament_id'] == 0 and TxHash.objects.filter(match_id=data['match_id']).exists():
        tnx = TxHash.objects.get(match_id=data['match_id'])
        return tnx.tx_hash
    elif data['tournament_id'] != 0 and TxHash.objects.filter(tournament_id=data['tournament_id']).exists():
        tnx = TxHash.objects.get(tournament_id=data['tournament_id'])
        return tnx.tx_hash
    else:
        return None
