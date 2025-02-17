from rest_framework import serializers
from django.core.validators import MinValueValidator
from .models import Match


class Matchserializer(serializers.Serializer):
    match_id = serializers.IntegerField(validators=[MinValueValidator(0)])
    tournament_id = serializers.IntegerField(validators=[MinValueValidator(0)])
    timestamp = serializers.IntegerField(validators=[MinValueValidator(0)])
    player1_score = serializers.IntegerField(validators=[MinValueValidator(0)])
    player2_score = serializers.IntegerField(validators=[MinValueValidator(0)])
    player1_id = serializers.IntegerField(validators=[MinValueValidator(0)])
    player2_id = serializers.IntegerField(validators=[MinValueValidator(0)])
    winner_id = serializers.IntegerField(validators=[MinValueValidator(0)])


def Tournament_group_data(validated_data):
    matches = zip(*[item.values() for item in validated_data])
    match_ids, tournament_ids, timestamp, player1_scores, player2_scores, player1_ids, player2_ids, winner_ids = map(list, matches)

    tournament_dict = {
        'match_ids': match_ids,
        'tournament_id': tournament_ids[0],
        'timestamps': timestamp,
        'player1_scores': player1_scores,
        'player2_scores': player2_scores,
        'player1_ids': player1_ids,
        'player2_ids': player2_ids,
        'winner_ids': winner_ids
    }
    return tournament_dict


def SendDbMatchToSerializer(match):
    match_json = Matchserializer(data={
        "match_id": match[0],
        "tournament_id": match[1],
        "timestamp": match[2],
        "player1_score": match[6],
        "player2_score": match[7],
        "player1_id": match[3],
        "player2_id": match[4],
        "winner_id": match[5],
    })
    return match_json


def serialize_match_data(match_data):
    serialize = Matchserializer(data=match_data)
    if serialize.is_valid():
        validated_data = serialize.validated_data
        validated_data['from_blockchain'] = False
        return validated_data
    return None
