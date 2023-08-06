import os

from setuptools import setup
from setuptools import find_packages


with open(os.path.join(os.path.dirname(__file__), "twitlim", "VERSION")) as file:
    VERSION = file.read().strip()


REQUIREMENTS = [
    "Click>=8.0,<=8.999",
    "tweepy>=4.0.1,<4.0.999",
    "click-option-group>=0.5.3,<0.6.0",
]

setup(
    author="RMNL",
    author_email="pypi@rmnl.net",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Environment :: Console",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX",
        "Programming Language :: Python :: 3 :: Only",
    ],
    description="Simple CLI tool to help delete Tweets.",
    entry_points={"console_scripts": ["twitlim = twitlim.twitlim:twitlim"]},
    include_package_data=True,
    install_requires=REQUIREMENTS,
    name="twitlim",
    packages=find_packages(),
    url="https://gitlab.com/rmnl/twitlim",
    version=VERSION,
    zip_safe=False,
)
