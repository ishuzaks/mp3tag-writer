import json
from pathlib import Path

import py
import pytest
from mp3tag_writer import load_json_file, load_metadata, write_tags
from mutagen.id3 import Frames
from mutagen.mp3 import MP3
from PIL import Image
from pytest_mock import MockerFixture


class TestMp3TagWriter:
    def test_load_metadata(self, mocker: MockerFixture) -> None:
        mock_audio = mocker.MagicMock()
        mock_audio.info.length = 120.0  # 例: 長さ120秒
        mock_audio.info.bitrate = 128000  # 例: ビットレート128kbps
        mock_audio.tags = {"TIT2": "Sample Title"}
        patcher = mocker.patch(
            "mp3tag_writer.__main__.MP3", autospec=True, return_value=mock_audio
        )

        metadata = load_metadata("dummy.mp3")

        assert metadata.info.length == 120.0
        assert metadata.info.bitrate == 128000
        assert metadata.tags["TIT2"] == "Sample Title"
        patcher.assert_called_once_with(filename="dummy.mp3")

    def test_write_success_tags(self, mocker: MockerFixture) -> None:
        mock_metadata = mocker.MagicMock(autospec=MP3)

        write_tags(mp3=mock_metadata, field="TIT2", value="Sample Title")

        frame = Frames.get("TIT2")
        mock_metadata.ID3.add.assert_called_once_with(
            frame(encoding=3, text="Sample Title")
        )

    def test_write_failed_tags(self, mocker: MockerFixture) -> None:
        mock_metadata = mocker.MagicMock(autospec=MP3)

        field = "TIT001"
        with pytest.raises(ValueError, match=f"Frame {field} not found"):
            write_tags(mp3=mock_metadata, field=field, value="Sample Title")


class TestJSONLoader:
    @pytest.fixture
    def simple_json_file(self, tmpdir: py.path.LocalPath) -> py.path.LocalPath:
        file = tmpdir / "simple.json"
        file.write_text(
            """{
  "tags": {
    "TALB": "Sample Album",
    "TDRC": "2024",
    "TCON": "sample genre",
    "TPE1": "Sample Artist",
    "TPE2": "Sample Artists"
  }
}""",
            encoding="utf-8",
        )
        return file

    def test_convert_from_json_to_dict_success(
        self, simple_json_file: py.path.LocalPath
    ) -> None:
        loaded = load_json_file(file=simple_json_file)

        with simple_json_file.open(mode="r", encoding="utf-8") as f:
            json_data = json.load(f)

        assert loaded
        for frame in loaded.get("tags"):
            assert any(
                frame.pprint() == f"{field_name}={text}"
                for field_name, text in json_data.get("tags").items()
            )

    @pytest.fixture
    def adding_cover_json_file(self, tmpdir: Path) -> Path:
        file = tmpdir / "adding_cover.json"
        cover = tmpdir / "cover.jpg"
        white_image = Image.new("RGB", (500, 500), (255, 255, 255))
        white_image.save(cover)
        file.write_text(
            f"""{{
  "tags": {{
    "TALB": "Sample Album2",
    "TDRC": "2022",
    "TCON": "sample genre2",
    "TPE1": "Sample Artist2",
    "TPE2": "Sample Artists2"
  }},
  "cover": "{cover}"
}}""",
            encoding="utf-8",
        )
        return file

    def test_convert_from_json_to_dict_with_cover_success(
        self, adding_cover_json_file: py.path.LocalPath
    ) -> None:
        loaded = load_json_file(file=adding_cover_json_file)

        apic = loaded["cover"]
        assert apic.encoding == 3
        assert apic.mime == "image/jpeg"
        assert apic.type == 3
        assert apic.desc == "cover"
        assert apic.data
