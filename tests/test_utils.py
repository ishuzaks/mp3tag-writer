from pathlib import Path

import py
import pytest
from mp3tag_writer.utils import get_mimetype
from PIL import Image


class TestImageTools:
    def create_white_image(self, ext: str, dir_: Path) -> Path:
        _path = (Path(dir_) / "image.tmp").with_suffix(ext)

        # 真っ白な画像を作成
        white_image = Image.new("RGB", (500, 500), (255, 255, 255))

        # 画像を保存
        white_image.save(_path)
        return _path

    @pytest.fixture
    def jpg(self, tmpdir: py.path.LocalPath) -> Path:
        return self.create_white_image(".jpg", tmpdir)

    @pytest.fixture
    def png(self, tmpdir: py.path.LocalPath) -> Path:
        return self.create_white_image(".png", tmpdir)

    @pytest.fixture
    def webp(self, tmpdir: py.path.LocalPath) -> Path:
        return self.create_white_image(".webp", tmpdir)

    def test_get_jpeg_mimetype(self, jpg: Path) -> None:
        assert get_mimetype(jpg) == "image/jpeg"

    def test_get_png_mimetype(self, png: Path) -> None:
        assert get_mimetype(png) == "image/png"

    def test_get_webp_mimetype(self, webp: Path) -> None:
        assert get_mimetype(webp) == "image/webp"
