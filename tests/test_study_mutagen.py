from pathlib import Path
from pprint import pprint

from mutagen.id3 import APIC, ID3, TIT2, Frames
from mutagen.mp3 import MP3


def test_id3_tag_read() -> None:
    for path in (Path.cwd() / "exclude" / "mp3").glob(pattern=r"*.mp3"):
        tags = ID3(path)
        print(tags.pprint())


def test_id3_tag_read_from_mp3_instance() -> None:
    for path in (Path.cwd() / "exclude" / "mp3").glob(pattern=r"*.mp3"):
        mp3 = MP3(filename=path)

    print(mp3.pprint())


def test_frames_values() -> None:
    pprint(Frames)
    fields = ["TALB", "TDRC", "TCON", "TPE1", "TPE2"]
    for frame in [Frames.get(field) for field in fields]:
        pprint(frame)
