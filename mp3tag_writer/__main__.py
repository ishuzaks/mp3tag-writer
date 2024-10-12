import json
import os
from copy import deepcopy
from pathlib import Path

from mutagen.id3 import Frames
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


def load_json_file(file: str | os.PathLike[str]) -> dict:
    with Path(file).open(mode="r", encoding="utf-8") as f:
        loaded = json.load(f)

    data = deepcopy(loaded)

    data["tags"] = [
        Frames[tag](encoding=3, text=value)
        for tag, value in loaded.get("tags", {}).items()
        if tag in Frames
    ]

    return data
