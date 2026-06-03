"""Comprehensive tests for the file_utils module."""

import json
import pytest
from pathlib import Path

from nitttin.file_utils import (
    read_text,
    write_text,
    read_json,
    write_json,
    read_csv,
    write_csv,
    get_file_size,
    list_files,
    ensure_directory,
)


@pytest.fixture
def tmp_dir(tmp_path):
    """Provide a temporary directory for file tests."""
    return tmp_path


class TestReadText:
    def test_read_existing_file(self, tmp_dir):
        f = tmp_dir / "hello.txt"
        f.write_text("hello world", encoding="utf-8")
        assert read_text(str(f)) == "hello world"

    def test_read_nonexistent_raises(self, tmp_dir):
        with pytest.raises(FileNotFoundError):
            read_text(str(tmp_dir / "missing.txt"))


class TestWriteText:
    def test_write_creates_file(self, tmp_dir):
        f = tmp_dir / "out.txt"
        write_text(str(f), "content")
        assert f.read_text(encoding="utf-8") == "content"

    def test_write_creates_parent_dirs(self, tmp_dir):
        f = tmp_dir / "sub" / "deep" / "file.txt"
        write_text(str(f), "nested")
        assert f.read_text(encoding="utf-8") == "nested"


class TestReadJson:
    def test_read_valid_json(self, tmp_dir):
        f = tmp_dir / "data.json"
        f.write_text('{"key": "value"}', encoding="utf-8")
        assert read_json(str(f)) == {"key": "value"}

    def test_read_json_list(self, tmp_dir):
        f = tmp_dir / "list.json"
        f.write_text('[1, 2, 3]', encoding="utf-8")
        assert read_json(str(f)) == [1, 2, 3]

    def test_read_invalid_json_raises(self, tmp_dir):
        f = tmp_dir / "bad.json"
        f.write_text("not json", encoding="utf-8")
        with pytest.raises(json.JSONDecodeError):
            read_json(str(f))

    def test_read_json_nonexistent_raises(self, tmp_dir):
        with pytest.raises(FileNotFoundError):
            read_json(str(tmp_dir / "nope.json"))


class TestWriteJson:
    def test_write_dict(self, tmp_dir):
        f = tmp_dir / "out.json"
        write_json(str(f), {"a": 1, "b": 2})
        assert json.loads(f.read_text(encoding="utf-8")) == {"a": 1, "b": 2}

    def test_write_json_creates_dirs(self, tmp_dir):
        f = tmp_dir / "x" / "y" / "z.json"
        write_json(str(f), [1, 2])
        assert json.loads(f.read_text(encoding="utf-8")) == [1, 2]


class TestReadCsv:
    def test_read_csv(self, tmp_dir):
        f = tmp_dir / "data.csv"
        f.write_text("name,age\nAlice,30\nBob,25\n", encoding="utf-8")
        rows = read_csv(str(f))
        assert len(rows) == 2
        assert rows[0] == {"name": "Alice", "age": "30"}
        assert rows[1] == {"name": "Bob", "age": "25"}

    def test_read_csv_nonexistent_raises(self, tmp_dir):
        with pytest.raises(FileNotFoundError):
            read_csv(str(tmp_dir / "missing.csv"))


class TestWriteCsv:
    def test_write_csv(self, tmp_dir):
        f = tmp_dir / "out.csv"
        data = [{"x": "1", "y": "2"}, {"x": "3", "y": "4"}]
        write_csv(str(f), data)
        content = f.read_text(encoding="utf-8")
        assert "x,y" in content
        assert "1,2" in content
        assert "3,4" in content

    def test_write_csv_empty_data(self, tmp_dir):
        f = tmp_dir / "empty.csv"
        write_csv(str(f), [])
        assert not f.exists()

    def test_write_csv_custom_fieldnames(self, tmp_dir):
        f = tmp_dir / "custom.csv"
        data = [{"a": "1", "b": "2"}]
        write_csv(str(f), data, fieldnames=["b", "a"])
        content = f.read_text(encoding="utf-8")
        lines = content.strip().split("\n")
        assert lines[0] == "b,a"


class TestGetFileSize:
    def test_get_size(self, tmp_dir):
        f = tmp_dir / "sized.txt"
        f.write_text("12345", encoding="utf-8")
        assert get_file_size(str(f)) == 5

    def test_nonexistent_raises(self, tmp_dir):
        with pytest.raises(FileNotFoundError):
            get_file_size(str(tmp_dir / "nope.txt"))


class TestListFiles:
    def test_list_all_files(self, tmp_dir):
        (tmp_dir / "a.txt").touch()
        (tmp_dir / "b.py").touch()
        (tmp_dir / "subdir").mkdir()
        files = list_files(str(tmp_dir))
        assert "a.txt" in files
        assert "b.py" in files
        assert "subdir" not in files

    def test_filter_by_extension(self, tmp_dir):
        (tmp_dir / "a.txt").touch()
        (tmp_dir / "b.py").touch()
        files = list_files(str(tmp_dir), extension=".txt")
        assert files == ["a.txt"]

    def test_not_a_directory_raises(self, tmp_dir):
        f = tmp_dir / "file.txt"
        f.touch()
        with pytest.raises(NotADirectoryError):
            list_files(str(f))


class TestEnsureDirectory:
    def test_creates_directory(self, tmp_dir):
        d = tmp_dir / "new" / "nested"
        result = ensure_directory(str(d))
        assert d.exists()
        assert result == d

    def test_existing_directory(self, tmp_dir):
        result = ensure_directory(str(tmp_dir))
        assert result == tmp_dir
