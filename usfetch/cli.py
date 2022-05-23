import argparse
import os
import subprocess
import sys

from usoptimize.fetch import fetch


def cli():
    parser = argparse.ArgumentParser(
        description='A Python CLI UltraStar Song Converter to optimize song files for the web.')
    parser.add_argument('-i', '--input', metavar='<path of song file>', type=str, nargs=1, required=True,
                        help='Filepath of song file')
    parser.add_argument('-u', '--url', metavar='<youtube url>', type=str, nargs=1,
                        help='Use this youtube video')

    args = parser.parse_args()
    input_path = args.input[0]

    if args.url is None:
        youtube_url = None
    else:
        youtube_url = args.url[0]

    if not os.path.exists(input_path):
        print('The path specified does not exist')
        sys.exit()

    fetch(input_path, youtube_url)
