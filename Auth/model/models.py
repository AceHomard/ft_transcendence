from django.contrib.auth.models import AbstractUser
from django.db import models
import pyotp
import qrcode
import base64
from io import BytesIO
from django.contrib.postgres.fields import ArrayField
from .UniqId import Uniqid

class CustomUser(AbstractUser):

	profile_picture = models.ImageField(default="profile_default.png", upload_to='profile_pictures/', null=False, blank=False)
	uniqid = models.CharField(max_length=255, unique=True, null=True, blank=True)
	identifiant = models.CharField(max_length=15, unique=True, null=False, blank=False, default='')
	friends_list = ArrayField(models.CharField(max_length=255), blank=True, default=list)
	otp_secret = models.CharField(max_length=32)
	two_factor_enabled = models.BooleanField(default=False)  # Champ pour activer ou désactiver le 2FA

	username = models.CharField(max_length=15, unique=True)
	
	class Meta:
		# Définir l'application où ce modèle est déclaré
		app_label = 'model'
		# Définir le nom de la table
		db_table = 'CustomUser'

	# Résoudre les conflits de reverse accessor
	groups = models.ManyToManyField('auth.Group', related_name='custom_users', blank=True)
	user_permissions = models.ManyToManyField('auth.Permission', related_name='custom_users', blank=True)

	def save(self, *args, **kwargs):
		if not self.uniqid:
			self.uniqid = Uniqid.generate()
		super().save(*args, **kwargs)
	
	def generate_otp_qr_code(self):
		if self.otp_secret:
			# Génère l'URI de provisioning pour le TOTP
			uri = pyotp.totp.TOTP(self.otp_secret).provisioning_uri(name=self.identifiant, issuer_name='ft_transcendence')

			# Crée un objet QRCode
			qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)

			# Ajoute l'URI de provisioning au QR code
			qr.add_data(uri)
			qr.make(fit=True)

			# Crée une image QR code
			img = qr.make_image(fill_color="black", back_color="white")

			# Convertit l'image en BytesIO
			img_buffer = BytesIO()
			img.save(img_buffer, format='PNG')
			img_base64 = base64.b64encode(img_buffer.getvalue()).decode()

			# Retourne l'URI de l'image encodée en base64
			return f"data:image/png;base64,{img_base64}"
		else:
			return None

	def verify_otp(self, otp_code):
		if self.otp_secret:
			# Vérifie si l'OTP code fourni est valide
			totp = pyotp.TOTP(self.otp_secret)
			return totp.verify(otp_code)
		else:
			# Si aucun secret OTP n'est configuré, retourne False
			return False
