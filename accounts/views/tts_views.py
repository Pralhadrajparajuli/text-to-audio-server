from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.http import HttpResponse
import os
import csv
from fuzzywuzzy import process

from accounts.serializers import TextInputSerializer
from utils.custom_response import custom_response
from utils.functions import load_tsv
from utils.functions import find_best_match
from utils.functions import find_best_match_fuzzy


class TTSAPIView(APIView):
    permission_classes = [IsAuthenticated]  # Ensures only authenticated users can access the TTS API
    
    def post(self, request):
        serializer = TextInputSerializer(data=request.data)
        if not serializer.is_valid():
            return custom_response(
                status_bool=False,
                message="Invalid text input.",
                http_status=status.HTTP_400_BAD_REQUEST
            )
        
        text = serializer.validated_data.get('text')

        # Load the mapping from .tsv file (audio_id -> sentence)
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))  # Project root
        audio_data_dir = os.path.join(BASE_DIR, 'data')  # Now points to the 'data' folder in the root directory
        file_path = os.path.join(audio_data_dir, 'MaleVoice.tsv')  # Adjust the name of your .tsv file
        
        audio_data = load_tsv(file_path)

        # Find the best match for the provided text (you can use exact or fuzzy matching)
        audio_id = find_best_match_fuzzy(text, audio_data)  # Use find_best_match for exact match
        if not audio_id:
            return custom_response(
                status_bool=False,
                message="Audio file not found.",
                http_status=status.HTTP_404_NOT_FOUND
            )

        # Get the corresponding audio file path
        audio_file_path = os.path.join(audio_data_dir, f"{audio_id}.wav")
        if not os.path.exists(audio_file_path):
            return custom_response(
                status_bool=False,
                message="Audio file not found.",
                http_status=status.HTTP_404_NOT_FOUND
            )

        # Send the audio file directly as a response
        with open(audio_file_path, 'rb') as f:
            response = HttpResponse(f.read(), content_type="audio/wav")
            response['Content-Disposition'] = f'attachment; filename="{audio_id}.wav"'
            return response
