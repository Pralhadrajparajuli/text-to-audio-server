

import csv
from fuzzywuzzy import process


def load_tsv(file_path):
    data = {}
    with open(file_path, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file, delimiter='\t')
        for row in reader:
            audio_id = row['audio_id']
            sentence = row['sentence']
            data[audio_id] = sentence
    return data

# Exact match: Find the corresponding audio_id based on the exact sentence
def find_best_match(text, audio_data):
    for audio_id, sentence in audio_data.items():
        if sentence.strip() == text.strip():  # Exact match
            return audio_id
    return None


# Fuzzy match: Find the closest matching sentence based on fuzzywuzzy
def find_best_match_fuzzy(text, audio_data):
    sentences = list(audio_data.values())
    best_match = process.extractOne(text, sentences)
    if best_match and best_match[1] > 80:  # Confidence threshold of 80%
        matching_sentence = best_match[0]
        audio_id = [key for key, value in audio_data.items() if value == matching_sentence][0]
        return audio_id
    return None