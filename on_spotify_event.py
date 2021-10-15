#!/usr/bin/env python3

from tendo import singleton
import os
import sys
import argparse
import urllib.request
import random
import time
from spotipy import Spotify
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth
from subprocess import run, CalledProcessError, DEVNULL
import shutil
import tempfile
from pathlib import Path
import requests
import json
import logging
from contextlib import contextmanager
from dotenv import load_dotenv

load_dotenv()

REFRESH_TOKEN = os.environ['REFRESH_TOKEN']
CLIENT_ID = os.environ['CLIENT_ID']
CLIENT_SECRET = os.environ['CLIENT_SECRET']

CACHE_DIR = Path('/home/pi/.cache/soundserver-album-art')
NOW_PLAYING = Path('/home/pi/.now_playing')
LAST_EVENT = Path('/home/pi/.last_event')

def handle_events():
    event = os.getenv('PLAYER_EVENT')
    track_id = os.getenv('TRACK_ID')

    with open(LAST_EVENT, 'w') as f:
        f.write(str(int(time.time())))

    if not track_id:
        return

    logger.info(track_id)

    last_id = None
    try:
        with open(NOW_PLAYING, 'r') as f:
            last_id = f.readline().strip()
    except FileNotFoundError:
        pass

    if last_id and last_id == track_id:
        return

    auth_manager = SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
    sp = Spotify(auth_manager=auth_manager)

    data = sp.track(track_id)
    name = data['name']
    artist = data['artists'][0]['name']
    album = data['album']['name']
    album_id = data['album']['id']
    art_url = data['album']['images'][0]['url']

    logger.info(f'Now playing: {name} - {artist}')

    with open(NOW_PLAYING, 'w') as f:
        f.write(track_id + '\n')
        f.write(name + '\n')
        f.write(artist + '\n')
        f.write(album + '\n')

    logger.info(f'Changing wallpaper to album {album} ({album_id})')
    change_wallpaper(album_id, art_url)

def change_wallpaper(album_id, art_url):

    CACHE_DIR.mkdir(exist_ok=True)
    art_path = CACHE_DIR / album_id
    download_attempts = 0
    while download_attempts < 2:
        if not art_path.is_file():
            # download album art if it's not in our cache
            logger.debug(f'Downloading album art...')
            urllib.request.urlretrieve(art_url, art_path.resolve())

        try:
            # set color theme
            run([f'/home/pi/.local/bin/wal', '-stenqi', art_path.resolve()], check=True)

            # set as wallpaper
            run(['hsetroot', '-extend', art_path.resolve()], check=True)
        except CalledProcessError:
            # delete and redownload
            if art_path.is_file():
                art_path.unlink()
            download_attempts -= 1
        else:
            break

    # reload cava (wal changes its config file)
    run(['pkill', '-USR1', 'cava'])

if __name__ == '__main__':
    singleton.SingleInstance() # will sys.exit(-1) if other instance is running

    logging.basicConfig(stream=sys.stdout, level=logging.INFO)
    logger = logging.getLogger(Path(__file__).stem)

    if not os.getenv('DISPLAY'):
        os.environ['DISPLAY'] = ':0'
    
    run(['killall', __file__], stdout=DEVNULL, stderr=DEVNULL)
    try:
        handle_events()
    except Exception as e:
        logger.exception(e)
