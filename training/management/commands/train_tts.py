from django.core.management.base import BaseCommand
from training.tts_training import prepare_dataset, preprocess_audio, train_tacotron, train_hifi_gan

class Command(BaseCommand):
    help = "Train the TTS model using Tacotron 2 and HiFi-GAN."

    def handle(self, *args, **kwargs):
        self.stdout.write("Starting TTS training pipeline...")

        try:
            prepare_dataset()
            preprocess_audio()
            train_tacotron()
            train_hifi_gan()
            self.stdout.write("TTS training completed successfully!")
        except Exception as e:
            self.stderr.write(f"Error during training: {e}")