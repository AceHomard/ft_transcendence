from rest_framework import serializers


class MatchResultSerializer(serializers.Serializer):
    match_id = serializers.IntegerField()
    tournament_id = serializers.IntegerField()
    player1_score = serializers.IntegerField()
    player2_score = serializers.IntegerField()
    player1_id = serializers.IntegerField()
    player2_id = serializers.IntegerField()
    winner_id = serializers.IntegerField()
