from rest_framework import serializers
from .models import CustomUser

class UserSerializer(serializers.ModelSerializer):
	profile_picture = serializers.ImageField(required=False)
	confirm_password = serializers.CharField(write_only=True)

	class Meta:
		model = CustomUser
		fields = ['id', 'username', 'email', 'password', 'profile_picture', 'confirm_password', 'identifiant', 'uniqid']
		extra_kwargs = {
			'password': {'write_only': True},
		}

	def validate_username(self, value):
		if len(value) > 15:
			raise serializers.ValidationError("Le nom d'utilisateur ne peut pas dépasser 30 caractères.")
		return value
	
	def validate(self, data):
		if data['password'] != data['confirm_password']:
			raise serializers.ValidationError({"password": "Les mots de passe ne correspondent pas."})
		return data