#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# (c) 2019, Philip Douglass <philip@philipdouglass.com>
"""
An Ansible Vault Client that manages Vault passwords in the Bitwarden
password manager (https://bitwarden.com).
"""
import json
import subprocess
import sys
from argparse import ArgumentParser
from base64 import b64encode
from configparser import ConfigParser
from configparser import NoSectionError
from pathlib import Path
from shlex import split as shplit
from shutil import which

BW = which("bw")
if not BW:
    raise Exception(
        "{prog} requires `bw' executable on $PATH".format(prog=Path(sys.argv[0]).name)
    )


ANSIBLE_METADATA = {
    "status": ["preview"],
    "supported_by": "community",
    "version": "1.0",
}

KEYNAME_UNKNOWN_RC = 2


def get_vault_config(vault_id=None):
    """
    Return the contents of the ansible.cfg [vault] section if present, or
    return the defaults.
    """
    try:
        # potential ImportError
        import ansible.constants as C

        config = ConfigParser()
        # potential TypeError`
        config.read(C.CONFIG_FILE)
        if not vault_id:
            vault_id = config.get("vault", "bitwarden_default_id", fallback="default")
        # potential NoSectionError
        return dict(config.items("vault", vars={"vault_id": vault_id}))
    except (ImportError, TypeError, NoSectionError):
        return {
            "bitwarden_default_id": "default",
            "bitwarden_search": "Ansible Vault: default",
            "bitwarden_password_options": "-uln --length 20",
        }


def encode(data):
    """Base64 encode a compact data structure"""
    return b64encode((json.dumps(data, separators=(",", ":")) + "\n").encode()).decode()


def bw(command, session_key=None):
    """
    Run a Bitwarden CLI command, with a temporary session key if necessary.

    Prompts for username/password will be output to STDERR for manual
    input via STDIN when needed.
    """
    command = [BW] + shplit(command)
    if session_key:
        command += ["--session", session_key]
    with subprocess.Popen(
        command,
        stdin=sys.stdin,
        stdout=subprocess.PIPE,
        stderr=sys.stderr,
    ) as process:
        output = process.stdout.read()
        return_code = process.wait()
        if return_code:
            return None
        else:
            try:
                return json.loads(output)
            except:
                return output.decode().strip()


def main():
    parser = ArgumentParser(description="Manage Ansible Vault passwords with Bitwarden")

    parser.add_argument(
        "--vault-id",
        action="store",
        default=None,
        dest="vault_id",
        help="The vault_id for the entry to get from Bitwarden",
    )
    parser.add_argument(
        "--set",
        action="store_true",
        default=False,
        dest="set_password",
        help="set the password instead of getting it",
    )

    args = parser.parse_args()

    vault_config = get_vault_config(args.vault_id)
    title = vault_config["bitwarden_search"]

    if args.set_password:
        # Ensure Bitwarden is unlocked and ready to use
        session_key = None
        status = bw("status")["status"]
        command = {
            "unauthenticated": "login --raw",
            "locked": "unlock --raw",
        }.get(status)
        if command:
            session_key = bw(command)

        password = bw(
            "generate {options}".format(
                options=vault_config.get(
                    "bitwarden_password_options", "-ulns --length 20"
                )
            )
        )
        item = bw("get item '{title}'".format(title=title), session_key=session_key)
        if not item:
            # create a new item
            item = bw("get template item", session_key=session_key)
            item["name"] = title
            item["notes"] = None

        login = item["login"]
        if not login:
            login = bw("get template item.login", session_key=session_key)

        login["username"] = args.vault_id
        old_password = login["password"]
        login["password"] = password
        login["totp"] = None

        item["login"] = login

        data = encode(item)
        if "id" in item:
            bw(
                "edit item {id} {data}".format(id=item["id"], data=data),
                session_key=session_key,
            )
            print(
                "Updated '{old_password}' to '{password}'.".format(
                    old_password=old_password, password=password
                ),
                file=sys.stderr,
            )
        else:
            bw("create item {data}".format(data=data), session_key=session_key)
            print("Created.", file=sys.stderr)

    else:
        password = bw("get password '{title}'".format(title=title))
        if not password:
            print(
                "{prog} could not find Bitwarden entry: '{title}'".format(
                    prog=Path(sys.argv[0]).name, title=title
                ),
                file=sys.stderr,
            )
            sys.exit(KEYNAME_UNKNOWN_RC)
        print(password)


if __name__ == "__main__":
    main()
