import csv
from fuzzywuzzy import process
import numpy as np
import os
from scipy.io.wavfile import read
import noisereduce as nr
from scipy.signal import butter, filtfilt
from pydub import AudioSegment
from pydub.effects import compress_dynamic_range


AudioSegment.ffmpeg = "/usr/local/bin/ffmpeg"
AudioSegment.ffprobe = "/usr/local/bin/ffprobe"


def apply_noise_reduction(audio_data, sample_rate):
    """Apply noise reduction to the audio."""
    reduced_audio = nr.reduce_noise(y=audio_data, sr=sample_rate)
    return reduced_audio

def high_pass_filter(audio_data, sample_rate, cutoff=1000):
    """Apply high-pass filter to remove low-frequency noise."""
    nyquist = 0.5 * sample_rate
    normal_cutoff = cutoff / nyquist
    b, a = butter(1, normal_cutoff, btype='high', analog=False)
    return filtfilt(b, a, audio_data)

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
    # Convert AudioSegment to numpy array
    if isinstance(audio, AudioSegment):
        audio = np.array(audio.get_array_of_samples())

    # Now perform the operation
    trimmed_audio = audio[np.abs(audio) > threshold]
    return np.concatenate((trimmed_audio, np.zeros(int(0.01 * sample_rate))))  # Add slight padding

def match_syllable(syllable, syllable_mapping):
    """Match syllable and check for variations like ौ vs. ाै."""
    # First try the exact match
    if syllable in syllable_mapping:
        return syllable_mapping[syllable]
    
    # Check for specific variations
    variations = {
        'ौ': 'ाै',  # Handle alternate variations of syllables
    }

    if syllable in variations:
        alternative_syllable = variations[syllable]
        if alternative_syllable in syllable_mapping:
            return syllable_mapping[alternative_syllable]

    # Return None if no match is found
    return None

def split_into_syllables(text, syllable_mapping):
    """Split text into syllables and map to audio IDs."""
    print(f"Original text: {text}")
    syllables = []
    current_syllable = ""

    # Nepali vowel signs and modifiers
    vowels = ['ो', 'ा', 'ी', 'ु', 'े', 'ै', 'ि', 'ं', 'ँ']
    consonants = ['क', 'ख', 'ग', 'घ', 'च', 'छ', 'ज', 'झ', 'ट', 'ठ', 'ड', 'ढ', 'त', 'थ', 'द', 'ध', 'न', 'प', 'फ', 'ब', 'भ', 'म', 'य', 'र', 'ल', 'व', 'श', 'ष', 'स', 'ह', 'ळ', 'क्ष', 'ज्ञ']
    special_combination_chars = ['ृ']  # Characters like 'ृ' that need special handling

    i = 0  # Index to track position in the word
    while i < len(text):
        char = text[i]

        # Check if the previous character is 'ं' and the current one is a consonant like 'र'
        if char == 'ं' and i > 0 and text[i-1] in consonants:
            # Combine previous syllable with 'न्'
            current_syllable = text[i-1] + 'न्'
            syllables.append(syllable_mapping.get(current_syllable))  # Add the combined syllable
            i += 1  # Skip the current 'ं' character
            continue

        # If the character is a vowel or diacritic, append it to the current syllable
        elif char in vowels:
            current_syllable += char
            i += 1
        elif char == '्':  # Handling '्' (virama) as part of the previous syllable
            current_syllable += char
            i += 1
        elif char in special_combination_chars:
            # Special handling for 'ृ' to combine the previous syllable with 'रि'
            if current_syllable:
                combined_syllable = current_syllable[:-1] + "्" + "रि"  # Combine consonant and 'रि'
                syllables.append(syllable_mapping.get(combined_syllable))  # Add the combined syllable
            current_syllable = ''  # Reset current syllable after combining
            i += 1
        else:
            # When a new character is encountered, check if the current syllable has a valid mapping
            if current_syllable:
                mapped_syllable = match_syllable(current_syllable, syllable_mapping)  # Use match_syllable for variations
                if mapped_syllable:
                    syllables.append(mapped_syllable)
                else:
                    print(f"No match found for syllable: {current_syllable}")
            current_syllable = char
            i += 1

    # After the loop, check if the last syllable has a valid mapping
    if current_syllable:
        mapped_syllable = match_syllable(current_syllable, syllable_mapping)  # Use match_syllable for variations
        if mapped_syllable:
            syllables.append(mapped_syllable)
        else:
            print(f"No match found for syllable: {current_syllable}")

    print(f"Split syllables (audio IDs): {syllables}")
    return syllables

def get_audio_file_path(audio_dir, audio_id):
    """Returns the path to an audio file, checking for both .wav and .mp3 formats."""
    if audio_id is None:
        print("Warning: Received None as audio_id.")
        return None

    # Check for the direct syllable first
    wav_file_path = os.path.join(audio_dir, f"{audio_id}.wav")
    mp3_file_path = os.path.join(audio_dir, f"{audio_id}.mp3")

    # If the exact audio file is not found, attempt combining syllables for complex cases
    if not os.path.exists(wav_file_path) and not os.path.exists(mp3_file_path):
        # Handle complex syllables with 'ृ' like 'कृ' -> 'क्' + 'रि'
        if 'ृ' in audio_id:  # If the syllable contains 'ृ'
            base_consonant = audio_id[:-1]  # Remove 'ृ' (for example, 'क' from 'कृ')
            combined_audio_id = base_consonant + '्' + 'रि'  # Combine with 'रि'
            wav_file_path = os.path.join(audio_dir, f"{combined_audio_id}.wav")
            mp3_file_path = os.path.join(audio_dir, f"{combined_audio_id}.mp3")
        
        if not os.path.exists(wav_file_path) and not os.path.exists(mp3_file_path):
            # Handle complex syllables with 'ं' like 'कं' -> 'क' + '्' + 'न'
            if 'ं' in audio_id:  # If the syllable contains 'ं'
                base_consonant = audio_id[:-1]
                combined_audio_id = base_consonant + 'न्'
                wav_file_path = os.path.join(audio_dir, f"{combined_audio_id}.wav")
                mp3_file_path = os.path.join(audio_dir, f"{combined_audio_id}.mp3")


    # If the audio file exists, return the path
    if os.path.exists(wav_file_path):
        return wav_file_path
    elif os.path.exists(mp3_file_path):
        return mp3_file_path
    return None


def combine_syllables_to_word(syllables, audio_dir):
    """Combine syllables' audio into a single audio clip that sounds like a word."""
    word_audio = []

    for audio_id in syllables:
        audio_file_path = get_audio_file_path(audio_dir, audio_id)
        if audio_file_path:
            print(f"Found audio file for syllable: {audio_file_path}")
            if audio_file_path.endswith('.mp3'):
                # Handle .mp3 file using pydub
                audio_data = AudioSegment.from_mp3(audio_file_path)
                sample_rate = audio_data.frame_rate  # Get the frame rate before converting to numpy
            else:
                # Handle .wav file using scipy
                sample_rate, audio_data = read(audio_file_path)  # Read both sample rate and audio data

            trimmed_audio = trim_silence(audio_data, sample_rate)
            word_audio.append(trimmed_audio)
        else:
            print(f"Audio file not found: {audio_file_path}")

    # Combine the syllables into a single word audio, ensuring smooth transition between syllables
    if word_audio:
        combined_word_audio = np.concatenate(word_audio)

        # Make sure the transition between syllables is quick by removing any silence padding between them


        combined_word_audio = apply_noise_reduction(combined_word_audio, sample_rate)
        # combined_word_audio = high_pass_filter(combined_word_audio, sample_rate)

        return combined_word_audio, sample_rate
    return None, None

def generate_combined_audio_for_words(text, syllable_mapping, audio_dir):
    """Generate combined audio for text by combining syllables into words."""
    audio_clips = []
    words = text.split()  # Split the text into words

    for word in words:
        syllables = split_into_syllables(word, syllable_mapping)  # Split the word into syllables
        word_audio, sample_rate = combine_syllables_to_word(syllables, audio_dir)  # Combine syllables into word audio
        
        if word_audio is not None:
            audio_clips.append(word_audio)
        else:
            print(f"Could not generate audio for word: {word}")

    # Combine all words into a single audio
    if audio_clips:
        padding_length = 7000  # Adjust this based on your needs

        # Apply padding between clips
        audio_clips_with_padding = []
        for i, clip in enumerate(audio_clips):
            audio_clips_with_padding.append(clip)
            # Add padding after each clip except the last one
            if i < len(audio_clips) - 1:
                audio_clips_with_padding.append(np.zeros(padding_length))  # Add padding

        # Concatenate the clips with padding
        combined_audio = np.concatenate(audio_clips_with_padding)
        # combined_audio = apply_noise_reduction(combined_audio, sample_rate)
        combined_audio = high_pass_filter(combined_audio, sample_rate)

        return sample_rate, combined_audio
    
    return None, None

def update_tsv(file_path, new_audio_id, text):
    """Update TSV with new entry."""
    with open(file_path, 'a', encoding='utf-8', newline='') as file:
        writer = csv.writer(file, delimiter='\t')
        writer.writerow([new_audio_id, text])