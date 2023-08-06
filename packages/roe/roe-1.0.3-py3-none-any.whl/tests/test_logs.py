from click.testing import CliRunner

from roe.commands import cmd_deploy
from roe.commands.cmd_logs import cli
from roe.utilities import errors


def test_logs_nonlocal():
    """
    Tests that not passing the local flag tells one to contact ChainOpt support.
    """
    runner = CliRunner()
    result = runner.invoke(cli, "afsdl;kj438094fglk")
    assert isinstance(result.exception, errors.NoLocalFlagError)


def test_logs_no_package():
    """
    Tests what happens when no package name is passed through
    """
    runner = CliRunner()
    result = runner.invoke(cli)
    assert isinstance(result.exception, SystemExit)
    assert result.exit_code == 2


def test_logs_missing_package():
    """
    Tests when a package name is given that doesn't exist
    """
    runner = CliRunner()
    runner.invoke(cmd_deploy.cli, ['-l', "-q", r'samples/simple_test'])
    result = runner.invoke(cli, ["-l", "roe-api"])
    assert isinstance(result.exception, errors.PackageExistenceError)


def test_logs_success():
    runner = CliRunner()
    runner.invoke(cmd_deploy.cli, ['-l', "-q", r'samples/simple_test'])
    result = runner.invoke(cli, ["-l", "simple_test"])
    assert not result.exception
    assert "Logs are available at: " in result.output
