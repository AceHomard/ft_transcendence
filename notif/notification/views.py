from asgiref.sync import async_to_sync
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import status
from rest_framework.decorators import api_view

from notification.ClientManager import client_manager
from notification.decode import decrypt_routine
from notification.serializer import NotifResultSerializer


# Create your views here.
@api_view(['POST'])
def new_notif(request):
    data = NotifResultSerializer(data=request.data)
    if not decrypt_routine(request):
        error_message = "Bad Token"
        return Response(error_message, status=status.HTTP_401_UNAUTHORIZED)

    if data.is_valid():
        valid_data = data.validated_data
        if not client_manager.isClientIdExist(valid_data["user_id"]):
            error_message = "Unknown user"
            return Response(error_message, status=status.HTTP_401_UNAUTHORIZED)
        client = client_manager.getClientById(valid_data["user_id"])
        async_to_sync(client.notification)(valid_data["status"], valid_data["title"], valid_data["message"])
        return Response(data=data.data, status=status.HTTP_200_OK)
    else:
        return Response(data.errors, status=status.HTTP_400_BAD_REQUEST)
