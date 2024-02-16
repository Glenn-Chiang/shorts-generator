import sys
from script_generator import generate_script
from image_fetcher import fetch_images
from video_maker import images_to_video
from voice_generator import text_to_speech

def main():
    video_size = (1080, 1920)
    fps = 1/4

    print('Generating script...')
    script = generate_script()

    if not script:
        print("Error generating script")
        sys.exit()

    video_title: str = script['title']
    video_script: str = script['content']
    keywords = script['keywords']
    print(video_title)
    print(video_script)
    print(keywords)

    # Generate voice-over narration using text-to-speech
    print("Generating voice-over narration...")
    audio = text_to_speech(text=video_script, audio_filepath='output/audio/voiceover.mp3')

    # Compute number of images required to fit voiceover duration, given that each image is displayed for x seconds
    number_of_images_required = audio.duration * fps
    
    # Generate search terms based on video script
    images_query = (' ').join(keywords)

    print("Fetching images...")
    image_urls = fetch_images(
        query=images_query, number_of_images=number_of_images_required)


    def title_to_filename(title: str):
        return '-'.join(video_title.split(' ')).strip('?')
    
    video_filepath = f"output/{title_to_filename(video_title)}.mp4"
    print("Compiling images to video...")
    video = images_to_video(
        image_urls=image_urls, video_size=video_size, fps=fps)
    video.write_videofile(video_filepath)

    video_with_audio = video.set_audio(audio)
    

if __name__ == '__main__':
    main()
