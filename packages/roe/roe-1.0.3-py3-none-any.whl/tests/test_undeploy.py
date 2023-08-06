from click.testing import CliRunner

from roe.commands import cmd_deploy
from roe.commands.cmd_undeploy import cli
from roe.utilities.errors import *


def test_undeploy_nonlocal():
    """
    Tests that not passing the local flag tells one to contact ChainOpt support.
    """
    runner = CliRunner()
    result = runner.invoke(cli)
    assert isinstance(result.exception, NoLocalFlagError)


def test_undeploy_all():
    """
    Tests undeploying all packages
    """

    runner = CliRunner()
    result = runner.invoke(cli, ["-l", "--all"], input="y\n")
    assert not result.exception
    assert "Are you sure you want to undeploy all packages?" in result.output
    assert "Removed the following packages:" in result.output


def test_undeploy_bad_name():
    """
    Tests undeploying a package that is not already deployed
    """

    runner = CliRunner()
    runner.invoke(cmd_deploy.cli, ['-l', "-q", r'samples/simple_test'])
    result = runner.invoke(cli, ["-l", "-p", "roe-api"], input="y\n")
    assert isinstance(result.exception, PackageExistenceError)


def test_undeploy_no_packages():
    """
    Tests trying to undeploy when no packages are running.
    """
    runner = CliRunner()
    runner.invoke(cli, ["-l", "--all"], input="y\n")
    result = runner.invoke(cli, ["-l", "-p", "roe-api"], input="y\n")
    assert isinstance(result.exception, NoRunningPackagesError)


def test_undeploy_package_success():
    runner = CliRunner()
    runner.invoke(cmd_deploy.cli, ['-l', "-q", r'samples/simple_test'])
    result = runner.invoke(cli, ["-l", "-p", "simple_test"], input="y\n")
    assert not result.exception
    assert "'simple_test' package undeployed." in result.output
