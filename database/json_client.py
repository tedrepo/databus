from client.client import Client
from config.constants import *
from os import path, scandir
from typing import List


def build_client_dir_path(p_client: Client) -> str:
    client_root_path = build_client_root_path()
    return path.join(client_root_path, p_client.name)


def build_client_root_path() -> str:
    return path.join(JSON_DB_DATABASE_DIR, JSON_DB_CLIENT_DIR)


def get_client_directories() -> List[str]:
    return [f.name for f in scandir(build_client_root_path()) if f.is_dir()]