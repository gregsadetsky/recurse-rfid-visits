#!/usr/bin/env python3
import sys
import subprocess
from urllib.parse import urlparse
import os
import requests
from typing import Union, Tuple, List
import logging
import keyboard
import itertools
import pathlib

BACKEND_URL = "https://octopass.recurse.com"
HTTP_ERROR_MP3 = "http-error.mp3"
UNKNOWN_ERROR_MP3 = "unknown-error.mp3"
STARTUP_MP3 = "startup.mp3"
MODULE_PATH = pathlib.Path(__file__).parent.absolute()

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.StreamHandler(stream=sys.stdout)
formatter = logging.Formatter(
    fmt="%(asctime)s %(name)s.%(levelname)s: %(message)s",
    datefmt="%Y.%m.%d %H:%M:%S",
)
handler.setFormatter(formatter)
logger.addHandler(handler)


def _play_sound(
    sound_url: Union[None, str] = None,
    cached_sound_path: Union[None, pathlib.Path] = None,
) -> None:
    """
    Play sound from url, will always attempt to find a cached sound file first
    in case the sound file is not cached, it will be downloaded and cached to cache_sound_path
    if cached_sound_path is not provided, it will be cached to the current working directory, with the name of the file

    Args:
        sound_url: url to sound file. in case of None cached_sound_path must be provided. Defaults to None
        cached_sound_path: path to cache the sound file. Defaults to None (will be cached to current working directory, with the name of the file)

    Returns:
        None
    """
    if not (cached_sound_path is not None or sound_url is not None):
        raise ValueError("sound_url or cached_sound_path must be provided")

    if cached_sound_path is None:
        parsed_url = urlparse(sound_url)
        cached_sound_path = pathlib.Path.cwd() / pathlib.Path(parsed_url.path).name

    if not pathlib.Path(cached_sound_path).exists():
        if sound_url is None:
            raise FileNotFoundError(f"Sound file not found in {cached_sound_path}")

        logger.info("Downloading sound...")
        r = requests.get(sound_url, allow_redirects=True)
        open(cached_sound_path, "wb").write(r.content)
        logger.info("Sound downloaded")

    logger.info("Playing sound...")
    subprocess.call(f"/usr/bin/mpv --volume=100 {cached_sound_path}", shell=True)


def play_sounds(
    sound_urls: Union[None, List[str]] = None,
    cached_sound_paths: Union[None, List[pathlib.Path]] = None,
) -> None:
    """
    Play list of sounds from urls

    Args:
        sound_urls: list of urls to sound files
        cached_sound_paths: list of paths to cached sound files

    Notes:
        1. sound_urls and cached_sound_paths cannot be provided at the same time, unless they are of the same length
        2. at least one of sound_urls or cached_sound_paths must be provided
    Returns:
        None
    """
    if not (sound_urls is not None or cached_sound_paths is not None):
        raise ValueError("sound_urls or cached_sound_paths must be provided")

    if not (
        (sound_urls is None or cached_sound_paths is None)
        or len(sound_urls) == len(cached_sound_paths)
    ):
        raise ValueError(
            "sound_urls and cached_sound_paths cannot be provided at the same time, unless they are of the same length"
        )

    list_length = len(sound_urls) if sound_urls is not None else len(cached_sound_paths)

    for i in range(list_length):
        _play_sound(
            sound_urls[i] if sound_urls is not None else None,
            cached_sound_paths[i] if cached_sound_paths is not None else None,
        )


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


def play_http_error_sound(status_code: int) -> None:
    """
    Play sound according to http status code

    Args:
        status_code: http status code

    Returns:
        None
    """
    play_sounds(
        cached_sound_paths=list(
            itertools.chain(
                [pathlib.Path(MODULE_PATH) / f"assets/{HTTP_ERROR_MP3}"],
                [
                    pathlib.Path(MODULE_PATH) / f"assets/{number}.mp3"
                    for number in str(status_code)
                ],
            ),
        )
    )


def main():
    try:
        logger.debug(f"Working directory: {pathlib.Path.cwd()}")
        logger.debug(f"Module path: {MODULE_PATH}")
        _play_sound(
            cached_sound_path=pathlib.Path(MODULE_PATH) / f"assets/{STARTUP_MP3}"
        )

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
                play_http_error_sound(response.status_code)
            else:
                play_http_error_sound(response.status_code)
                logger.error(
                    f"Unknown HTTP error returned from the backend. error code: {response.status_code}"
                )
    except Exception as e:
        logger.exception(e)
        _play_sound(
            cached_sound_path=pathlib.Path(MODULE_PATH) / f"assets/{UNKNOWN_ERROR_MP3}"
        )


if __name__ == "__main__":
    main()
