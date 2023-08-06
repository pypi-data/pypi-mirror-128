import pytest

from roe.utilities.RoeClient import RoeClient
from roe.utilities.errors import *

FAKE_URL = "https://google.com"

def test_no_url():
    client = RoeClient()
    assert client.get_base_url()


def test_set_url():
    client = RoeClient(FAKE_URL)
    client.set_base_url(FAKE_URL)
    assert client.get_base_url()
    assert str(client)


def test_bad_url_deploy():
    client = RoeClient(FAKE_URL)
    with pytest.raises(APIError) as exc_info:
        client.deploy('roe', 8081)

    assert 'Deploy' in exc_info.value.args[0]


def test_bad_url_verify():
    client = RoeClient(FAKE_URL)
    with pytest.raises(APIError) as exc_info:
        client.verify('roe')

    assert 'Verify' in exc_info.value.args[0]


def test_bad_url_delete():
    client = RoeClient(FAKE_URL)
    with pytest.raises(APIError) as exc_info:
        client.delete_both('roe')

    assert 'Container Delete' in exc_info.value.args[0] or 'Package Delete' in exc_info.value.args[0]


def test_bad_url_delete_package():
    client = RoeClient(FAKE_URL)
    with pytest.raises(APIError) as exc_info:
        client.delete_package('roe')

    assert 'Package Delete' in exc_info.value.args[0]


def test_bad_url_delete_container():
    client = RoeClient(FAKE_URL)
    with pytest.raises(APIError) as exc_info:
        client.delete_both('roe')

    assert 'Container Delete' in exc_info.value.args[0]


def test_bad_url_delete_all():
    client = RoeClient(FAKE_URL)
    with pytest.raises(APIError) as exc_info:
        client.delete_all()

    assert 'Delete All' in exc_info.value.args[0]


def test_bad_url_undeploy():
    client = RoeClient(FAKE_URL)
    with pytest.raises(APIError) as exc_info:
        client.undeploy('roe')

    assert 'Undeploy' in exc_info.value.args[0]


def test_bad_url_get_containers():
    client = RoeClient(FAKE_URL)
    with pytest.raises(APIError) as exc_info:
        client.get_containers()

    assert 'Container List' in exc_info.value.args[0]


def test_bad_url_get_packages():
    client = RoeClient(FAKE_URL)
    with pytest.raises(APIError) as exc_info:
        client.get_packages()

    assert 'Package List' in exc_info.value.args[0]


def test_bad_url_upload():
    client = RoeClient(FAKE_URL)
    with pytest.raises(APIError) as exc_info:
        client.upload('roe', r'./samples/simple_test/requirements.txt')

    assert 'Upload' in exc_info.value.args[0]


def test_bad_url_logging():
    client = RoeClient(FAKE_URL)
    with pytest.raises(LoggingError) as exc_info:
        client.logs('roe', 100)


def test_bad_url_stop():
    client = RoeClient(FAKE_URL)
    with pytest.raises(PackageStopError) as exc_info:
        client.stop('roe')


def test_bad_url_start():
    client = RoeClient(FAKE_URL)
    with pytest.raises(PackageStartError) as exc_info:
        client.start('roe')
