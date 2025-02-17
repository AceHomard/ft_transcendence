from rest_framework.response import Response
from rest_framework.decorators import api_view

from api.postRequest import post_request
from model.models import CustomUser
from model.serializers import UserSerializer
from rest_framework import status
from rest_framework.authtoken.models import Token

from django.shortcuts import get_object_or_404, render
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.views import APIView
from rest_framework.renderers import TemplateHTMLRenderer
from .forms import UserProfileForm, ProfileImageForm
from django.http import JsonResponse
from django.views.generic import View
import json
import pyotp

from django.core.files.uploadedfile import InMemoryUploadedFile

class ProfileView(APIView):
	renderer_classes = [TemplateHTMLRenderer]
	template_name = 'profil.html'
	authentication_classes = [TokenAuthentication]
	permission_classes = [IsAuthenticated]
	
	def get(self, request, *args, **kwargs):
		user = request.user
		user_form = UserProfileForm(instance=user)
		profile_image_form = ProfileImageForm(instance=user)
		qr_code = user.generate_otp_qr_code()  # Génère le QR code du secret OTP
		return render(request, 'profil.html', {'user_form': user_form, 'profile_image_form': profile_image_form, 'qr_code': qr_code})

	def post(self, request, *args, **kwargs):
		cookie_notif = request.COOKIES.get('notif_id')
		if cookie_notif is None:
			return Response({'error': 'Invalid notif_id cookie'}, status=status.HTTP_400_BAD_REQUEST)
		user_form = UserProfileForm(request.data, instance=request.user)
		profile_image_form = ProfileImageForm(request.data, request.FILES, instance=request.user)

		if user_form.is_valid() and profile_image_form.is_valid():
			user = user_form.save(commit=False)
			user.set_password(request.data['password'])

			# Vérifier si la case two_factor_enabled est cochée
			if 'two_factor_enabled' in request.data and request.data['two_factor_enabled'] == 'on':
				# Générer le secret OTP s'il n'existe pas
				if not user.otp_secret:
					user.otp_secret = pyotp.random_base32()
			else:
				# Supprimer le secret OTP s'il existe
				if user.otp_secret:
					user.otp_secret = ''

			user.save()
			
			if 'profile_picture' in request.FILES:
				user.profile_picture = request.FILES['profile_picture']

			profile_image_form.save()
			post_request.pushNotif({"user_id":cookie_notif,"status":"info","title":"notif.info.title","message":"notif.info.form"})
			return JsonResponse({'success': True})
		else:
			errors = {'user_form': user_form.errors, 'profile_image_form': profile_image_form.errors}
			post_request.pushNotif({"user_id":cookie_notif,"status":"error","title":"notif.error.title","message":"notif.error.form"})
			return JsonResponse({'success': False, 'errors': errors})





@api_view(['POST'])
def login(request):
	cookie_notif = request.COOKIES.get('notif_id')
	identifiant = request.data['identifiant']
	if cookie_notif is None:
		return Response({'error': 'Invalid notif_id cookie'}, status=status.HTTP_400_BAD_REQUEST)
	try:
		user = CustomUser.objects.get(identifiant=identifiant)
	except CustomUser.DoesNotExist:
		post_request.pushNotif({"user_id":cookie_notif,"status":"error","title":"notif.error.title","message":"notif.error.incorrect_login"})
		return Response({'error': 'Invalid username or password'}, status=status.HTTP_400_BAD_REQUEST)
	if not user.check_password(request.data['password']):
		post_request.pushNotif({"user_id":cookie_notif,"status":"error","title":"notif.error.title","message":"notif.error.incorrect_login"})
		return Response({'error': 'Invalid username or password'}, status=status.HTTP_400_BAD_REQUEST)
	token, created = Token.objects.get_or_create(user=user)
	# Vérifier s'il a activé le 2FA
	if user.two_factor_enabled:
		return Response({'token': token.key, '2fa_required': True})
	serializer = UserSerializer(instance=user)
	return Response({"token": token.key, "user": serializer.data})


@api_view(['POST'])
def signup(request):
	serializer = UserSerializer(data=request.data)
	cookie_notif = request.COOKIES.get('notif_id')
	if cookie_notif is None:
		return Response({'error': 'Invalid notif_id cookie'}, status=status.HTTP_400_BAD_REQUEST)

	if serializer.is_valid():
		validated_data = serializer.validated_data
		# Exclure 'confirm_password' des données validées
		validated_data.pop('confirm_password', None)
		user = serializer.save()
		user.set_password(validated_data['password'])
		user.save()
		token = Token.objects.create(user=user)
		response = Response({'user': serializer.data, 'token': token.key})
		# Ajouter les en-têtes CORS appropriés
		response["Access-Control-Allow-Origin"] = "*"  # Autorise toutes les origines
		response["Access-Control-Allow-Methods"] = "POST"  # Méthode HTTP autorisée
		response["Access-Control-Allow-Headers"] = "Content-Type, Authorization"  # En-têtes autorisés
		return response
	else:
		if 'username' in serializer.errors:
			post_request.pushNotif({"user_id":cookie_notif,"status":"error","title":"notif.error.title","message":"notif.error.register_user_already_used"})
		if 'identifiant' in serializer.errors:
			post_request.pushNotif({"user_id":cookie_notif,"status":"error","title":"notif.error.title","message":"notif.error.register_id_already_used"})
		if 'password' in serializer.errors:
			for error in serializer.errors['password']:
				if error == "Les mots de passe ne correspondent pas.":
					post_request.pushNotif({"user_id":cookie_notif,"status":"error","title":"notif.error.title","message":"notif.error.password_mismatch"})
	return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def verify_otp(request):
	otp_code = request.data.get('otp_code')
	cookie_notif = request.COOKIES.get('notif_id')
	if cookie_notif is None:
		return Response({'error': 'Invalid notif_id cookie'}, status=status.HTTP_400_BAD_REQUEST)
	user = get_object_or_404(CustomUser, identifiant=request.data['identifiant'])
	# Vérifier si l'OTP est valide
	if not user.verify_otp(otp_code):
		post_request.pushNotif({"user_id":cookie_notif,"status":"error","title":"notif.error.title","message":"notif.error.otp"})
		return Response({'error': 'Invalid OTP code'}, status=status.HTTP_400_BAD_REQUEST)
	
	token, created = Token.objects.get_or_create(user=user)
	serializer = UserSerializer(instance=user)
	return Response({"token": token.key, "user": serializer.data})

@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def test_token(request):
	return Response("passed!")


@api_view(['GET'])
def user_info(request, uniqids):
	uniqid_list = uniqids.split(',')
	users = CustomUser.objects.filter(uniqid__in=uniqid_list)
	data = {}

	for user in users:
		user_data = {
			'username': user.username,
			'profile_picture': user.profile_picture.url
		}
		data[user.uniqid] = user_data

	return JsonResponse(data)

