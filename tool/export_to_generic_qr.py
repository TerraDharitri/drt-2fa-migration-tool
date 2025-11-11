import hashlib
import sys
import traceback
from argparse import ArgumentParser
from pathlib import Path
from typing import Any

import pyotp
import qrcode
from rich import print
from rich.prompt import Confirm

from tool import errors, ux
from tool.auth_registration import load_auth_entries
from tool.constants import DEFAULT_ALGORITHM, AuthAlgorithm
from tool.shared import create_random_tag, prepare_image_name


def main(cli_args: list[str] = sys.argv[1:]):
    try:
        _do_main(cli_args)
    except errors.KnownError as err:
        ux.show_critical_error(traceback.format_exc())
        ux.show_critical_error(err.get_pretty())
        return 1


def _do_main(cli_args: list[str]):
    parser = ArgumentParser()
    parser.add_argument("--auth", required=True, help="auth registration file (input)")
    parser.add_argument("--workspace", required=True, help="where to save the QR images (output)")
    parser.add_argument("--tag", required=False, help="export tag, for easier correlation of output files")
    parser.add_argument('--all', required=False, help="export all entries", action="store_true")
    args = parser.parse_args(cli_args)

    auth_path = Path(args.auth).expanduser().resolve()
    workspace = Path(args.workspace).expanduser().resolve()
    export_tag = args.tag or create_random_tag()
    should_confirm_each = not args.all

    workspace.mkdir(parents=True, exist_ok=True)
    entries = load_auth_entries(auth_path)

    for index, entry in enumerate(entries):
        print(f"[yellow]{entry.label}[/yellow]")

        if should_confirm_each:
            if not Confirm.ask("Export?"):
                continue

        provisioning_uri = pyotp.totp.TOTP(
            s=entry.secret,
            digits=entry.digits,
            digest=convert_string_to_algorithm(entry.algorithm),
            name=entry.label,
            issuer=entry.issuer,
            interval=entry.interval
        ).provisioning_uri()

        image_name = prepare_image_name(
            tag=export_tag,
            index=index,
            labels=[entry.label]
        )

        image_path = workspace / image_name

        print(f"\tURI: {provisioning_uri}")
        print(f"\tImage: {image_path}")

        img: Any = qrcode.make(provisioning_uri)
        img.save(image_path)


def convert_string_to_algorithm(algorithm_name: str) -> Any:
    if not algorithm_name:
        return DEFAULT_ALGORITHM

    algorithm_name = algorithm_name.lower()

    if algorithm_name == AuthAlgorithm.SHA1:
        return hashlib.sha1
    if algorithm_name == AuthAlgorithm.SHA256:
        return hashlib.sha256
    if algorithm_name == AuthAlgorithm.SHA512:
        return hashlib.sha512
    if algorithm_name == AuthAlgorithm.MD5:
        return hashlib.md5

    raise errors.KnownError(f"unknown algorithm: {algorithm_name}")


if __name__ == "__main__":
    ret = main(sys.argv[1:])
    sys.exit(ret)
