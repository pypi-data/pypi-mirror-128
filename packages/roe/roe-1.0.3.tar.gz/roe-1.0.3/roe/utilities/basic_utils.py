import socket
from contextlib import closing

import requests
import yaml

from roe.utilities.errors import *


def load_yaml(stream) -> dict:
    yaml_file = open(stream, "r", encoding="utf-8")
    try:
        cred_yaml = yaml.load(yaml_file, Loader=yaml.Loader)
    except yaml.YAMLError:
        cred_yaml = None
    finally:
        yaml_file.close()
    return cred_yaml


def check_port(port):
    if port:
        if 1023 < int(port) < 65535:
            if port_in_use(int(port)):
                raise BadPortError(f"The port {port} is already in use.")
        else:
            raise BadPortError()
    else:
        port = find_free_port()
    return port


def find_free_port():
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as s:
        s.bind(('localhost', 0))
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        return s.getsockname()[1]


def port_in_use(port) -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('localhost', port)) == 0


def uri_exists_stream(uri: str) -> bool:
    try:
        with requests.get(uri, stream=True) as response:
            try:
                response.raise_for_status()
                return True
            except requests.exceptions.HTTPError:
                return False
    except requests.exceptions.ConnectionError:
        return False
