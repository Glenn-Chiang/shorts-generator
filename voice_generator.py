import requests
import base64
from moviepy.editor import AudioFileClip


ENDPOINT = 'https://tiktok-tts.weilnet.workers.dev/api/generation'


def generate_voice(text: str):
    res = requests.post(url=ENDPOINT, json={
                        'text': text, 'voice': 'en_us_001'})
    res.raise_for_status()
    return res.json()['data']


def text_to_speech(text: str, audio_filepath: str):
    voice_code = None
    try:
        voice_code = generate_voice(text)
    except Exception as error:
        print('Error getting response from TikTok TTS API:', error)
        return
    
    voice_bytes = base64.b64decode(voice_code)
    with open(audio_filepath, 'wb') as file:
        file.write(voice_bytes)
        return AudioFileClip(audio_filepath)
        

if __name__ == '__main__':
    text = "Did you know that people who spend time looking into each other's eyes experience a chemical reaction in their brains? This reaction is linked to increased intimacy and a surge in oxytocin, known as the 'love hormone.'"
    audio_filepath = 'output/audio/voiceover.mp3'
    text_to_speech(text, audio_filepath)
