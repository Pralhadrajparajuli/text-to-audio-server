import pandas as pd
import numpy as np
from g2p_en import G2p
from pathlib import Path
import subprocess

BASE_DIR = Path(__file__).resolve().parent.parent

# Constants
AUDIO_DIR = BASE_DIR / "Syllables"
METADATA_FILE = BASE_DIR / "data/metadata.csv"
TACOTRON_DIR = BASE_DIR / "tacotron2"
HIFI_GAN_DIR = BASE_DIR / "tacotron2/hifi-gan"
FILELISTS_DIR = TACOTRON_DIR / "filelists"
OUTPUT_DIR = TACOTRON_DIR / "output"
LOG_DIR = TACOTRON_DIR / "logs"


# Utility: Convert text to phonemes
def text_to_phonemes(text):
    g2p = G2p()
    phonemes = " ".join(g2p(text))
    return phonemes


# Prepare Dataset
def prepare_dataset():
    # Read metadata
    metadata = pd.read_csv(METADATA_FILE, delimiter='|', names=['audio_id', 'text'])

    # Normalize text (optional: convert to phonemes)
    metadata['text'] = metadata['text'].apply(lambda x: x.strip())

    # Split into train, validation, and test
    train, validate, test = np.split(metadata.sample(frac=1, random_state=42), [int(.8*len(metadata)), int(.9*len(metadata))])

    # Save filelists
    FILELISTS_DIR.mkdir(parents=True, exist_ok=True)

    def save_filelist(dataset, filename):
        with open(FILELISTS_DIR / filename, 'w', encoding='utf-8') as f:
            for _, row in dataset.iterrows():
                f.write(f"{AUDIO_DIR / row['audio_id']}.wav|{row['text']}\n")

    save_filelist(train, "train.txt")
    save_filelist(validate, "val.txt")
    save_filelist(test, "test.txt")
    print("Dataset preparation completed.")


# Preprocess Audio for Tacotron
def preprocess_audio():
    command = f"python {TACOTRON_DIR}/preprocess.py --filelists {FILELISTS_DIR}/train.txt {FILELISTS_DIR}/val.txt {FILELISTS_DIR}/test.txt --output_directory {OUTPUT_DIR}"
    subprocess.run(command, shell=True, check=True)
    print("Audio preprocessing completed.")


# Train Tacotron 2
def train_tacotron():
    command = f"python {TACOTRON_DIR}/train.py --output_directory {OUTPUT_DIR} --log_directory {LOG_DIR} --hparams 'batch_size=32,epochs=100'"
    subprocess.run(command, shell=True, check=True)
    print("Tacotron 2 training completed.")


# Fine-Tune HiFi-GAN
def train_hifi_gan():
    command = f"python {HIFI_GAN_DIR}/train.py --input_wavs_dir {AUDIO_DIR} --input_mels_dir {OUTPUT_DIR}/mels --checkpoint_path {HIFI_GAN_DIR}/config.json"
    subprocess.run(command, shell=True, check=True)
    print("HiFi-GAN fine-tuning completed.")