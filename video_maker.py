from typing import List, Tuple
import os
import random
import numpy as np
import requests
from moviepy.editor import (CompositeVideoClip, ImageSequenceClip, TextClip,
                            VideoFileClip, clips_array)
from moviepy.video.tools.subtitles import SubtitlesClip
from PIL import Image


def get_image_from_url(image_url: str):
    res = requests.get(image_url, stream=True)
    res.raise_for_status()
    return Image.open(res.raw)


def resize_image(image: Image.Image, size: Tuple[int, int]):
    return image.resize(size=size)


def images_to_video(image_urls: List[str], video_size: Tuple[int, int], fps: float = 1/4):
    images = []
    for image_url in image_urls:
        try:
            image = get_image_from_url(image_url)
            images.append(image)
        except Exception as error:
            print(f"Error getting image from url: {image_url}", error)

    images = [resize_image(image, video_size) for image in images]
    # for index, image in enumerate(images):
    #     image.save(f'images/{index}.png')
    np_images = [np.asarray(image) for image in images]
    image_sequence = ImageSequenceClip(np_images, fps=fps)
    return image_sequence


def burn_subtitles_into_video(video_filepath: str, subtitles_filepath: str):
    video = VideoFileClip(video_filepath)

    def generator(text): return TextClip(txt=text, font='Segoe-UI-Bold', fontsize=100,
                                         color='white', stroke_color='black', stroke_width=5,
                                         method='caption', align='center', size=video.size)

    subtitles = SubtitlesClip(subtitles_filepath, generator)
    subtitled_video = CompositeVideoClip(
        [video, subtitles.set_position(('center', 'center'))])
    return subtitled_video


def get_random_clip(audio_duration: int):
    # Randomly select a video from assets
    saved_videos = os.listdir('assets')
    random_video_path = f'assets/{random.choice(saved_videos)}'
    video = VideoFileClip(random_video_path)
    video_duration = int(video.duration)
    # If audio duration is longer than full video duration, just clip the full video
    if (audio_duration > video_duration):
        return video

    # Randomly extract a clip from the video that matches the audio duration
    clip_start = random.randint(0, video_duration - audio_duration)
    clip: VideoFileClip = video.subclip(clip_start, clip_start + audio_duration)
    return clip


def create_video(image_urls: List[str], audio_duration: int, video_size: Tuple[int, int], video_filepath: str):
    # Video containing relevant stock images
    images_video = images_to_video(
        image_urls=image_urls, video_size=video_size)
    # Random dopamine-stimulating video
    random_video = get_random_clip(audio_duration=audio_duration)
    # Combines videos
    combined_video = clips_array([[random_video], [images_video]])
    combined_video.subclip(0, audio_duration)
    combined_video.write_videofile(video_filepath)
    return combined_video

def combine_videos():
    ...

def main():
    video_filepath = r'output\video\c8825c83-7019-4972-b2d0-0b07e64f909a.mp4'
    subtitles_filepath = r'output\subtitles\c8825c83-7019-4972-b2d0-0b07e64f909a.srt'
    video = get_random_clip(10)
    video.write_videofile('output/video/test_clip.mp4')

if __name__ == '__main__':
    main()
