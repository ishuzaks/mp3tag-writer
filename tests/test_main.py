from mp3tag_writer import load_metadata
from pytest_mock import MockerFixture


class TestMp3TagWriter:
    def test_load_metadata(self, mocker: MockerFixture):
        # モックの設定
        mock_audio = mocker.MagicMock()
        mock_audio.info.length = 120.0  # 例: 長さ120秒
        mock_audio.info.bitrate = 128000  # 例: ビットレート128kbps
        mock_audio.tags = {"TIT2": "Sample Title"}
        patcher = mocker.patch(
            "mp3tag_writer.__main__.MP3", autospec=True, return_value=mock_audio
        )

        # 関数を呼び出し
        metadata = load_metadata("dummy.mp3")

        # アサーション
        assert metadata.info.length == 120.0
        assert metadata.info.bitrate == 128000
        assert metadata.tags["TIT2"] == "Sample Title"
        patcher.assert_called_once_with(filename="dummy.mp3")
