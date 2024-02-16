import sys
from script_generator import generate_script
from image_fetcher import fetch_images
from video_maker import images_to_video

def main():  
    script = generate_script()

    if not script:
        print("Error generating script")
        sys.exit()

    video_title = script['title']
    video_script = script['content']
    print(video_script)

    # TODO: Generate voice-over narration using text-to-speech

    number_of_images_required = 5 # TODO: Compute number of images required to fit voiceover duration, given that each image is displayed for x seconds
    images_query = "" # TODO: Generate search terms based on video script
    image_urls = fetch_images(query=images_query, number_of_images=number_of_images_required)
    
    video_title = 'video-title'
    video_filepath = f'output/{video_title}.mp4'
    video_size = (1080, 1920)
    fps = 1/4

    image_sequence = images_to_video(image_urls=image_urls, video_filepath=video_filepath, video_size=video_size, fps=fps)
    

if __name__ == '__main__':
    main()