from typing import List, Tuple
import requests
from moviepy.editor import ImageSequenceClip
from PIL import Image
import numpy as np


def get_image_from_url(image_url: str):
    res = requests.get(image_url, stream=True)
    res.raise_for_status()
    return Image.open(res.raw)


def resize_image(image: Image.Image, size: Tuple[int, int]):
    return image.resize(size=size)


def images_to_video(image_urls: List[str], video_size: Tuple[int, int], video_filepath: str, fps: float):
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


def main():
    video_title = 'video-title'
    video_filepath = f'output/{video_title}.mp4'
    video_size = (1080, 1920)
    fps = 1/4
    image_urls = ['https://images.pexels.com/photos/265722/pexels-photo-265722.jpeg', 'https://images.pexels.com/photos/704748/pexels-photo-704748.jpeg',
                  'https://images.pexels.com/photos/258421/pexels-photo-258421.jpeg', 'https://images.pexels.com/photos/1187079/pexels-photo-1187079.jpeg', 'https://images.pexels.com/photos/1024984/pexels-photo-1024984.jpeg']
    image_sequence = images_to_video(image_urls, video_filepath=video_filepath, video_size=video_size, fps=fps)
    image_sequence.write_videofile(video_filepath)


if __name__ == '__main__':
    main()
