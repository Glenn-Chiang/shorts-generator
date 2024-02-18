from moviepy.editor import CompositeVideoClip, TextClip, VideoFileClip
from moviepy.video.tools.subtitles import SubtitlesClip
import assemblyai as aai
import os
from dotenv import load_dotenv
load_dotenv()


ASSEMBLY_AI_API_KEY = os.getenv('ASSEMBLY_AI_API_KEY')


def generate_subtitles(audio_filepath: str, subtitles_filepath: str):
    try:
        aai.settings.api_key = ASSEMBLY_AI_API_KEY
        transciber = aai.Transcriber()
        transcript = transciber.transcribe(audio_filepath)
        # print(transcript.text)
        subtitles = transcript.export_subtitles_srt(chars_per_caption=30)

        with open(subtitles_filepath, 'w') as file:
            file.write(subtitles)

        return subtitles
    except Exception as error:
        print("Error generating subtitles:", error)


if __name__ == '__main__':
    audio_filepath = 'output/audio/voiceover.mp3'
    subtitles_filepath = 'output/subtitles/subtitles.srt'
    video_filepath = 'output/video/video.mp4'
    final_output_filepath = 'output/final/final.mp4'

    print(TextClip.list('font'))
    print(TextClip.list('color'))
    # subtitled_video = burn_subtitles_into_video(video_filepath=video_filepath, subtitles_filepath=subtitles_filepath)
    # subtitled_video.write_videofile(filename=final_output_filepath, fps=30)
