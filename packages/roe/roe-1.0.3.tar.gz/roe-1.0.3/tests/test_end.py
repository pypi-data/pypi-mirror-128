from click.testing import CliRunner

from roe.commands import cmd_begin, cmd_deploy
from roe.commands.cmd_end import cli
from roe.utilities.errors import *


def test_end_nonlocal():
    """
    Tests that not passing the local flag tells one to contact ChainOpt support.
    """
    runner = CliRunner()
    result = runner.invoke(cli)
    assert isinstance(result.exception, NoLocalFlagError)


def test_end_not_running():
    """
    Tests to ensure that when there's no image running locally that there will be the proper output.
    """
    runner = CliRunner()
    # First runs the command to ensure that if ROE is running we stop it first.
    runner.invoke(cli, "-l", input="n\n\n")
    result = runner.invoke(cli, "-l")
    assert isinstance(result.exception, AlreadyEndedError)
    assert "ROE was not running. To restart, simply run the 'roe begin -l' command." in result.output


def test_end_base():
    """
    Base case where we end the local roe instance that was already running.
    """
    runner = CliRunner()
    # First ensure that ROE is running
    runner.invoke(cmd_begin.cli, "-l", input="y\n")
    result = runner.invoke(cli, "-l", input="y\n")
    assert not result.exception
    assert "ROE has ended. To restart, simply run the 'roe begin -l' command.\n" in result.output


def test_end_stop():
    runner = CliRunner()
    runner.invoke(cmd_deploy.cli, ['-l', "-q", r'./samples/simple_test'])
    result = runner.invoke(cli, "-l", input="y\n")
    assert not result.exception
    assert "Would you like to stop all running packages? Enter Y to confirm:" in result.output
