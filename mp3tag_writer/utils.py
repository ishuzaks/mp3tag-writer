from pathlib import Path

from PIL import Image


def get_mimetype(image: Path) -> str:
    with Image.open(image) as f:
        return f.get_format_mimetype()
