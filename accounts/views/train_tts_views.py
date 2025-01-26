from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from training.tts_training import prepare_dataset, preprocess_audio, train_tacotron, train_hifi_gan

class TrainTTSView(APIView):
    def post(self, request):
        try:
            prepare_dataset()
            preprocess_audio()
            train_tacotron()
            train_hifi_gan()
            return Response({"status": True, "message": "TTS training completed successfully."}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"status": False, "message": f"Training failed: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)