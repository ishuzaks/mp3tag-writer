import os

from mutagen.mp3 import MP3


def load_metadata(file: str | os.PathLike[str]) -> MP3:
    return MP3(filename=file)
