from dotenv import load_dotenv
load_dotenv()
import os
import assemblyai as aai

ASSEMBLY_AI_API_KEY = os.getenv('ASSEMBLY_AI_API_KEY')

def generate_subtitles(audio_filepath: str, subtitles_filepath: str):
    try: 
        aai.settings.api_key = ASSEMBLY_AI_API_KEY
        transciber = aai.Transcriber()
        transcript = transciber.transcribe(audio_filepath)
        subtitles = transcript.export_subtitles_srt()

        with open(subtitles_filepath, 'w') as file:
            file.write(subtitles)

        return subtitles
    except Exception as error:
        print("Error generating subtitles:", error)
        

if __name__ == '__main__':
    audio_filepath = 'output/audio/voiceover.mp3'
    subtitles_filepath = 'output/subtitles/subtitles.srt'
    subtitles = generate_subtitles(audio_filepath, subtitles_filepath)
