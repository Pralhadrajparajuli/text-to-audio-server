from gtts import gTTS
import os
import nepali_roman as nr

# Simple Nepali to Romanized mapping (limited support)


def nepali_text_to_speech(text, output_file="output.mp3"):
    romanized_text = nr.romanize_text(text)
    tts = gTTS(romanized_text, lang="ne")  # Using English TTS for better pronunciation
    tts.save(output_file)
    os.system(f"open {output_file}")  # 'start' for Windows, 'xdg-open' for Linux
    return output_file

nepali_text = "मूजी मूजी मूजी मूजी मूजी मूजी मूजी मूजी मूजी मूजी मूजी मूजी मूजी मूजी मूजी मूजी मूजी मूजी मूजी मूजी मूजी मूजी मूजी मूजी मूजी मूजी मूजी मूजी मूजी मूजी मूजी मूजी मूजी मूजी मूजी मूजी मूजी मूजी मूजी मूजी मूजी मूजी मूजी मूजी मूजी मूजी मूजी मूजी मूजी मूजी मूजी मूजी मूजी मूजी मूजी मूजी मूजी मूजी मूजी मूजी मूजी मूजी मूजी मूजी मूजी मूजी मूजी मूजी मूजी मूजी मूजी मूजी मूजी मूजी मूजी मूजी मूजी मूजी मूजी मूजी मूजी मूजी मूजी मूजी मूजी मूजी मूजी मूजी मूजी मूजी मूजी मूजी मूजी मूजी मूजी मूजी मूजी मूजी मूजी मूजी मूजी मूजी मूजी मूजी मूजी मूजी मूजी मूजी मूजी मूजी मूजी मूजी मूजी मूजी मूजी मूजी मूजी मूजी मूजी मूजी मूजी मूजी मूजी मूजी मूजी मूजी मूजी मूजी  मूजी मूजी "
output = nepali_text_to_speech(nepali_text)
print(f"Audio saved as {output}")