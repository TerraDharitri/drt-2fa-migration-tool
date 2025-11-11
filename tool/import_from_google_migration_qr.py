import base64
import sys
import traceback
from argparse import ArgumentParser
from pathlib import Path
from typing import Optional
from urllib.parse import parse_qs, urlparse

from rich import print

from tool import errors, ux
from tool.auth_registration import (AuthRegistrationEntry,
                                    append_or_create_entries)
from tool.constants import URL_SCHEME_GOOGLE_OTPAUTH_MIGRATION, AuthAlgorithm
from tool.google_auth_migration_pb2 import (Algorithm, DigitCount,
                                            MigrationPayload)
from tool.qr import UrlHolder, read_urls_from_folder


def main(cli_args: list[str] = sys.argv[1:]):
    try:
        _do_main(cli_args)
    except errors.KnownError as err:
        ux.show_critical_error(traceback.format_exc())
        ux.show_critical_error(err.get_pretty())
        return 1


def _do_main(cli_args: list[str]):
    parser = ArgumentParser()
    parser.add_argument("--auth", required=True, help="auth registration file (output)")
    parser.add_argument("--workspace", required=True, help="where to find QR images (input)")

    args = parser.parse_args(cli_args)

    auth_path = Path(args.auth).expanduser().resolve()
    workspace = Path(args.workspace).expanduser().resolve()

    new_entries: list[AuthRegistrationEntry] = []
    url_holders = read_urls_from_folder(workspace)

    for holder in url_holders:
        print(f"Handling {holder.file} ...")
        entries = read_entries(holder)

        print(f"Found {len(entries)} entries.")
        new_entries.extend(entries)

    if not new_entries:
        print("No entries to import.")
        return

    append_or_create_entries(auth_path, new_entries)


def read_entries(url_holder: UrlHolder) -> list[AuthRegistrationEntry]:
    entries: list[AuthRegistrationEntry] = []

    parsed_url = urlparse(url_holder.url)

    if parsed_url.scheme != URL_SCHEME_GOOGLE_OTPAUTH_MIGRATION:
        return []

    data = parse_qs(parsed_url.query).get("data", [""])[0]
    decoded_data = base64.b64decode(data)
    migration_payload = MigrationPayload.FromString(decoded_data)

    context = {
        "source": "Google Authenticator",
        "file": str(url_holder.file),
        "url": url_holder.url,
    }

    for item in migration_payload.otp_parameters:
        entries.append(AuthRegistrationEntry(
            context=context,
            issuer=item.issuer,
            label=item.name,
            algorithm=convert_algorithm_to_string(item.algorithm),
            digits=convert_digit_count_to_int(item.digits),
            interval=0,
            secret=base64.b32encode(item.secret).decode(),
        ))

    return entries


def convert_algorithm_to_string(algorithm: Algorithm) -> str:
    if algorithm == Algorithm.ALGORITHM_TYPE_UNSPECIFIED:
        return ""
    if algorithm == Algorithm.SHA1:
        return AuthAlgorithm.SHA1
    if algorithm == Algorithm.SHA256:
        return AuthAlgorithm.SHA256
    if algorithm == Algorithm.SHA512:
        return AuthAlgorithm.SHA512
    if algorithm == Algorithm.MD5:
        return AuthAlgorithm.MD5

    raise errors.KnownError(f"unknown algorithm: {algorithm}")


def convert_digit_count_to_int(digit_count: DigitCount) -> int:
    if digit_count == DigitCount.DIGIT_COUNT_UNSPECIFIED:
        return 0
    if digit_count == DigitCount.SIX:
        return 6
    if digit_count == DigitCount.EIGHT:
        return 8

    raise errors.KnownError(f"unknown digit count: {digit_count}")


if __name__ == "__main__":
    ret = main(sys.argv[1:])
    sys.exit(ret)
