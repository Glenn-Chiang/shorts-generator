import random
from typing import List
import os
import requests
from dotenv import load_dotenv
load_dotenv()

API_KEY = os.getenv('PEXELS_API_KEY')


def split_number(num: int, parts: int) -> List[int]:
    quotient = num // parts
    remainder = num % parts
    return [quotient + 1] * remainder + [quotient] * (parts - remainder)


def fetch_images(search_terms: List[str], number_of_images: int):
    image_urls = []
    # Determine the number of images to fetch for each search term
    # The split_number() function tries to balance the distribution as much as possible
    images_per_term = split_number(number_of_images, parts=len(search_terms))

    for index, search_term in enumerate(search_terms):
        print("Fetching images for:", f"'{search_term}'")
        try:
            response = requests.get("https://api.pexels.com/v1/search",
                                    params={
                                        'query': search_term, 'orientation': 'portrait', 'per_page': images_per_term[index]},
                                    headers={'Authorization': API_KEY})
            response.raise_for_status()
            response_data = response.json()
            photos = response_data['photos']
        except requests.exceptions.RequestException as error:
            print('Error fetching photos:', error)
            continue

        image_urls.extend([photo['src']['original'] for photo in photos])

    random.shuffle(image_urls)
    return image_urls


def main():
    query = 'heart'
    number_of_images = 5
    image_urls = fetch_images(query, number_of_images)
    print(image_urls)


if __name__ == '__main__':
    main()
