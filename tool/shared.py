import random
import string
from typing import Any


def prepare_image_name(tag: str, index: int, labels: list[str]) -> str:
    padded_index = str(index).zfill(3)
    aggregated_label = "_".join(labels)
    normalized_label = "".join(char if char.isalnum() else "_" for char in aggregated_label)
    return f"{tag}_{padded_index}_{normalized_label}.png"


def split_to_chunks(items: list[Any], chunk_size: int):
    assert chunk_size > 0

    for i in range(0, len(items), chunk_size):
        yield items[i:i + chunk_size]


def create_random_tag(length: int = 8) -> str:
    return "".join(random.SystemRandom().choice(string.ascii_lowercase + string.digits) for _ in range(length))
