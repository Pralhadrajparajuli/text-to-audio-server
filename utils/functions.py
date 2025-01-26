import csv
from fuzzywuzzy import process
import numpy as np
import os
from scipy.io.wavfile import read

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
    syllable = ""
    for char in text:
        syllable += char
        if char in ['ो', 'ा', 'ी', 'ु', 'े', 'ै', 'ि', 'ं', 'ँ']:  # Nepali vowels
            best_match = find_best_match_fuzzy(syllable, syllable_mapping)
            if best_match:
                syllables.append(best_match)  # Append matched audio_id
            else:
                print(f"No match found for syllable: {syllable}")
            syllable = ""  # Reset for the next syllable

    # Handle any remaining syllable
    if syllable:
        best_match = find_best_match_fuzzy(syllable, syllable_mapping)
        if best_match:
            syllables.append(best_match)
        else:
            print(f"No match found for syllable: {syllable}")
    
    print(f"Split syllables (audio IDs): {syllables}")
    return syllables

def generate_combined_audio(text, syllable_mapping, audio_dir):
    """Generate combined audio for text."""
    
    audio_clips = []
    syllables = split_into_syllables(text, syllable_mapping)

    for audio_id in syllables:
        audio_file_path = os.path.join(audio_dir, f"{audio_id}.wav")
        print(f"Found audio file for full text: {audio_file_path}")

        if os.path.exists(audio_file_path):
            print(f"Found audio file: {audio_file_path}")
            sample_rate, audio_data = read(audio_file_path)
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