import os

from click.testing import CliRunner

from roe.commands import cmd_deploy
from roe.commands.cmd_verify import cli
from roe.utilities.errors import *


def test_verify_nonlocal():
    """
    Tests that not passing the local flag tells one to contact ChainOpt support.
    """
    runner = CliRunner()
    result = runner.invoke(cli, "roe-api")
    assert isinstance(result.exception, NoLocalFlagError)


def test_verify_base():
    """ Tests the bast case of verification works """
    runner = CliRunner()
    result = runner.invoke(cli, ["-l", r"samples/simple_test"])
    assert not result.exception
    assert "Requirements.txt successfully found." in result.output
    assert "Failed model" not in result.output
    assert "Successfully verified model folders:\nheart_disease" in result.output
    assert "non-model" not in result.output


def test_verify_empty_dir():
    """ Tests verification with an empty directory """
    runner = CliRunner()
    os.makedirs(r"samples/test_dir")
    result = runner.invoke(cli, ["-l", r"samples/test_dir"])
    os.rmdir(r"samples/test_dir")
    assert not result.exception
    assert "needs to be configured" in result.output
    assert "No model folders with a config.yaml were found!" in result.output


def test_verify_dupe():
    """ Tests verify when there's a matching package already """
    runner = CliRunner()
    runner.invoke(cmd_deploy.cli, ['-l', "-q", r'samples/simple_test'])
    result = runner.invoke(cli, ["-l", r"samples/simple_test"])
    assert not result.exception
    assert "Requirements.txt successfully found." in result.output
    assert "Failed model" not in result.output
    assert "Successfully verified model folders:\nheart_disease" in result.output
    assert "non-model" not in result.output
