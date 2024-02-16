import os
import requests
from dotenv import load_dotenv
load_dotenv()

API_KEY = os.getenv('PEXELS_API_KEY')


def fetch_images(query: str, number_of_images: int):
    try:
        response = requests.get("https://api.pexels.com/v1/search",
                                params={
                                    'query': query, 'orientation': 'portrait', 'per_page': number_of_images},
                                headers={'Authorization': API_KEY})
        response.raise_for_status()
        response_data = response.json()
        photos = response_data['photos']
        image_urls = [photo['url'] for photo in photos]
        return image_urls
    except Exception as error:
        print('Error fetching photos:', error)
        return


def main():
    query = 'love'
    number_of_images = 5
    image_urls = fetch_images(query, number_of_images)
    print(image_urls)

if __name__ == '__main__':
    main()
