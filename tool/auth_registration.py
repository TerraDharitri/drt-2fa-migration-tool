
import json
from pathlib import Path
from typing import Any, Optional

from rich import print
from rich.prompt import Confirm

from tool.constants import (DEFAULT_ALGORITHM_NAME, DEFAULT_INTERVAL,
                            DEFAULT_NUM_DIGITS)


class AuthRegistrationEntry:
    def __init__(self,
                 context: dict[str, Any],
                 issuer: str,
                 label: str,
                 algorithm: str,
                 digits: int,
                 interval: int,
                 secret: str) -> None:
        self.context = context
        self.issuer = issuer
        self.label = label
        self.algorithm = algorithm or DEFAULT_ALGORITHM_NAME
        self.digits = digits or DEFAULT_NUM_DIGITS
        self.interval = interval or DEFAULT_INTERVAL
        self.secret = secret

    @classmethod
    def new_from_dictionary(cls, data: dict[str, Any]):
        context = data.get("context", {})

        # Handle synonyms, on a best-effort basis.
        issuer = data.get("issuer", "")
        label = (data.get("account", "")
                 or data.get("name", "")
                 or data.get("label", "")
                 or data.get("tag", ""))
        algorithm = data.get("algorithm", "")
        digits = data.get("digits", 0)
        interval = (data.get("interval", 0)
                    or data.get("period", 0))
        secret = data.get("secret", "")

        return cls(
            context=context,
            issuer=issuer,
            label=label,
            algorithm=algorithm,
            digits=digits,
            interval=interval,
            secret=secret,
        )

    def to_dictionary(self) -> dict[str, Any]:
        return {
            "context": self.context,
            "issuer": self.issuer,
            "label": self.label,
            "algorithm": self.algorithm,
            "digits": self.digits,
            "interval": self.interval,
            "secret": self.secret,
        }


def append_or_create_entries(file: Path, entries: list[AuthRegistrationEntry]):
    if file.exists():
        print(f"File [yellow]already exists[/yellow]: {file}")
        if not Confirm.ask(f"[yellow]Append[/yellow] {len(entries)} new entry (entries) to it?"):
            return

        append_auth_entries(file, entries)
    else:
        save_auth_entries(file, entries)


def load_auth_entries(file: Path) -> list[AuthRegistrationEntry]:
    content = file.read_text()
    entries_raw = json.loads(content)
    entries = [AuthRegistrationEntry.new_from_dictionary(entry) for entry in entries_raw]

    print(f"Loaded {len(entries)} entries from file: {file}")
    return entries


def append_auth_entries(file: Path, entries: list[AuthRegistrationEntry]):
    original_entries = load_auth_entries(file)
    updated_entries = original_entries + entries

    print(f"Saving {len(original_entries)} + {len(entries)} = {len(updated_entries)} entries.")
    save_auth_entries(file, updated_entries)


def save_auth_entries(file: Path, entries: list[AuthRegistrationEntry]):
    entries_raw = [entry.to_dictionary() for entry in entries]
    content = json.dumps(entries_raw, indent=4)
    file.write_text(content)
    print(f"File saved: {file}")
