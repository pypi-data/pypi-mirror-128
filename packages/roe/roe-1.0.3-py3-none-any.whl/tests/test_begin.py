import os

from click.testing import CliRunner

from roe.commands import cmd_deploy, cmd_stop
from roe.commands.cmd_begin import cli
from roe.utilities import errors


def test_cmd_begin():
    """
    Tests that simply running with the local flag starts ROE
    """
    runner = CliRunner()
    result = runner.invoke(cli, ["-l"], input="y\n")
    assert not result.exception
    assert "ROE is now ready" in result.output
    assert "Loading credentials from: " in result.output


def test_cmd_begin_nonlocal():
    """
    Tests that not passing the local flag tells one to contact ChainOpt support.
    """
    runner = CliRunner()
    result = runner.invoke(cli)
    assert isinstance(result.exception, errors.NoLocalFlagError)


def test_begin_good_creds():
    """
    Tests if passing through good creds successfully deploys ROE fully.
    """
    runner = CliRunner()
    # We will pass through  previously saved credentials in the Documents folder, set up as stated in the README
    cred_path = os.path.join(os.path.join(os.path.join(os.path.expanduser("~"), "Documents"), "ROE"),
                             "test-credentials.yaml")
    result = runner.invoke(cli, ["-l", "-f", cred_path], input="y\n")

    # Checks for    1) no errors
    #               2) completion of beginning the API container
    #               3) Loading the credentials from the file
    #               4) Ensuring it didn't try to load credentials from previously saved location
    assert not result.exception
    assert "ROE is now ready" in result.output
    assert "Loading credentials from file:" in result.output
    assert "These credentials are used to check" not in result.output


def test_begin_bad_creds():
    """
    Tests handling of bad given Docker credentials
    """
    runner = CliRunner()
    result = runner.invoke(cli, ["-l", "-f", r"./samples/credentials.yaml"])
    # Checks for    1) no errors
    #               2) Failed creds
    #               3) Loading the credentials from the default saved file
    #               4) Ensure Credentials succeed
    #               5) Ensure API begins
    assert not result.exception
    assert "Provided credentials file failed to authenticate." in result.output
    assert "Loading credentials from: " in result.output
    assert "Saved credentials file failed to authenticate." not in result.output
    assert "ROE is now ready" in result.output


def test_begin_bad_creds_input_no_saved():
    """
    Tests what happens when all credentials served are bad
    """
    runner = CliRunner()
    # We're going to need to mess with the saved file, then change it back at the end so that we can emulate not having
    # the previously saved credentials file
    cred_path = os.path.join(os.path.join(os.path.join(os.path.expanduser("~"), "Documents"), "ROE"),
                             "credentials.yaml")
    new_path = cred_path + ".old"
    os.rename(cred_path, new_path)
    # Intentionally serve up a bad username, password, and email
    result = runner.invoke(cli, ["-l", "-f", r"./samples/credentials.yaml"], input="username\npassword\n")
    os.rename(new_path, cred_path)
    # Checks for    1) Correct exception raised
    #               2) Provided credentials don't authenticate
    #               3) ROE does not run
    assert isinstance(result.exception, errors.BadCredError)
    assert "Provided credentials file failed to authenticate." in result.output
    assert "ROE is now ready" not in result.output


def test_begin_stopped():
    runner = CliRunner()
    runner.invoke(cmd_deploy.cli, ['-l', "-q", r'./samples/simple_test'])
    runner.invoke(cmd_stop.cli, ["-l", "-p", "simple_test"])
    result = runner.invoke(cli, ['-l'], input='y\n')
    assert not result.exception
    assert 'Would you like to start all stopped packages? Enter Y to confirm:' in result.output
