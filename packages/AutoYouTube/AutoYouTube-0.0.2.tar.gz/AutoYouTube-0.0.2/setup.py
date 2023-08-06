from setuptools import setup, find_packages
import codecs
import os

VERSION = '0.0.2'
DESCRIPTION = 'AutoYouTube'
LONG_DESCRIPTION = 'A package to perform YouTube Sortcut Keys'

# Setting up
setup(
    name="AutoYouTube",
    version=VERSION,
    author="Suraj",
    author_email="surajdholakiya12@gmail.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=['keyboard'],
    keywords=['suraj dholakiya','AutoYoutube','youtube sortcut keys','sortcut keys'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)