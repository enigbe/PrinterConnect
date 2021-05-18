import json
from pathlib import Path
from typing import List

strings_file = 'en-ng'
cached_strings = {}
base_directory = Path(__file__).resolve().parent.parent
strings_directory = base_directory.joinpath('strings')


def refresh_cached_string():
    global cached_strings
    with open(f"{strings_directory}/{strings_file}.json") as f:
        cached_strings = json.load(f)


def gettext(name):
    return cached_strings[name]


def split_name(name: str) -> List:
    return name.split(' ')


refresh_cached_string()
