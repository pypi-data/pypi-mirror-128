from click.testing import CliRunner

from roe.commands import cmd_undeploy
from roe.commands.cmd_deploy import cli
from roe.utilities.errors import *
from roe.utilities.RoeClient import RoeClient


def test_deploy_no_package():
    """
    Tests if ROE properly gives an error if no package is given to deploy.
    """
    runner = CliRunner()
    result = runner.invoke(cli)
    assert isinstance(result.exception, SystemExit)
    assert result.exit_code == 2
    assert "Missing argument" in result.output


def test_deploy_nonlocal():
    """
    Tests that not passing the local flag tells one to contact ChainOpt support.
    """
    runner = CliRunner()
    result = runner.invoke(cli, [r"samples/simple_test"], input="y\n")
    assert isinstance(result.exception, NoLocalFlagError)


def test_deploy_bad_package_path():
    """
    Tests error handling when passing through a bad package name.
    """
    runner = CliRunner()
    result = runner.invoke(cli, ["-l", "asdfljk"])
    assert isinstance(result.exception, PackagePathError)


def test_deploy_base():
    """ Base case for testing the deploy command"""
    runner = CliRunner()
    result = runner.invoke(cli, ["-l", r"samples/simple_test"], input="y\n")
    assert not result.exception


def test_deploy_bad_port():
    runner = CliRunner()
    runner.invoke(cmd_undeploy.cli, ["-l", "--all"], input="y\n")
    result = runner.invoke(cli, ["-l", r"samples/simple_test", "-p", "900"], input="y\n")
    assert isinstance(result.exception, BadPortError)


def test_deploy_no_requirements():
    runner = CliRunner()
    result = runner.invoke(cli, ["-l", r"samples/bad_no_requirements"], input="y\n")
    assert isinstance(result.exception, PackageVerifyError)
    assert "Requirements.txt needs to be configured at root of package." in result.output


def test_deploy_no_config():
    runner = CliRunner()
    result = runner.invoke(cli, ["-l", r"samples/bad_no_config"], input="y\n")
    assert isinstance(result.exception, PackageVerifyError)
    assert "Unable to find any properly model folders with a config.yaml file" in result.output


def test_deploy_bad_config():
    runner = CliRunner()
    result = runner.invoke(cli, ["-l", r"samples/bad_no_config"], input="y\n")
    assert isinstance(result.exception, PackageVerifyError)
    assert "Unable to find any properly model folders with a config.yaml file" in result.output


def test_deploy_failed_no_logs():
    runner = CliRunner()
    result = runner.invoke(cli, ["-l", r"samples/bad_python"], input="n\n")
    assert not result.exception
    assert "Logs not generated" in result.output


def test_deploy_failed_logs():
    runner = CliRunner()
    result = runner.invoke(cli, ["-l", r"samples/bad_python"], input="y\n")
    assert not result.exception
    assert "Logs are available at:" in result.output


def test_non_roe_dupe():
    runner = CliRunner()
    runner.invoke(cli, ["-l", "-q", r"samples/simple_test"], input="y\n")
    RoeClient().delete_package('simple_test')
    result = runner.invoke(cli, ["-l", r"samples/simple_test"], input="y\n")
    assert isinstance(result.exception, PackageNameConflictError)
    runner.invoke(cmd_undeploy.cli, ['-l', '--all'], input="y\n")
