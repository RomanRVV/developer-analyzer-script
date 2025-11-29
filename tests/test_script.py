import pytest
from _pytest.capture import CaptureFixture
from unittest.mock import patch
from pathlib import Path
from script import read_csv, parse_args, main


class TestReadCsv:
    def test_read_csv_success(self, tmp_path: Path) -> None:
        csv_file = tmp_path / "test.csv"
        csv_file.write_text("position,performance\nQA,5.3\nDev,4.4")
        result = read_csv([str(csv_file)])

        assert len(result) == 2
        assert result[0]["position"] == "QA"

    def test_read_csv_file_not_found(self) -> None:
        with pytest.raises(FileNotFoundError):
            read_csv(["/test/test.csv"])


class TestParseArgs:
    def test_parse_args_valid(self) -> None:
        with patch(
                "sys.argv",
                ["script.py", "--files", "test.csv", "--report", "performance"]
        ):
            args = parse_args()

            assert args.files == ["test.csv"]
            assert args.report == "performance"

    def test_parse_args_missing_required(self) -> None:
        with patch("sys.argv", ["script.py", "--files", "test.csv"]):
            with pytest.raises(SystemExit):
                parse_args()


class TestMain:

    def test_main_success(
            self,
            tmp_path: Path,
            capsys: CaptureFixture
    ) -> None:
        csv_file = tmp_path / "test.csv"
        csv_file.write_text("position,performance\nQA,5.3\nDev,4.4")

        with patch(
                "sys.argv",
                ["script.py", "--files", str(csv_file), "--report", "performance"]
        ):
            main()

        captured = capsys.readouterr()
        assert "QA" in captured.out
        assert "5.3" in captured.out
        assert "Dev" in captured.out
        assert "4.4" in captured.out

    def test_main_calculates_average(
            self,
            tmp_path: Path,
            capsys: CaptureFixture
    ) -> None:
        csv_file = tmp_path / "test.csv"
        csv_file.write_text("position,performance\nDev,5.7\nDev,6")

        with patch(
                "sys.argv",
                ["script.py", "--files", str(csv_file), "--report", "performance"]
        ):
            main()

        captured = capsys.readouterr()
        avg_perf = "5.85"
        assert avg_perf in captured.out

    def test_main_file_not_found(self) -> None:
        with patch(
                "sys.argv",
                ["script.py", "--files", "/test/test.csv", "--report", "performance"]
        ):
            with pytest.raises(FileNotFoundError):
                main()
