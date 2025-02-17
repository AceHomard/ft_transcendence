from django.contrib import admin
from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings
from .views import user_info

urlpatterns = [
	path('admin/', admin.site.urls),
    path('auth/login/', views.login),
    path('auth/signup/', views.signup),
    path('auth/verify_otp/', views.verify_otp),
    path('auth/test_token/', views.test_token),
    path('auth/profil/', views.ProfileView.as_view(), name='profil'),
    path('auth/user_info/<str:uniqids>/', user_info, name='user_info'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
