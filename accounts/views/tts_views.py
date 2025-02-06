from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.http import HttpResponse
import os
from accounts.serializers import TextInputSerializer
from utils.custom_response import custom_response
from utils.functions import get_audio_file_path, load_tsv
from utils.functions import find_best_match_fuzzy
from utils.functions import generate_combined_audio
from utils.functions import update_tsv
import random
from scipy.io.wavfile import write
import numpy as np

class TTSAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = TextInputSerializer(data=request.data)
        if not serializer.is_valid():
            return custom_response(
                status_bool=False,
                message="Invalid text input.",
                http_status=status.HTTP_400_BAD_REQUEST
            )

        text = serializer.validated_data.get('text')

        # Load the mappings from the .tsv files
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))  # Project root
        audio_dir = os.path.join(BASE_DIR, 'data')  # Folder containing audio files
        syllable_dir = os.path.join(BASE_DIR, 'Syllables')  # Folder containing syllable audio files
        full_text_tsv = os.path.join(audio_dir, 'MaleVoice.tsv')  # Full text audio mapping
        syllable_tsv = os.path.join(syllable_dir, 'syllables.tsv')  # Syllable audio mapping

        # Load audio mappings
        full_text_mapping = load_tsv(full_text_tsv)
        syllable_mapping = load_tsv(syllable_tsv)

        # Step 1: Try fuzzy matching for full text
        audio_id = find_best_match_fuzzy(text, full_text_mapping)
        print(f"Match found for full text: {audio_id}")
        if audio_id:
            # Try finding the audio file in both .wav and .mp3 formats
            audio_file_path = get_audio_file_path(audio_dir, audio_id)
            if audio_file_path:
                print(f"Found audio file: {audio_file_path}")
                with open(audio_file_path, 'rb') as f:
                    content_type = "audio/wav" if audio_file_path.endswith('.wav') else "audio/mpeg"
                    response = HttpResponse(f.read(), content_type=content_type)
                    response['Content-Disposition'] = f'attachment; filename="{audio_id}{os.path.splitext(audio_file_path)[1]}"'
                    return response

        print(f"No full text match found for: {text}")

        # Step 2: Fallback to generating audio by combining syllables
        sample_rate, combined_audio = generate_combined_audio(text, syllable_mapping, syllable_dir)
        if combined_audio is None:
            return custom_response(
                status_bool=False,
                message="Could not generate audio for the provided text.",
                http_status=status.HTTP_404_NOT_FOUND
            )

        # Generate a unique file name
        random_id = random.randint(100000, 999999)
        new_audio_id = f"Voice{random_id}"
        temp_file = os.path.join(audio_dir, f"{new_audio_id}.wav")

        # Save the combined audio
        write(temp_file, sample_rate, combined_audio.astype(np.int16))

        # Update the full text TSV file
        # update_tsv(full_text_tsv, new_audio_id, text)

        # Send the combined audio file as a response
        with open(temp_file, 'rb') as f:
            response = HttpResponse(f.read(), content_type="audio/wav")
            response['Content-Disposition'] = f'attachment; filename="{new_audio_id}.wav"'
            return response