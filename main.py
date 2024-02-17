import sys
from script_generator import generate_script
from image_fetcher import fetch_images
from video_maker import images_to_video
from voice_generator import text_to_speech
from subtitle_generator import generate_subtitles, burn_subtitles_into_video
import math
from uuid import uuid4


def main():
    video_size = (1080, 1920)
    seconds_per_image = 4
    video_id = uuid4()
    audio_filepath = f'output/audio/{video_id}.mp3'
    video_filepath = f'output/video/{video_id}.mp4'
    subtitles_filepath = f'output/subtitles/{video_id}.srt'
    final_output_filepath = f'output/final/{video_id}.mp4'

    print('Generating script...')
    try:
        script = generate_script()
        video_title: str = script['title']
        video_script: str = script['content']
        keywords = script['keywords']
        print(video_title)
        print(video_script)
        print(keywords)

    except Exception as error:
        print("Error generating script:", error)
        sys.exit()


    # Generate voice-over narration using text-to-speech
    print("Generating voice-over narration...")
    audio = text_to_speech(text=video_script, audio_filepath=audio_filepath)
    # Compute number of images required to fit voiceover duration, given that each image is displayed for x seconds
    number_of_images_required: int = math.ceil(audio.duration / seconds_per_image)
    
    # Generate search terms based on video script
    images_query = keywords[0]

    print("Fetching images...")
    image_urls = fetch_images(
        query=images_query, number_of_images=number_of_images_required)

    if not image_urls:
        print('No images found')
        sys.exit()

    print("Compiling images to video...")
    video = images_to_video(
        image_urls=image_urls, video_size=video_size, fps=1/seconds_per_image)
    video.write_videofile(video_filepath)

    # Generate subtitles based on audio file
    print("Generating subtitles...")
    subtitles = generate_subtitles(audio_filepath, subtitles_filepath)    

    # Burn subtitles into video
    print("Burning subtitles...")
    subtitled_video = burn_subtitles_into_video(video_filepath=video_filepath, subtitles_filepath=subtitles_filepath)    

    audio = audio.subclip(0, audio.duration - 0.05) # For some reason we need to clip the audio at tne end to avoid a weird audio glitch at the end
    final_video = subtitled_video.set_audio(audio)
    final_video.write_videofile(final_output_filepath, fps=30)


if __name__ == '__main__':
    main()



