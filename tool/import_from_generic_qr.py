import base64
import sys
import traceback
from argparse import ArgumentParser
from pathlib import Path
from typing import Any, Optional, cast
from urllib.parse import parse_qs, urlparse

import pyotp
from rich import print
from rich.rule import Rule

from tool import errors, ux
from tool.auth_registration import (AuthRegistrationEntry, append_auth_entries,
                                    append_or_create_entries,
                                    save_auth_entries)
from tool.constants import (DEFAULT_INTERVAL, DEFAULT_NUM_DIGITS,
                            URL_SCHEME_OTP_AUTH)
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
        print(Rule())

        context = {
            "source": "2FA app",
            "file": str(holder.file),
            "url": holder.url,
        }

        print(f"Handling ...")
        print("\tFile:", holder.file)
        print("\tURL:", holder.url)

        try:
            entry = parse_url_standard(holder, context)
        except Exception as error:
            print(f"\t[red]Error[/red] (will go into fallback mode): {error}")
            entry = parse_url_fallback(holder, context)

        if entry is not None:
            print(f"\tFound one entry.")
            new_entries.append(entry)

    if not new_entries:
        print("No entries to import.")
        return

    print(Rule())
    append_or_create_entries(auth_path, new_entries)


def parse_url_standard(holder: UrlHolder, context: Any) -> AuthRegistrationEntry:
    print("parse_url_standard()", holder.url[:80], "...")

    totp = cast(pyotp.TOTP, pyotp.parse_uri(holder.url))

    return AuthRegistrationEntry(
        context=context,
        issuer=totp.issuer or "",
        label=totp.name,
        algorithm=totp.digest.__name__ if totp.digest is not None else "",
        digits=totp.digits,
        interval=totp.interval,
        secret=base64.b32encode(totp.byte_secret()).decode()
    )


def parse_url_fallback(holder: UrlHolder, context: Any) -> Optional[AuthRegistrationEntry]:
    print("parse_url_fallback()", holder.url[:80], "...")

    parsed_url = urlparse(holder.url)

    if parsed_url.scheme != URL_SCHEME_OTP_AUTH:
        return None

    parameters = parse_qs(parsed_url.query)
    issuer = parameters.get("issuer", [""])[0]
    label = parsed_url.path.strip("/")
    algorithm = parameters.get("algorithm", [""])[0].lower()
    digits = int(parameters.get("digits", [DEFAULT_NUM_DIGITS])[0])
    interval = int(parameters.get("period", [DEFAULT_INTERVAL])[0])
    secret = parameters.get("secret", [""])[0]

    return AuthRegistrationEntry(
        context=context,
        issuer=issuer,
        label=label,
        algorithm=algorithm,
        digits=digits,
        interval=interval,
        secret=secret
    )


if __name__ == "__main__":
    ret = main(sys.argv[1:])
    sys.exit(ret)
