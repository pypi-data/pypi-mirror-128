import os
import socket

import pytest

from roe.utilities import errors, basic_utils, loader


def test_bad_yaml_load():
    """ Tests when a poorly configured YAML file is given. """
    filename = "bad.yaml"
    with open(filename, "w") as bad_yaml:
        bad_yaml.write("aaslvclk:fjas;lk:jflask:klsfdj:\n\n\n:fkdlj")
        bad_yaml.close()
    result = basic_utils.load_yaml(os.path.join(os.getcwd(), filename))

    os.remove(filename)
    assert result is None


def test_check_port_good():
    port = 65000
    result = basic_utils.check_port(port)
    assert result == port


def test_check_port_existing():
    # Creates temporary socket on the port, then raises the BadPortError properly
    port = 65000
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as test_socket:
        location = ('', port)
        test_socket.bind(location)
        test_socket.listen(1)
        with pytest.raises(errors.BadPortError):
            basic_utils.check_port(port)


def test_uri_stream_bad():
    assert not basic_utils.uri_exists_stream('https://test')


def test_loader():
    load = loader.Loader()
    load.quit()
