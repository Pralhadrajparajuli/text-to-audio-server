from django.urls import path
from accounts.views.auth_views import RegisterView, LoginView
from accounts.views.tts_views import TTSAPIView
from accounts.views.train_tts_views import TrainTTSView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('tts/', TTSAPIView.as_view(), name='tts'),
    path('api/train-tts/', TrainTTSView.as_view(), name='train_tts'),
    
]