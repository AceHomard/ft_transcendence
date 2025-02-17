from rest_framework.response import Response
from rest_framework.decorators import action, api_view
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.views import APIView
from rest_framework import status
from .Api_call import GetAllUniqueIds, AddNameAndImgToDict
import requests

class GameView(APIView):
	renderer_classes = [TemplateHTMLRenderer]
	template_name = 'game.html'

	def get(self, request, *args, **kwargs):
		# Retourne une réponse HTML avec les données utilisateur
		return Response(template_name=self.template_name)


class SignupView(APIView):
	renderer_classes = [TemplateHTMLRenderer]
	template_name = 'signup.html'

	def get(self, request, *args, **kwargs):
		# Retourne une réponse HTML avec les données utilisateur
		return Response(template_name=self.template_name)


class LoginView(APIView):
	renderer_classes = [TemplateHTMLRenderer]
	template_name = 'connexion.html'

	def get(self, request, *args, **kwargs):
		# Retourne une réponse HTML avec les données utilisateur
		return Response(template_name=self.template_name)

class Fa2(APIView):
	renderer_classes = [TemplateHTMLRenderer]
	template_name = '2FA.html'

	def get(self, request, *args, **kwargs):
		# Retourne une réponse HTML avec les données utilisateur
		return Response(template_name=self.template_name)

class GameOn(APIView):
	renderer_classes = [TemplateHTMLRenderer]
	template_name = 'gameOn.html'

	def get(self, request, *args, **kwargs):
		# Retourne une réponse HTML avec les données utilisateur
		return Response(template_name=self.template_name)

class Local(APIView):
	renderer_classes = [TemplateHTMLRenderer]
	template_name = 'ponglocale.html'

	def get(self, request, *args, **kwargs):
		# Retourne une réponse HTML avec les données utilisateur
		return Response(template_name=self.template_name)
	
class History(APIView):
	renderer_classes = [TemplateHTMLRenderer]
	template_name = 'history.html'

	def get(self, request, *args, **kwargs):
		# Retourne une réponse HTML avec les données utilisateur
		return Response(template_name=self.template_name)

@api_view(['GET'])
def MatchHistory(request, player_id):
	try:
		final_dict, unique_ids = GetAllUniqueIds(player_id)
		final_dict = AddNameAndImgToDict(final_dict, unique_ids, player_id)
		return Response(final_dict, status=status.HTTP_200_OK)

	except (requests.exceptions.RequestException, Exception) as e:
		return Response({"error": f"No Match found with player_id {player_id} and {e}"}, status=status.HTTP_400_BAD_REQUEST)