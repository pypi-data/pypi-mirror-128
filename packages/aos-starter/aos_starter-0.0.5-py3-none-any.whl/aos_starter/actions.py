from pathlib import PurePath, Path

from aos_keys.actions import new_token_user, UserType
from aos_keys.errors import AosKeysError
from aos_prov.actions import create_new_unit, install_vbox_sdk


def do_oem_user(domain: str, user_token: str):
    try:
        new_token_user(domain, str(PurePath(Path.home() / '.aos' / 'security')), user_token, UserType.OEM.value, False)
    except AosKeysError as ake:
        print('User certificate already exists... skipping')
    install_vbox_sdk()
    create_new_unit('My first Aos Unit')
