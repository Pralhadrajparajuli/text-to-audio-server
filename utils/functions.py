import csv
from fuzzywuzzy import process
import numpy as np
from pydub import AudioSegment
import os
from scipy.io.wavfile import read


AudioSegment.ffmpeg = "/usr/local/bin/ffmpeg"
AudioSegment.ffprobe = "/usr/local/bin/ffprobe"

def load_tsv(file_path):
    """Load TSV file and map sentences to audio IDs."""
    syllable_mapping = {}
    with open(file_path, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file, delimiter='\t')
        for row in reader:
            audio_id = row.get('audio_id')
            sentence = row.get('sentence', '').strip()
            if audio_id and sentence:  # Ensure valid data
                syllable_mapping[sentence] = audio_id
            else:
                print(f"Skipping row due to missing fields: {row}")
    return syllable_mapping

def find_best_match_fuzzy(text, syllable_mapping):
    """Find the best match for a syllable in the syllable mapping."""
    # Check for an exact match first
    if text in syllable_mapping:
        return syllable_mapping[text]
    
    # Fuzzy match fallback
    sentences = sorted(syllable_mapping.keys(), key=len, reverse=True)  # Sort by length (longest first)
    best_match = process.extractOne(text, sentences)
    if best_match and best_match[1] > 90:  # Confidence threshold
        return syllable_mapping[best_match[0]]  # Return the matched audio_id
    return None

def trim_silence(audio, sample_rate, threshold=100):
    """Trim silence from audio data."""
    trimmed_audio = audio[np.abs(audio) > threshold]
    return np.concatenate((trimmed_audio, np.zeros(int(0.01 * sample_rate))))  # Add slight padding

def split_into_syllables(text, syllable_mapping):
    """Split text into syllables and map to audio IDs."""
    print(f"Original text: {text}")
    syllables = []
    current_syllable = ""

    # Nepali vowel signs
    vowels = ['ो', 'ा', 'ी', 'ु', 'े', 'ै', 'ि', 'ं', 'ँ']
    
    for char in text:
        # If the character is a vowel or diacritic, append it to the current syllable
        if char in vowels:
            current_syllable += char
        elif char == '्':  # Handling '्' (virama) as part of the previous syllable
            current_syllable += char
        else:
            # When a new character is encountered, check if the current syllable has a valid mapping
            if current_syllable:
                # Check if there's a mapping for the syllable
                if current_syllable in syllable_mapping:
                    syllables.append(syllable_mapping[current_syllable])
                else:
                    print(f"No match found for syllable: {current_syllable}")
            # Start a new syllable
            current_syllable = char
    
    # After the loop, check if the last syllable has a valid mapping
    if current_syllable:
        if current_syllable in syllable_mapping:
            syllables.append(syllable_mapping[current_syllable])
        else:
            print(f"No match found for syllable: {current_syllable}")
    
    print(f"Split syllables (audio IDs): {syllables}")
    return syllables

def get_audio_file_path(audio_dir, audio_id):
    """
    Returns the path to an audio file, checking for both .wav and .mp3 formats.
    """
    wav_file_path = os.path.join(audio_dir, f"{audio_id}.wav")
    mp3_file_path = os.path.join(audio_dir, f"{audio_id}.mp3")

    if os.path.exists(wav_file_path):
        return wav_file_path
    elif os.path.exists(mp3_file_path):
        return mp3_file_path
    return None

def generate_combined_audio(text, syllable_mapping, audio_dir):
    """Generate combined audio for text."""
   
    audio_clips = []
    syllables = split_into_syllables(text, syllable_mapping)

    for audio_id in syllables:
        audio_file_path = get_audio_file_path(audio_dir, audio_id)
        if audio_file_path:
            print(f"Found audio file: {audio_file_path}")
            if audio_file_path.endswith('.mp3'):
                # Handle .mp3 file using pydub
                audio_data = AudioSegment.from_mp3(audio_file_path)
                sample_rate = audio_data.frame_rate  # Get the frame rate before converting to numpy
                audio_data = np.array(audio_data.get_array_of_samples())
            else:
                # Handle .wav file using scipy
                sample_rate, audio_data = read(audio_file_path)  # Read both sample rate and audio data

            trimmed_audio = trim_silence(audio_data, sample_rate)
            audio_clips.append(trimmed_audio)
        else:
            print(f"Audio file not found: {audio_file_path}")

    if audio_clips:
        combined_audio = np.concatenate(audio_clips)
        return sample_rate, combined_audio
    return None, None

def update_tsv(file_path, new_audio_id, text):
    """Update TSV with new entry."""
    with open(file_path, 'a', encoding='utf-8', newline='') as file:
        writer = csv.writer(file, delimiter='\t')
        writer.writerow([new_audio_id, text])