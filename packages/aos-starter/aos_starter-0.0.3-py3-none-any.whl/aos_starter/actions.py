from pathlib import PurePath, Path

from aos_keys.actions import new_token_user, UserType
from aos_prov.actions import create_new_unit


def do_oem_user(domain: str, user_token: str):
    new_token_user(domain, str(PurePath(Path.home() / '.aos' / 'security')), user_token, UserType.OEM.value, False)
    create_new_unit('My first Aos Unit')
