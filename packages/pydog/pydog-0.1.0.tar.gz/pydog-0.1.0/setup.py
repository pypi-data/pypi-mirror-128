
import re

from os import path
from setuptools import setup, find_packages

PACKAGE_NAME = 'pydog'
HERE = path.abspath(path.dirname(__file__))

with open(path.join(HERE, PACKAGE_NAME, 'const.py')) as f:
    VERSION = re.findall("__version__ = '([^']+)'", f.read())[0]


setup(
    name=PACKAGE_NAME,
    version=VERSION,
    author='Daniel Ahn',
    author_email='firefwing42@gmail.com',
    description="A Simple Python API Wrapper for https://dog.ceo.",
    install_requires=['requests'],
    packages=find_packages(exclude=['tests', 'tests.*'])
)
