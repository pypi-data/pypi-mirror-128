
__version__ = '0.1.0'

DOG_CEO_URL = "https://dog.ceo"

# All Dogs
ALL_DOGS_URL = DOG_CEO_URL + "/api/breeds/list/all"
RANDOM_DOG_IMAGE_URL = DOG_CEO_URL + "/api/breeds/image/random"

# By Breed
BREED_LIST_URL = DOG_CEO_URL + "/api/breeds/list"
ALL_BREED_IMAGES_URL = DOG_CEO_URL + "/api/breed/{}/images"
RANDOM_IMAGE_FROM_BREED_URL = DOG_CEO_URL + "/api/breed/{}/images/random"

# By Subbreed
SUBBREED_LIST_URL = DOG_CEO_URL + "/api/breed/{}/list"
ALL_SUBBREED_IMAGES_URL = DOG_CEO_URL + "/api/breed/{0}/{1}/images"
RANDOM_IMAGE_FROM_SUBBREED_URL = DOG_CEO_URL + "/api/breed/{0}/{1}/images/random"