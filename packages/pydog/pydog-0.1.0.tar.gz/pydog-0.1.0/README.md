# PyDog
Python API Wrapper for https://dog.ceo/dog-api/

# Usage
```Python
import pydog

dog = pydog.PyDog()
dog.get_all_dogs()
dog.get_all_breeds()
dog.get_all_subbreeds('spaniel')

dog.get_breed_images('affenpinscher')
dog.get_subbreed_image('spaniel', 'japanese')

dog.get_random_image()
dog.get_random_image(breed_name='affenpinscher')
dog.get_random_image(breed_name='spaniel', sub_breed_name='japanese')

```

# Installation
```
pip install -U git+"https://github.com/xNinjaKittyx/pydog.git"
```
