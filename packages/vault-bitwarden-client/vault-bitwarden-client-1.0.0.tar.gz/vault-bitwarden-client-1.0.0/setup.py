# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['vault_bitwarden_client']
entry_points = \
{'console_scripts': ['vault-bitwarden-client = vault_bitwarden_client:main']}

setup_kwargs = {
    'name': 'vault-bitwarden-client',
    'version': '1.0.0',
    'description': 'Use Bitwarden to unlock Ansible vaults',
    'long_description': '# Ansible Vault Bitwarden Client\n\nUse Bitwarden to unlock Ansible vaults.\n\n## Description\n\nAs described in [Storing and accessing vault passwords][vault-docs], Ansible has the\nability to retrieve vault passwords from third-party tools using a client script. This\nscript implements the client interface for retrieving passwords from Bitwarden.\n\n## Requirements\n\n- Ansible\n- `bw` [Bitwarden CLI][bw-cli] tool\n\n## Installation\n\n    pip install --user vault-bitwarden-client\n\nFrom source:\n\n    pip install --user /path/to/repos/vault-bitwarden-client\n\nYou can also run the script directly, without installing it:\n\n    python3 /path/to/repos/vault-vitwarden-client/vault_bitwarden_client.py --help\n\n## Setup\n\nBitwarden entries for your vaults must have names containing "Ansible Vault: $vault_id"\nand the vault-id should be saved as the username. Use `default` as the username when no\nvault-id is being used. For example:\n\n- **Name:** Ansible Vault: dev\n- **Username:** dev\n- **Password:** S3kr1t\n\nEntries should have unique names; as only the first matching entry will be used. The\nvalue for the default vault-id and the Bitwarden search string are both configurable in\nyour `ansible.cfg` file, as documented below.\n\nIn order to not be prompted for your Bitwarden password every time, you can update your\nenvironment with your session key. For example:\n\n### Bash\n```bash\nexport BW_SESSION=$(bw unlock --raw)\n```\n\n### Fish\n```fish\nset -Ux BW_SESSION (bw unlock --raw)\n```\n\nOtherwise, you will be prompted for your password the same as if you were executing `bw`\non the command line.\n\n## Usage\n\nYou can call the script directly:\n\n```bash\nansible-vault --vault-id dev@$(command -v vault-bitwarden-client) view some_encrypted_file\n\nansible-playbook --vault-password-file $(command -v vault-bitwarden-client) playbook.yml\n```\nSet it in your environment:\n\n```bash\nexport ANSIBLE_VAULT_PASSWORD_FILE=$(command -v vault-bitwarden-client)\n\nansible-vault --vault-id dev view some_encrypted_file\n\nansible-playbook playbook.yml\n```\n\nOr configure it in your `ansible.cfg` file:\n\n```conf\n[defaults]\nvault_password_file = ~/.local/bin/vault-bitwarden-client\n\n# Optional:\n[vault]\nbitwarden_search = Ansible Vault: %(vault_id)s\nbitwarden_default_id = default\n```\n\nIn addition to creating Bitwarden entries manually, you can set passwords using this script:\n\n```bash\nvault-bitwarden-client --set                 # Sets \'default\' password\nvault-bitwarden-client --vault-id dev --set  # Sets \'dev password\n```\n\nYou can set the `bitwarden_password_options` in your `ansible.cfg` file to override the\ndefault password generator options, which are `-ulns --length 20`.\n\nChanging an existing entriy\'s password will output the old password and the new password\nto facilitate rekeying existing vault files.\n\n\n[vault-docs]: https://docs.ansible.com/ansible/latest/user_guide/vault.html#storing-and-accessing-vault-passwords\n[bw-cli]: https://bitwarden.com/help/article/cli/\n',
    'author': 'Philip Douglass',
    'author_email': 'philip@philipdouglass.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'entry_points': entry_points,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
