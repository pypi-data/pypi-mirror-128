import requests

from .const import *

class PyDog:
    def __init__(self, requests_session=None):
        if requests_session:
            self.session = requests_session
        else:
            self.session = requests.Session()
    
    def get_all_dogs(self):
        """ Returns a dictionary of all breeds and their subbreeds """
        with self.session.get(ALL_DOGS_URL) as r:
            if r.status_code != 200:
                raise Exception(f"{ALL_DOGS_URL} returned status code: {r.status_code}")
            return r.json()['message']
    
    def get_random_image(self, breed_name=None, sub_breed_name=None):
        """ Returns a URL of the image """
        if breed_name:
            if sub_breed_name:
                url = RANDOM_IMAGE_FROM_SUBBREED_URL.format(breed_name, sub_breed_name)
            else:
                url = RANDOM_IMAGE_FROM_BREED_URL.format(breed_name)
        elif sub_breed_name:
            raise Exception('Cannot give a sub_breed_name if breed_name is left empty.')
        else:
            url = RANDOM_DOG_IMAGE_URL
        
        with self.session.get(url) as r:
            if r.status_code != 200:
                if breed_name and sub_breed_name:
                    raise Exception(f'Random Image for {breed_name}/{sub_breed_name} returned status code: {r.status_code}')
                elif breed_name:
                    raise Exception(f'Random Image for {breed_name} returned status code: {r.status_code}')
                else:
                    raise Exception(f'Random Dog Image returned status code: {r.status_code}')
            return r.json()['message']
    
    def get_all_breeds(self):
        with self.session.get(BREED_LIST_URL) as r:
            if r.status_code != 200:
                raise Exception(f'{BREED_LIST_URL} returned status code: {r.status_code}')
            return r.json()['message']
    
    def get_breed_images(self, breed_name):
        with self.session.get(ALL_BREED_IMAGES_URL.format(breed_name)) as r:
            if r.status_code != 200:
                raise Exception(f'{ALL_BREED_IMAGES_URL.format(breed_name)} returned status code: {r.status_code}')
            return r.json()['message']

    def get_all_subbreeds(self, breed_name):
        with self.session.get(SUBBREED_LIST_URL.format(breed_name)) as r:
            if r.status_code != 200:
                raise Exception(f'{SUBBREED_LIST_URL.format(breed_name)} returned status code: {r.status_code}')
            return r.json()['message']

    def get_subbreed_image(self, breed_name, sub_breed_name):
        with self.session.get(ALL_SUBBREED_IMAGES_URL.format(breed_name, sub_breed_name)) as r:
            if r.status_code != 200:
                raise Exception(f'{ALL_SUBBREED_IMAGES_URL.format(breed_name, sub_breed_name)} returned status code: {r.status_code}')
            return r.json()['message']
        