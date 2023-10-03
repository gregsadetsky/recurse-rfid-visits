#!/usr/bin/env python3
import sys
import subprocess
from urllib.parse import urlparse
import os
import requests
from typing import Union, Tuple, List
import logging
import keyboard

BACKEND_URL = "https://64dd-2602-fb65-0-100-b072-c2e7-c8ba-2075.ngrok-free.app"

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.StreamHandler(stream=sys.stdout)
formatter = logging.Formatter(
    fmt="%(asctime)s %(name)s.%(levelname)s: %(message)s",
    datefmt="%Y.%m.%d %H:%M:%S",
)
handler.setFormatter(formatter)
logger.addHandler(handler)

def _play_sound(sound_url, cached_sound_path: Union[None, str] = None) -> None:
    """
    Play sound from url, will always attempt to find a cached sound file first
    in case the sound file is not cached, it will be downloaded and cached to cache_sound_path
    if cached_sound_path is not provided, it will be cached to the current working directory, with the name of the file

    Args:
        sound_url (str): url to sound file
        cached_sound_path (Union[None, str]): path to cache the sound file. Defaults to None (will be cached to current working directory, with the name of the file)

    Returns:
        None
    """
    if cached_sound_path is None:
        parsed_url = urlparse(sound_url)
        cached_sound_path = os.path.join(os.getcwd(), os.path.basename(parsed_url.path))

    if not os.path.exists(cached_sound_path):
        logger.info("Downloading sound...")
        r = requests.get(sound_url, allow_redirects=True)
        open(cached_sound_path, "wb").write(r.content)
        logger.info("Sound downloaded")

    logger.info("Playing sound...")
    subprocess.call(f"/usr/bin/mpv {cached_sound_path}", shell=True)


def play_sounds(sound_urls: List[str]) -> None:
    """
    Play list of sounds from urls

    Args:
        sound_urls (list[str]): list of urls to sound files

    Returns:
        None
    """
    for sound_url in sound_urls:
        _play_sound(sound_url)


def read_rfid() -> Union[Tuple[str, str], None]:
    """
    Read RFID from RFID reader
    We use EH301 RFID reader which simulate keyboard input (with newline)

    This device has multiple configuration modes, we use the default mode which is:
    10 digit format, With Enter, buzzer sound, QWERTY keyboard, Disable HID Raw

    Note: if you would like to read more about configuring this device you can follow this:
    https://download.wezhan.cn/contents/sitefiles2041/10205132/files/473369..pdf?response-content-disposition=inline%3Bfilename%2A%3Dutf-8%27%27FissaiD-EH301-V8-OnLine.pdf&response-content-type=application%2Fpdf&auth_key=1695929334-f2ca675f6c4842eda7036f465ffdbeac-0-cca5608b286471bd42819337066a0dbb

    Returns:
        tuple of (fc, card) if RFID is valid, None otherwise
    """
    data_read = list(keyboard.get_typed_strings(keyboard.record(until="enter")))[0]
    if len(data_read) != 10:
        logger.error(f"RFID is not 10 digits, RFID: {data_read}")
        return None
    
    # will be 10 digits number in the base of 10
    read_value_value = int(data_read, 10)

    # the format being used here is 8h-10d in the documentation
    fc = (read_value_value >> 16) & 0xFF
    card = read_value_value & 0xFFFF

    return fc, card


def main():
    logger.debug(f"Working directory: {os.getcwd()}")

    while True:
        logger.info("Waiting for RFID scans...")
        rfid_return_value = read_rfid()
        if not rfid_return_value:
            continue
        fc, card = rfid_return_value

        logger.info(f"RFID scanned, fd: {fc}, card: {card}")

        response = requests.post(
            f"{BACKEND_URL}/api/scan",
            json={"fc": fc, "card": card},
            headers={"x-api-key": os.environ["API_TOKEN"]},
        )
        if response.status_code == requests.codes.ok:
            logger.debug("RFID is valid")
            sound_urls = response.json()["sound_urls"]
            play_sounds(sound_urls)
        elif response.status_code == requests.codes.unauthorized:
            logger.error("token is invalid")
        else:
            raise Exception(
                f"Failed to check RFID, status code: {response.status_code}"
            )


if __name__ == "__main__":
    main()
