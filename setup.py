import pathlib

from setuptools import setup, find_packages

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

setup(
    name="usfetch",
    description="A Python CLI UltraStar Song fetcher to download mp3 / video files from youtube",
    long_description=README,
    long_description_content_type="text/markdown",
    version="0.1",
    author_email="nico.franke01@gmail.com",
    author_name="Nico Franke",
    license="MIT",
    url="https://github.com/ZerNico/ultrastar-fetcher",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "tqdm==4.64.0",
        "chardet==3.0.4",
        "ffmpeg-python==0.2.0",
        "yt-dlp==2022.5.18",
        "musicbrainzngs==0.7.1",
    ],
    entry_points={
        "console_scripts": [
            "usfetch = usfetch.cli:cli"
        ]
    },
)