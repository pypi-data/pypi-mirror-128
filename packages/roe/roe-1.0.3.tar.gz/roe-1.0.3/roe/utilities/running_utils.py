# Copyright 2021 Chainopt LLC.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import json
import os
import shutil
import time
from pathlib import Path

import click
import numpy as np
import pandas as pd
import yaml

from roe.utilities import loader, init_utils, basic_utils
from roe.utilities.RoeClient import RoeClient
from roe.utilities.errors import *


def get_package_url(package_name: str):
    roe_client = RoeClient()
    dfAllContainers = roe_client.get_containers()

    dfRunningContainers = dfAllContainers[dfAllContainers['State'] == 'running']
    launch_url = 'http://localhost:' + str(dfRunningContainers[dfRunningContainers['Names'] == package_name]
                                           .iloc[0]['Ports'].split(":")[1].split("-")[0])
    return launch_url


def begin_packages(local):
    roe_client = RoeClient()
    dfAllContainers = roe_client.get_containers()
    if not dfAllContainers.empty:
        dfStoppedContainers = dfAllContainers[dfAllContainers['State'] == 'exited']
        if not dfStoppedContainers.empty:
            checkStart = input("Would you like to start all stopped packages? Enter Y to confirm: ").lower()
            if checkStart == 'y':
                start(local, package_name=None, all=True)


def end(local):
    if not local:
        raise NoLocalFlagError()

    docker_client = init_utils.docker_client_init()

    myContainers = docker_client.containers(all=True)
    for i in myContainers:
        # look for the roe-api container running locally and remove it.
        if i['Names'][0] == '/roe-api':
            list_packages(local)
            end_packages(local)
            docker_client.remove_container(i, force=True)
            click.echo("ROE has ended. To restart, simply run the 'roe begin -l' command.")
            return
    raise AlreadyEndedError()


def end_packages(local):
    roe_client = RoeClient()

    dfAllContainers = roe_client.get_containers()
    if not dfAllContainers.empty:
        dfRunningContainers = dfAllContainers[dfAllContainers['State'] == 'running']
        if not dfRunningContainers.empty:
            checkDelete = input("Would you like to stop all running packages? Enter Y to confirm: ").lower()
            if checkDelete == 'y':
                stop(local, package_name=None, all=True)


def deploy(local, package_name, folder_path, port, quick_deploy):
    folder_name, full_path = package_path_check(folder_path)

    # Use folder name as package name if not specified
    if not package_name:
        package_name = folder_name

    # Check if deployment is local
    if not local:
        raise NoLocalFlagError()

    # Create roe_client
    roe_client = RoeClient()

    dfPackages = roe_client.get_packages()

    # Check if there are packages or if the package is already deployed
    if dfPackages.empty:
        redeploy_bool = False
    elif package_name not in dfPackages.get("Name").values:
        redeploy_bool = False
    else:
        redeploy_bool = True
        click.echo("Package named '" + package_name + "' found.")
        if not quick_deploy:
            check_quick_deploy = input(
                "Would you like to redeploy the package? Enter Y to confirm: ").lower()
            if check_quick_deploy == 'y':
                quick_deploy = True
            else:
                raise DuplicatePackageError()

    # Check the port or create a new port designation if not a redeployment
    if not redeploy_bool:
        port = basic_utils.check_port(port)

    # loader shows progress with begin title, end title and timer. It has been customized.
    loader_text = ["D", "Red"][redeploy_bool] + "eploying Package:"
    loader1 = loader.Loader(loader_text,
                            "The `" + package_name + "` package is deployed!",
                            "`" + package_name + "` model API has failed to deploy.",
                            0.05).start()

    if redeploy_bool:
        dfAllContainers = roe_client.get_containers()
        if dfAllContainers.empty or package_name not in dfAllContainers.Names.values:
            roe_client.delete_package(package_name)
            loader1.quit()
            deploy(local, package_name, folder_path, port, quick_deploy)
            return

        # delete the package
        try:
            roe_client.delete_package(package_name)
        except APIError:
            loader1.failed()
            raise

    # Upload the package
    upload_package(folder_path, folder_name, package_name, roe_client)

    # Verify the package is good to run
    requirements_exists, model_successes, model_failures, non_model_folders = parse_verify(roe_client, package_name)
    verify_failure = not requirements_exists or not model_successes or model_failures
    if verify_failure:
        loader1.failed()
        if not requirements_exists:
            click.secho("Requirements.txt needs to be configured at root of package.", bg="red", fg="white")
        if model_failures:
            click.secho("Failed model folders and issues:\n", bg="red", fg="white")
            click.secho(yaml.dump(model_failures), bg="red", fg="white")
        elif not model_successes:
            click.secho("Unable to find any properly model folders with a config.yaml file", bg="red", fg="white")
        roe_client.delete_package(package_name)
        raise PackageVerifyError()

    if redeploy_bool:
        # restart the api container with updated package
        try:
            roe_client.start(package_name)
        except PackageStartError:
            loader1.failed()
            raise

        launch_url = get_package_url(package_name)

    else:
        launch_url = 'http://localhost:' + str(port)
        try:
            roe_client.deploy(package_name, port)
        except (PackageNameConflictError, APIError):
            loader1.failed()
            roe_client.delete_package(package_name)
            raise

    # check if the url is actually up.
    while not basic_utils.uri_exists_stream(launch_url):
        # If it doesn't come up and container fails, check if container has stopped.
        dfAllContainers = roe_client.get_containers()
        if not dfAllContainers.empty:
            dfStoppedContainers = dfAllContainers[dfAllContainers['State'] == 'exited']
            if not dfStoppedContainers.empty:
                # If container has stopped save logs and clean up container garbage.
                if package_name in dfStoppedContainers.Names.values:
                    loader1.failed()
                    failure_state_logs(roe_client, package_name)
                    return

    # once out of while loop, assign work based on url being up or down.
    loader1.stop()
    click.echo("URL: " + launch_url)
    if not quick_deploy:
        click.pause("Press any key to launch in browser!")
        click.launch(launch_url)
    return


def undeploy(local, package_name, all):
    if not local:
        raise NoLocalFlagError()

    roe_client = RoeClient()

    # if all isn't specified and a package_name is given
    if not all and package_name:
        # List of Docker containers deployed
        dfAllContainers = roe_client.get_containers()

        # List of packages in the roe-packages volume
        dfPackages = roe_client.get_packages()

        # Check if there's nothing
        if dfAllContainers.empty and dfPackages.empty:
            raise NoRunningPackagesError()
        # Ensures we don't get DataFrame errors
        elif not dfAllContainers.empty:
            if package_name in dfAllContainers.Names.values:
                checkDelete = input("Would you like to stop and delete the package? Enter Y to confirm: ").lower()
                if checkDelete == 'y':
                    roe_client.delete_both(package_name)
                    click.echo(f"'{package_name}' package undeployed.")
                    return
                else:
                    click.echo(f"'{package_name}' is still running.")
        # Checks for orphaned packages
        if package_name in dfPackages.Name.values:
            roe_client.delete_package(package_name)
            click.echo(f"'{package_name}' package undeployed.")
        # Package must not exist in this case
        else:
            raise PackageExistenceError(package_name)

    # all is an optional flag that requests to  delete all packages
    elif all:
        checkUndeploy = input(
            "Are you sure you want to undeploy all packages? (This cannot be undone.) Enter Y to confirm: ").lower()
        if checkUndeploy == 'y':
            roe_client.delete_all()
        else:
            click.echo("Undeploy all aborted.")
    else:
        raise MissingPackageInputError()

    return


def stop(local, package_name, all):
    if not local:
        raise NoLocalFlagError()

    roe_client = RoeClient()

    # get list of deployed packages that are running
    dfContainers = roe_client.get_containers()
    if dfContainers.empty:
        raise NoRunningPackagesError()

    if all:
        for package in dfContainers.Names.values:
            roe_client.stop(package)
            click.echo("The '" + package + "' package has been stopped.")
    # check if package exists in list and stop it.
    elif package_name:
        if package_name in dfContainers.Names.values:
            roe_client.stop(package_name)
            click.echo("The '" + package_name + "' package has been stopped.")
        else:
            raise PackageExistenceError(package_name)
    else:
        raise MissingPackageInputError()


def start(local, package_name, all):
    if not local:
        raise NoLocalFlagError()
    roe_client = RoeClient()

    # Get all containers
    dfContainers = roe_client.get_containers()
    if dfContainers.empty:
        raise NoRunningPackagesError()

    if all:
        for package in dfContainers.Names.values:

            # If starting a package fails let the user know and move on
            try:
                start_package(roe_client, package)
            except PackageStartError as e:
                click.echo(e.message)

    # Check if package exists in list and start it.
    elif package_name:
        if package_name in dfContainers.Names.values:
            start_package(roe_client, package_name)
        else:
            raise PackageExistenceError(package_name)
    else:
        raise MissingPackageInputError()


def start_package(roe_client: RoeClient, package_name: str):
    roe_client.start(package_name)
    launch_url = get_package_url(package_name)

    # wait till package starts up to confirm
    while not basic_utils.uri_exists_stream(launch_url):
        dfAllContainers = roe_client.get_containers()
        if not dfAllContainers.empty:
            dfStoppedContainers = dfAllContainers[dfAllContainers['State'] == 'exited']

            # check if package container has errored out to stop waiting
            if not dfStoppedContainers.empty and package_name in dfStoppedContainers.Names.values:
                click.echo("Failed to start the package.")
                failure_state_logs(roe_client, package_name)
                return

    click.echo(f"Successfully restarted the package {package_name}")


def list_packages(local: bool):
    if not local:
        raise NoLocalFlagError()

    roe_client = RoeClient()

    # get list of uploaded packages
    dfPackages = roe_client.get_packages()

    # get list of deployed packages
    dfContainers = roe_client.get_containers()

    click.echo("--------------------")
    # somehow give a list back to the user, but only one consolidated list.
    if dfPackages.empty and dfContainers.empty:
        click.echo("No packages deployed.")
    elif dfContainers.empty:
        if len(dfPackages) == 1:
            click.echo(str(len(dfPackages)) + ' package:')
        elif len(dfPackages) > 1:
            click.echo(str(len(dfPackages)) + ' packages:')
        click.echo("--------------------")
        dfPackages.index = np.arange(1, len(dfPackages) + 1)
        click.echo(dfPackages)
        click.echo('Note: Showing limited information')
    else:
        # Ideally, this is the list called on at all times.
        # Each package should map to a running or stopped container.
        if len(dfContainers) == 1:
            click.echo(str(len(dfContainers)) + ' package:')
        elif len(dfContainers) > 1:
            click.echo(str(len(dfContainers)) + ' packages:')
        click.echo("--------------------")
        dfResult = pd.merge(dfContainers, dfPackages, left_on=['Names'], right_on=['Name'], how='inner')
        # Create clean url that can be clicked.
        dfResult['Ports'] = dfResult['Ports'] \
            .apply(lambda x: 'http://localhost:' + str(x)
                   .split(":")[1].split("-")[0] if not pd.isnull(x) else 'None')
        dfResult = dfResult.rename(columns={"Names": "Name", "Ports": "url", "Created": "Last Started",
                                            "LastModified": "Last Updated"})
        dfResult = dfResult.reset_index(drop=True)
        # Number the packages properly
        dfResult.index = np.arange(1, len(dfResult) + 1)
        click.echo(dfResult)
    click.echo("--------------------")


def logs(local, package_name, tail):
    if local:
        roe_client = RoeClient()

        # get all containers
        dfContainers = roe_client.get_containers()

        # find the container to get logs from
        if not dfContainers.empty:
            if package_name in dfContainers.Names.values:
                generate_logs(roe_client, package_name, tail)
            else:
                raise PackageExistenceError(package_name)
        else:
            raise NoRunningPackagesError()
    else:
        raise NoLocalFlagError()
    return


def failure_state_logs(roe_client: RoeClient, package_name: str):
    """ Generates logs and cleans up package and container data """
    checkLogs = input("Would you like to save the logs? Enter Y to confirm: ").lower()
    if checkLogs == 'y':
        generate_logs(roe_client, package_name)
    else:
        click.echo("Logs not generated")
    roe_client.delete_both(package_name)
    return


def generate_logs(roe_client: RoeClient, package_name: str, tail: str = None):
    """ Function for generating logs after a failed container method. """

    logs_dir = os.path.join(init_utils.ROE_DIR, "logs")
    if not os.path.isdir(logs_dir):
        os.makedirs(logs_dir)

    raw_logs = roe_client.logs(package_name, tail)
    logs_text = raw_logs.replace("\n\n", "\n").replace("\n\n", "\n")
    # Generate filename with timestamp
    file_name = os.path.join(logs_dir, package_name + "-" + time.strftime("%Y%m%d-%H%M%S") + "-running-logs.txt")
    with open(file_name, "w", encoding="utf-8") as log_file:
        log_file.write(logs_text)
        log_file.close()
    click.echo("Logs are available at: " + file_name)


def package_path_check(folder_path):
    # Check if folder name exists
    full_path = Path(folder_path).resolve()
    if not full_path.is_dir():
        raise PackagePathError()
    # Get folder name from specified path
    folder_name = full_path.name
    return folder_name, full_path


def upload_package(folder_path: str, folder_name: str, package_name: str, roe_client: RoeClient):
    target_dir = Path(folder_path).resolve().parent

    # Compress package
    archive_path = shutil.make_archive(folder_name, 'zip', target_dir, folder_name)

    # Upload files to API
    roe_client.upload(package_name, archive_path)

    os.remove(archive_path)


def dupe_upload_handler(full_path, package_name, roe_client):
    """ Handles duplicate package names when uploading the package """
    # Get list of all packages uploaded
    dfPackages = roe_client.get_packages()

    # Checks for an empty list of packages and then if the package is a duplicate
    if not dfPackages.empty:
        if package_name in dfPackages["Name"].values:
            # We iterate through numbers to append to ensure that we have a unique package name.
            new_package_name = package_name
            append = 0
            while new_package_name in dfPackages["Name"].values:
                append += 1
                new_package_name = package_name + f"_{append}"
            new_full_path = os.path.dirname(full_path) + f"\\{new_package_name}"
            os.rename(full_path, new_full_path)
            upload_package(new_full_path, new_package_name, new_package_name, roe_client)
            os.rename(new_full_path, full_path)
            return new_package_name

    upload_package(full_path, package_name, package_name, roe_client)
    return package_name


def verify(local: bool, package_path: str):
    if not local:
        raise NoLocalFlagError()

    roe_client = RoeClient()

    # Checks and creates variables to upload the package
    package_name, full_path = package_path_check(package_path)

    # Uploads package to the
    package_name = dupe_upload_handler(full_path, package_name, roe_client)

    requirements_exists, model_successes, model_failures, non_model_folders = parse_verify(roe_client, package_name)

    # Delete the package once verification completes
    roe_client.delete_package(package_name)

    if requirements_exists:
        click.secho("Requirements.txt successfully found.\n", bg="green", fg="white")
    else:
        click.secho("Requirements.txt needs to be configured at root of package.\n", bg="red", fg="white")
    if model_failures:
        click.secho("Failed model folders and issues:\n", bg="red", fg="white")
        click.secho(yaml.dump(model_failures), bg="red", fg="white")
    if model_successes:
        click.secho("Successfully verified model folders:", bg="green", fg="white")
        [click.secho(x, bg="green", fg="white") for x in model_successes]
    elif not model_failures:
        click.secho("No model folders with a config.yaml were found!", bg="red", fg="white")
    if non_model_folders:
        click.secho("\nThe following were seen as non-model folders:", bg="yellow", fg="white")
        [click.secho(x, bg="yellow", fg="white") for x in non_model_folders]
    return


def parse_verify(roe_client, package_name):
    # Verify the package and return either the verbose output or simply the
    verify_response = roe_client.verify(package_name)

    # Load the API response as a dictionary
    response_dict = json.loads(verify_response)
    # Generate containers for each of the directory checks
    model_successes = response_dict["model_successes"]
    model_failures = response_dict["model_failures"]
    non_model_folders = response_dict["non_model_folders"]
    requirements_exists = response_dict["requirements.txt"]
    return requirements_exists, model_successes, model_failures, non_model_folders
