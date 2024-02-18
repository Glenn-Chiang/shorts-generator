from typing import List, Tuple
import requests
from PIL import Image
import numpy as np
from moviepy.editor import CompositeVideoClip, TextClip, VideoFileClip, ImageSequenceClip
from moviepy.video.tools.subtitles import SubtitlesClip


def get_image_from_url(image_url: str):
    res = requests.get(image_url, stream=True)
    res.raise_for_status()
    return Image.open(res.raw)


def resize_image(image: Image.Image, size: Tuple[int, int]):
    return image.resize(size=size)


def images_to_video(image_urls: List[str], video_size: Tuple[int, int], fps: float):
    images = []
    for image_url in image_urls:
        try:
            image = get_image_from_url(image_url)
            images.append(image)
        except Exception as error:
            print(f"Error getting image from url: {image_url}")

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


def main():
    video_filepath = r'output\video\c8825c83-7019-4972-b2d0-0b07e64f909a.mp4'
    subtitles_filepath = r'output\subtitles\c8825c83-7019-4972-b2d0-0b07e64f909a.srt'
    final = burn_subtitles_into_video(
        video_filepath=video_filepath, subtitles_filepath=subtitles_filepath)
    final.write_videofile(
        r'output\final\c8825c83-7019-4972-b2d0-0b07e64f909a.mp4')


if __name__ == '__main__':
    main()
