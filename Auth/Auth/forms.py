from django import forms
from model.models import CustomUser


class UserProfileForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    two_factor_enabled = forms.BooleanField(label='Activer le 2FA', required=False)
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password', 'two_factor_enabled']

class ProfileImageForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['profile_picture']

    def clean_profile_picture(self):
        profile_picture = self.cleaned_data.get('profile_picture')

        if profile_picture:
            valid_mime_types = ['image/jpeg', 'image/png']
            valid_extensions = ['jpg', 'jpeg', 'png']

            mime_type = profile_picture.content_type
            extension = profile_picture.name.split('.')[-1].lower()

            if mime_type not in valid_mime_types or extension not in valid_extensions:
                raise forms.ValidationError('Unsupported file type. Please upload a JPEG or PNG image.')

        return profile_picture