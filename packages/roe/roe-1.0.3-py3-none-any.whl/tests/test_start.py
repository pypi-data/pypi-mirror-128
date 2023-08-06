from click.testing import CliRunner

from roe.commands import cmd_undeploy, cmd_deploy
from roe.commands.cmd_start import cli
from roe.utilities import errors


def test_start_nonlocal():
    """
    Tests that not passing the local flag tells one to contact ChainOpt support.
    """
    runner = CliRunner()
    result = runner.invoke(cli)
    assert isinstance(result.exception, errors.NoLocalFlagError)


def test_start_bad_package():
    """
    Tests when a bad package name is passed as input
    """
    runner = CliRunner()
    # Deploys sample package to ensure something is running
    runner.invoke(cmd_deploy.cli, ['-l', "-q", r'samples/simple_test'])
    result = runner.invoke(cli, ["-l", "-p", "roe-api"])
    assert isinstance(result.exception, errors.PackageExistenceError)


def test_start_no_running_packages():
    """
    Tests when there are no packages running.
    """
    runner = CliRunner()
    # Undeploys ALL packages
    runner.invoke(cmd_undeploy.cli, ["-l", "--all"], input="y\n")
    result = runner.invoke(cli, ["-l", "-p", "roe-api"])
    assert isinstance(result.exception, errors.NoRunningPackagesError)


def test_start_package():
    runner = CliRunner()
    runner.invoke(cmd_deploy.cli, ['-l', "-q", r'samples/simple_test'])
    result = runner.invoke(cli, ["-l", "-p", "simple_test"], input="n\n")
    assert not result.exception
