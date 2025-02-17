from rest_framework import serializers


class NotifResultSerializer(serializers.Serializer):
    user_id = serializers.CharField()
    status = serializers.CharField()
    title = serializers.CharField()
    message = serializers.CharField()

