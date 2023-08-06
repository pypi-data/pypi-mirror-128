import json
import os
from pathlib import Path
from ..configs import LANGUAGE_CODE

LANGUAGE_FILE_PATH = f"{Path(__file__).resolve().parent.joinpath('locales')}/{LANGUAGE_CODE}.json"

if os.path.isfile(LANGUAGE_FILE_PATH):
    CURRENT_LANGUAGE = json.load(open(LANGUAGE_FILE_PATH, 'r'))
else:
    CURRENT_LANGUAGE = {}


def get_translated_text(text: str):
    translated = CURRENT_LANGUAGE.get(text)
    return translated if translated is not None else text
