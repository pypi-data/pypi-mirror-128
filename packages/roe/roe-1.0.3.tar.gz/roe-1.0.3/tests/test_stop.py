from click.testing import CliRunner

from roe.commands import cmd_deploy
from roe.commands.cmd_stop import cli
from roe.utilities.errors import *


def test_stop_nonlocal():
    """
    Tests that not passing the local flag tells one to contact ChainOpt support.
    """
    runner = CliRunner()
    result = runner.invoke(cli)
    assert isinstance(result.exception, NoLocalFlagError)


def test_stop_base():
    """
    Tests the stopping of a deployed package
    """
    runner = CliRunner()
    runner.invoke(cmd_deploy.cli, ['-l', "-q", r'./samples/simple_test'])
    result = runner.invoke(cli, ["-l", "-p", "simple_test"])
    assert not result.exception
    assert "package has been stopped" in result.output


def test_stop_missing_input():
    """
    Tests running command with no input
    """
    runner = CliRunner()
    runner.invoke(cmd_deploy.cli, ['-l', "-q", r'./samples/simple_test'])
    result = runner.invoke(cli, ["-l"])
    assert isinstance(result.exception, MissingPackageInputError)
    assert "Please specify a package name or --all." in result.output