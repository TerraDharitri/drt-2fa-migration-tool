from pathlib import Path
from typing import Any

from PIL import Image
from pyzbar import pyzbar

from tool.constants import IMAGES_EXTENSIONS


class UrlHolder:
    def __init__(self, file: Path, url: str):
        self.file = file
        self.url = url


def read_urls_from_folder(folder: Path) -> list[UrlHolder]:
    folder = Path(folder).expanduser().resolve()
    files = list(folder.rglob("*"))
    results: list[UrlHolder] = []

    for file in files:
        results.extend(read_urls_from_file(file))

    return results


def read_urls_from_file(file: Path) -> list[UrlHolder]:
    file = Path(file).expanduser().resolve()

    if not file.suffix.lower() in IMAGES_EXTENSIONS:
        return []

    image = Image.open(file)
    codes: list[Any] = pyzbar.decode(image)
    urls = [code.data.decode() for code in codes]
    results = [UrlHolder(file, url) for url in urls]
    return results
