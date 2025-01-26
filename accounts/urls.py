from django.urls import path
from accounts.views.auth_views import RegisterView, LoginView
from accounts.views.tts_views import TTSAPIView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('tts/', TTSAPIView.as_view(), name='tts')
    
]