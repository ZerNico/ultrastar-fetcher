import codecs
import errno
import os
import pathlib
import re
import urllib.parse

import musicbrainzngs
from chardet import UniversalDetector
from yt_dlp import YoutubeDL

detector = UniversalDetector()
video_pattern = re.compile(r'(#VIDEO:).*', re.IGNORECASE)
audio_pattern = re.compile(r'(#MP3:).*', re.IGNORECASE)
cover_pattern = re.compile(r'(#COVER:).*', re.IGNORECASE)
avi_pattern = re.compile(r'(.*)(\.avi|\.divx|\.flv|\.mkv)', re.IGNORECASE)

musicbrainzngs.set_useragent("UltraStar Fetch", "0.1", "https://zernico.de")


def create_dir(path):
    if not os.path.exists(path):
        try:
            os.makedirs(path)
        except OSError as exc:
            if exc.errno != errno.EEXIST:
                raise


def convert_txt(in_path, out_path, file_name):
    detector.reset()
    for line in open(in_path, 'rb'):
        detector.feed(line)
        if detector.done: break
    detector.close()

    encoding = detector.result.get('encoding')

    with codecs.open(in_path, 'r', encoding) as original_file:
        original_content = original_file.read()

    # detect line break style in content
    if '\r\n' in original_content:
        line_break = '\r\n'
    else:
        line_break = '\n'

    video_tag = video_pattern.search(original_content)
    if video_tag is None:
        original_content = '#VIDEO:' + file_name + '.webm' + line_break + original_content
    new_content = re.sub(video_pattern, r'\1' + file_name + '.webm', original_content)

    audio_tag = audio_pattern.search(new_content)
    if audio_tag is None:
        new_content = '#MP3:' + file_name + '.mp3' + line_break + new_content
    new_content = re.sub(audio_pattern, r'\1' + file_name + '.mp3', new_content)

    cover_tag = cover_pattern.search(new_content)
    if cover_tag is None:
        new_content = '#COVER:Jonas Blue feat. JP Cooper - Perfect Strangers.jpg' + line_break + new_content
    new_content = re.sub(cover_pattern, r'\1' + file_name + '.jpg', new_content)

    with codecs.open(out_path, 'w+', "UTF-8") as new_file:
        new_file.write(new_content)


def fetch(input_path, youtube_url):
    path = pathlib.Path(input_path).parent.resolve()
    file_name = pathlib.Path(input_path).stem
    out_path = os.path.join(path, file_name)
    create_dir(out_path)

    artist, title = file_name.split(' - ')

    convert_txt(input_path, os.path.join(out_path, file_name + ".txt"), file_name)

    ydl_vid_opts = {
        'format': 'bestvideo[height<=1080]',
        'outtmpl': os.path.join(out_path, file_name) + '.%(ext)s',
        "quiet": True,
    }
    with YoutubeDL(ydl_vid_opts) as ydl:
        ydl.download([youtube_url])

    ydl_audio_opts = {
        'format': 'm4a/bestaudio/best',
        'outtmpl': os.path.join(out_path, file_name) + '.%(ext)s',
        "quiet": True,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '256',
        }]
    }

    with YoutubeDL(ydl_audio_opts) as ydl:
        ydl.download([youtube_url])

    try:
        result = musicbrainzngs.search_releases(release=title, artist=artist, limit=1)

        image_data = musicbrainzngs.get_image(mbid=result['release-list'][0]['id'], coverid="front", size="500",
                                              entitytype="release")
        # write image data to file
        with open(os.path.join(out_path, file_name + '.jpg'), 'wb') as f:
            f.write(image_data)
    except musicbrainzngs.musicbrainz.ResponseError:
        print()
        print("Failed to fetch cover image for: " + file_name)

        print("Search it yourself, for example on https://www.google.com/search?tbm=isch&q=" + urllib.parse.quote(
            artist) + "%20" + urllib.parse.quote(title) + "%20cover%20art")
        print("Name it (if it's a png you have to edit the txt):")
        print(file_name + '.jpg')
