import pytest
from mp3tag_writer import load_metadata, write_tags
from mutagen.id3 import Frames
from mutagen.mp3 import MP3
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
