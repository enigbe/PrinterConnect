import json

strings_file = 'en-ng'
cached_strings = {}


def refresh_cached_string():
    global cached_strings
    with open(f'strings/{strings_file}.json') as f:
        cached_strings = json.load(f)


def gettext(name):
    return cached_strings[name]


refresh_cached_string()
