#!/usr/bin/env python3
import sys
import re
from pygame import mixer
from urllib.parse import urlparse
import os
import requests

BACKEND_URL = "http://localhost:5000" # TODO: change this to the backend url

def play_sound(sound_url, cached_sound_path: None | str=None) -> None:
    '''
    Play sound from url, if cached_sound_path is provided it will be used to cache the sound

    Args:
        sound_url (str): url to sound file
        cached_sound_path (None | str, optional): path to cache the sound file. Defaults to None.

    Returns:
        None
    '''
    if cached_sound_path is None:
        parsed_url = urlparse(sound_url)
        cached_sound_path = os.path.join(os.getcwd(), os.path.basename(parsed_url.path))

    if not os.path.exists(cached_sound_path):
        print("Downloading sound...")
        r = requests.get(sound_url, allow_redirects=True)
        open(cached_sound_path, 'wb').write(r.content)
        print("Sound downloaded")

    print("Playing sound...")
    mixer = mixer.init()
    mixer.music.load(cached_sound_path)
    mixer.music.play()

def read_rfid() -> tuple[str, str] | None:
    '''
    Read RFID from RFID reader
    We use EH301 RFID reader which simulate keyboard input (with newline)
    
    to configure it properly you would like to use the following command:
    1. we will use format number 2 (3 digits FC,5 digits ID) which looks like this:
        '20440876 ( FC=204 ID=40876) /WG26 format'
    2. we will use 'Enter' as a suffix
    3. Enable buzzer sound (optional - we have a speaker too so we don't really need it)
    4. Disable HID raw
    5. No reverse data (Regular)
    6. Keyboard Layout - USA
    7. Advanced settings - user prefix and suffix (for data integrity):
        ABC ... XYZ


    to read more about configuring this device you can follow this:
    https://download.wezhan.cn/contents/sitefiles2041/10205132/files/473369..pdf?response-content-disposition=inline%3Bfilename%2A%3Dutf-8%27%27FissaiD-EH301-V8-OnLine.pdf&response-content-type=application%2Fpdf&auth_key=1695929334-f2ca675f6c4842eda7036f465ffdbeac-0-cca5608b286471bd42819337066a0dbb

    Returns:
        str: RFID
    '''
    data_read = input()
    # will look something like this: ABC12345678XYZ
    # where 123 is FC and 45678 is ID
    match = re.match(r'^ABC(?P<FC>\d{3})(?P<ID>\d{5})XYZ$', data_read)

    if not match:
        print("Invalid RFID scan")
        return None
    
    fc, id = match.group('FC'), match.group('ID')
    print(f"FC: {fc}, ID: {id}")
    return fc, id

def main():
    while True:
        print("Waiting for RFID scans...")
        rfid_return_value = read_rfid()
        if not rfid_return_value:
            continue
        fc, id = rfid_return_value
        
        print("RFID scanned, fd: {fc}, id: {id}")

        response = requests.get(f"{BACKEND_URL}/rfid_check", params={'fc': fc, 'id': id})
        match response.status_code:
            case requests.codes.ok:
                print("RFID is valid")
                sound_url = response.json()['sound_url']
                play_sound(sound_url)
            case requests.codes.unauthorized:
                print("RFID is not registered") 
                # TODO: play sound that says "RFID is not registered... your registration color is X"
            case _:
                raise Exception(f"Failed to check RFID, status code: {response.status_code}")



if __name__ == '__main__':
    main()