import os

from mutagen.id3 import ID3, TIT2, Frames
from mutagen.mp3 import MP3


def load_metadata(file: str | os.PathLike[str]) -> MP3:
    return MP3(filename=file)


def write_tags(mp3: MP3, field: str, value: str | float) -> MP3:
    frame = Frames.get(field)

    if frame is None:
        msg = f"Frame {field} not found"
        raise ValueError(msg)

    mp3.ID3.add(frame(encoding=3, text=value))
    return mp3
