import os
import librosa
import numpy as np
import pandas as pd
from pydub import AudioSegment
import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader
from tacotron2_model import Tacotron2  # Assumes Tacotron2 is defined in tacotron2_model.py

SAMPLE_RATE = 22050
BATCH_SIZE = 16
LEARNING_RATE = 0.001
EPOCHS = 50

# Paths
BASE_DIR = os.getcwd()
AUDIO_DIR = os.path.join(BASE_DIR, "data")
SYLLABLE_DIR = os.path.join(BASE_DIR, "Syllables")
FULL_TEXT_TSV = os.path.join(AUDIO_DIR, "MaleVoice.tsv")
SYLLABLE_TSV = os.path.join(SYLLABLE_DIR, "syllables.tsv")


class NepaliTTSDataset(Dataset):
    def __init__(self, tsv_file, audio_dir):
        self.data = pd.read_csv(tsv_file, sep='\t', header=None, names=["audio_id", "text"])
        self.audio_dir = audio_dir

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        audio_id, text = self.data.iloc[idx]
        audio_path = self._find_audio_file(audio_id)

        # Load audio and convert to mel-spectrogram
        if audio_path:
            audio = self._load_audio(audio_path)
            mel_spec = librosa.feature.melspectrogram(y=audio, sr=SAMPLE_RATE, n_mels=80)
            mel_spec = librosa.power_to_db(mel_spec, ref=np.max)
            return text, mel_spec.T

        return text, None

    def _find_audio_file(self, audio_id):
        """Finds audio file in .wav or .mp3 format."""
        wav_path = os.path.join(self.audio_dir, f"{audio_id}.wav")
        mp3_path = os.path.join(self.audio_dir, f"{audio_id}.mp3")

        if os.path.exists(wav_path):
            return wav_path
        elif os.path.exists(mp3_path):
            return mp3_path
        return None

    def _load_audio(self, file_path):
        """Loads audio from .wav or .mp3 format."""
        if file_path.endswith('.mp3'):
            audio = AudioSegment.from_mp3(file_path)
        else:
            audio = AudioSegment.from_wav(file_path)

        # Convert audio to numpy array for librosa
        samples = np.array(audio.get_array_of_samples()).astype(np.float32) / (2 ** 15)
        return librosa.resample(samples, orig_sr=audio.frame_rate, target_sr=SAMPLE_RATE)

def train_tts_model():
    dataset = NepaliTTSDataset(FULL_TEXT_TSV, AUDIO_DIR)
    dataloader = DataLoader(dataset, batch_size=BATCH_SIZE, shuffle=True, collate_fn=collate_fn)

    model = Tacotron2()
    model.train()

    criterion = nn.MSELoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=LEARNING_RATE)

    for epoch in range(EPOCHS):
        total_loss = 0.0
        for batch_idx, (texts, mels) in enumerate(dataloader):
            if len(texts) == 0:  # Skip empty batches
                continue

            optimizer.zero_grad()

            # Tacotron2 forward pass
            outputs, _ = model(texts, mels)

            # Ensure outputs are 3D (batch_size, seq_len, mel_bins)
            if len(outputs.shape) == 2:  # If output is 2D, add sequence dimension
                outputs = outputs.unsqueeze(1)  # Add sequence dimension: (batch_size, 1, mel_bins)

            # Handle the resizing condition
            if len(outputs.shape) == 3:  # Ensure output is 3D (batch_size, seq_len, mel_bins)
                if outputs.size(1) != mels.size(1):  # If sequence lengths are different
                    # Apply interpolation only on the sequence length dimension (axis 1)
                    try:
                        # Ensure input and output have the same number of dimensions
                        outputs = outputs.permute(0, 2, 1)  # Reshape to (batch_size, mel_bins, seq_len)
                        outputs_resized = torch.nn.functional.interpolate(
                            outputs, size=(mels.size(1),), mode='linear', align_corners=False
                        )
                        outputs_resized = outputs_resized.permute(0, 2, 1)  # Reshape back to (batch_size, seq_len, mel_bins)
                        outputs = outputs_resized
                    except ValueError as e:
                        print(f"Error during interpolation: {e}")
                        continue  # Skip this batch if resizing fails

            # Compute loss
            loss = criterion(outputs.squeeze(1), mels)  # Ensure dimensions match
            loss.backward()
            optimizer.step()

            total_loss += loss.item()

        print(f"Epoch [{epoch + 1}/{EPOCHS}], Loss: {total_loss / len(dataloader):.4f}")

    model_save_path = os.path.join(BASE_DIR, "tacotron2_nepali.pth")
    torch.save(model.state_dict(), model_save_path)
    print(f"Model saved at {model_save_path}")

# Updated collate_fn for improved tensor creation performance
def collate_fn(batch):
    texts, mels = zip(*[(text, mel) for text, mel in batch if mel is not None])

    # Padding mel spectrograms to the same length
    max_mel_length = max(mel.shape[0] for mel in mels)

    padded_mels = [np.pad(mel, ((0, max_mel_length - mel.shape[0]), (0, 0)), mode='constant') for mel in mels]

    # Convert the list of arrays into a single numpy array for faster tensor creation
    padded_mels_array = np.array(padded_mels)

    # Convert the numpy array to a tensor
    padded_mels_tensor = torch.tensor(padded_mels_array, dtype=torch.float32)

    return list(texts), padded_mels_tensor


if __name__ == "__main__":
    train_tts_model()