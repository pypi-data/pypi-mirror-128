# Ansible Vault Bitwarden Client

Use Bitwarden to unlock Ansible vaults.

## Description

As described in [Storing and accessing vault passwords][vault-docs], Ansible has the
ability to retrieve vault passwords from third-party tools using a client script. This
script implements the client interface for retrieving passwords from Bitwarden.

## Requirements

- Ansible
- `bw` [Bitwarden CLI][bw-cli] tool

## Installation

    pip install --user vault-bitwarden-client

From source:

    pip install --user /path/to/repos/vault-bitwarden-client

You can also run the script directly, without installing it:

    python3 /path/to/repos/vault-vitwarden-client/vault_bitwarden_client.py --help

## Setup

Bitwarden entries for your vaults must have names containing "Ansible Vault: $vault_id"
and the vault-id should be saved as the username. Use `default` as the username when no
vault-id is being used. For example:

- **Name:** Ansible Vault: dev
- **Username:** dev
- **Password:** S3kr1t

Entries should have unique names; as only the first matching entry will be used. The
value for the default vault-id and the Bitwarden search string are both configurable in
your `ansible.cfg` file, as documented below.

In order to not be prompted for your Bitwarden password every time, you can update your
environment with your session key. For example:

### Bash
```bash
export BW_SESSION=$(bw unlock --raw)
```

### Fish
```fish
set -Ux BW_SESSION (bw unlock --raw)
```

Otherwise, you will be prompted for your password the same as if you were executing `bw`
on the command line.

## Usage

You can call the script directly:

```bash
ansible-vault --vault-id dev@$(command -v vault-bitwarden-client) view some_encrypted_file

ansible-playbook --vault-password-file $(command -v vault-bitwarden-client) playbook.yml
```
Set it in your environment:

```bash
export ANSIBLE_VAULT_PASSWORD_FILE=$(command -v vault-bitwarden-client)

ansible-vault --vault-id dev view some_encrypted_file

ansible-playbook playbook.yml
```

Or configure it in your `ansible.cfg` file:

```conf
[defaults]
vault_password_file = ~/.local/bin/vault-bitwarden-client

# Optional:
[vault]
bitwarden_search = Ansible Vault: %(vault_id)s
bitwarden_default_id = default
```

In addition to creating Bitwarden entries manually, you can set passwords using this script:

```bash
vault-bitwarden-client --set                 # Sets 'default' password
vault-bitwarden-client --vault-id dev --set  # Sets 'dev password
```

You can set the `bitwarden_password_options` in your `ansible.cfg` file to override the
default password generator options, which are `-ulns --length 20`.

Changing an existing entriy's password will output the old password and the new password
to facilitate rekeying existing vault files.


[vault-docs]: https://docs.ansible.com/ansible/latest/user_guide/vault.html#storing-and-accessing-vault-passwords
[bw-cli]: https://bitwarden.com/help/article/cli/
