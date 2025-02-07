import torch
from torch.autograd import Variable
import os
from scipy.io.wavfile import write
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from accounts.serializers import TextInputSerializer
from utils.custom_response import custom_response
from utils.functions import get_audio_file_path
from tacotron2_model import Tacotron2  # Import your Tacotron2 model

from rest_framework.permissions import IsAuthenticated
from rest_framework import status
import numpy as np
import librosa

# Set the device (use GPU if available, otherwise fallback to CPU)
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
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

        # Load the trained model
        model = Tacotron2().to(device)
        model.load_state_dict(torch.load("tacotron2_nepali.pth", map_location=device, weights_only=True))
        model.eval()  # Set the model to evaluation mode

        # Generate mel spectrograms
        mel_spec = self.text_to_mel(text, model)  # Pass model as an argument
        
        # Run inference
        with torch.no_grad():
            mel_spec = Variable(mel_spec).unsqueeze(0).to(device)  # Add batch dimension
            audio = self.generate_audio_from_mel(mel_spec, model)

        # Save the generated audio to a file
        audio_file_path = self.save_audio(audio)

        # Return the generated audio file as a response
        with open(audio_file_path, 'rb') as f:
            response = HttpResponse(f.read(), content_type="audio/wav")
            response['Content-Disposition'] = f'attachment; filename="{os.path.basename(audio_file_path)}"'
            return response

    def text_to_sequence(self, text):
        """
        Convert input text to a sequence of integers (tokens).
        This function is very basic and can be extended according to your needs (e.g., use a phoneme dictionary).
        """
        # Simple preprocessing to remove unwanted characters
        text = text.strip().lower()
        
        # Example: Basic character-level tokenization (can be extended with phonemes or more complex tokenization)
        char_to_int = {char: idx for idx, char in enumerate("अआइईउऊऋएऐओऔकखगघङचछजझञटठडढणतथदधनपफबभमयरलवशषसह०१२३४५६७८९", 1)}  # Example mapping
        sequence = [char_to_int[char] for char in text if char in char_to_int]
        
        return sequence

    def text_to_mel(self, text, model):
        """
        Convert text to mel-spectrogram using the Tacotron2 model
        """
        # Convert text to sequence of tokens (you need to implement text_to_sequence)
        sequence = self.text_to_sequence(text)
        sequence = torch.tensor(sequence).unsqueeze(0).to(device)  # Add batch dimension

        # Dummy mel_inputs (you might need to replace this with actual mel input if applicable)
        mel_inputs = torch.randn(sequence.size(0), 100, 80).to(device)  # Random values or placeholder

        # Pass both text_inputs and mel_inputs to the model
        mel_spec, _ = model(sequence, mel_inputs)  # Call the model with both inputs

        print(f"Generated mel spectrogram shape: {mel_spec.shape}")
        return mel_spec

    def generate_audio_from_mel(self, mel_spec, model):
        """
        Convert mel spectrograms to audio using Griffin-Lim vocoder
        """
        # Check the mel_spec shape to ensure it's correct
        print(f"Mel spectrogram shape: {mel_spec.shape}")  # Add this line for debugging

        # Griffin-Lim parameters
        n_iter = 60
        hop_length = 256
        win_length = 1024
        power = 1.5

        # Convert mel spectrogram back to audio using Griffin-Lim
        mel_spec = mel_spec.squeeze(0).cpu().numpy()  # Remove batch dimension and convert to numpy
        reconstructed_waveform = librosa.feature.inverse.mel_to_audio(mel_spec,
                                                                    n_iter=n_iter,
                                                                    hop_length=hop_length,
                                                                    win_length=win_length,
                                                                    power=power)


        return reconstructed_waveform

    def save_audio(self, audio):
        """
        Save the audio numpy array as a .wav file
        """
        output_path = os.path.join("data", "generated_audio.wav")
        write(output_path, 22050, audio.astype(np.int16))  # 22050 Hz sample rate
        return output_path