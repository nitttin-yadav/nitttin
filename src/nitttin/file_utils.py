"""File handling utilities."""

import json
import csv
import os
from pathlib import Path


def read_text(filepath: str | Path) -> str:
    """Read and return the contents of a text file.

    Raises:
        FileNotFoundError: If the file does not exist.
    """
    path = Path(filepath)
    if not path.exists():
        raise FileNotFoundError(f"File not found: {filepath}")
    return path.read_text(encoding="utf-8")


def write_text(filepath: str | Path, content: str) -> None:
    """Write content to a text file, creating directories as needed."""
    path = Path(filepath)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def read_json(filepath: str | Path) -> dict | list:
    """Read and parse a JSON file.

    Raises:
        FileNotFoundError: If the file does not exist.
        json.JSONDecodeError: If the file is not valid JSON.
    """
    content = read_text(filepath)
    return json.loads(content)


def write_json(filepath: str | Path, data: dict | list, indent: int = 2) -> None:
    """Write data to a JSON file."""
    path = Path(filepath)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=indent), encoding="utf-8")


def read_csv(filepath: str | Path) -> list[dict[str, str]]:
    """Read a CSV file and return a list of dictionaries.

    Raises:
        FileNotFoundError: If the file does not exist.
    """
    path = Path(filepath)
    if not path.exists():
        raise FileNotFoundError(f"File not found: {filepath}")
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return list(reader)


def write_csv(
    filepath: str | Path, data: list[dict[str, str]], fieldnames: list[str] | None = None
) -> None:
    """Write a list of dictionaries to a CSV file."""
    if not data:
        return
    path = Path(filepath)
    path.parent.mkdir(parents=True, exist_ok=True)
    if fieldnames is None:
        fieldnames = list(data[0].keys())
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)


def get_file_size(filepath: str | Path) -> int:
    """Return the file size in bytes.

    Raises:
        FileNotFoundError: If the file does not exist.
    """
    path = Path(filepath)
    if not path.exists():
        raise FileNotFoundError(f"File not found: {filepath}")
    return path.stat().st_size


def list_files(directory: str | Path, extension: str | None = None) -> list[str]:
    """List files in a directory, optionally filtering by extension.

    Raises:
        NotADirectoryError: If the path is not a directory.
    """
    path = Path(directory)
    if not path.is_dir():
        raise NotADirectoryError(f"Not a directory: {directory}")
    files = []
    for item in path.iterdir():
        if item.is_file():
            if extension is None or item.suffix == extension:
                files.append(item.name)
    return sorted(files)


def ensure_directory(directory: str | Path) -> Path:
    """Create a directory and parents if they don't exist. Return the Path."""
    path = Path(directory)
    path.mkdir(parents=True, exist_ok=True)
    return path
