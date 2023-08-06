import os

import click
import docker
import keyring
import requests
import stdiomask
import yaml
from docker.utils import kwargs_from_env

from roe.utilities import loader, basic_utils
from roe.utilities.errors import *

ROE_DIR = os.path.join(os.path.join(os.path.expanduser("~"), "Documents"), "ROE")


def docker_client_init():
    try:
        return docker.APIClient(**kwargs_from_env())
    except docker.errors.DockerException:
        raise DockerNotRunningError()


def get_roe_url():
    docker_client = docker_client_init()
    roe_port = None
    for i in docker_client.containers():
        if i['Names'][0] == '/roe-api':
            roe_port = i['Ports'][0]['PublicPort']
            break
    if roe_port:
        base_url = 'http://localhost:' + str(roe_port)
    else:
        begin(local=True, file=None)
        base_url = get_roe_url()
    return base_url


def begin(local, file):
    if not local:
        raise NoLocalFlagError()

    # specify version here or use 'latest'
    api_version = 'latest'

    try:
        docker_client, docker_creds = login(file, api_version)
    except docker.errors.DockerException:
        raise DockerNotRunningError()

    loader_animation = loader.Loader("Setting up local deployment services..",
                                     "ROE is now ready to deploy your model.",
                                     0.05).start()

    # Custom function in utils to find a free port on local
    roe_port = basic_utils.find_free_port()

    # check if ROE is already running locally. If it is, then remove it.
    myContainers = docker_client.containers(all=True)
    for i in myContainers:
        if i['Names'][0] == '/roe-api':
            docker_client.remove_container(i, force=True)

    # Create the "roe-packages" volume if it does not already exist
    volume_name = "roe-packages"

    # create the roe-api local deployment docker container and specify ports and volume bindings.
    container = docker_client.create_container(name='roe-api', image='chainopt/roe-api:' + api_version,
                                               stdin_open=True,
                                               tty=True,
                                               environment=docker_creds,
                                               volumes=['/var/run/docker.sock', '/var/roe-packages'], ports=[80],
                                               host_config=docker_client.create_host_config(binds={
                                                   '/var/run/docker.sock': {'bind': '/var/run/docker.sock',
                                                                            'mode': 'rw', },
                                                   volume_name: {'bind': '/var/roe-packages', 'mode': 'rw', }},
                                                   port_bindings={80: roe_port}))

    docker_client.start(container)

    while not basic_utils.uri_exists_stream(get_roe_url()):
        # wait for roe to start up
        pass

    loader_animation.stop()

    return


def login(file: str, api_version: str):
    """
    Handles the sequence of trying different credential files to gain access to DockerHub
    """

    # Instantiate the default credentials path and ROE folder
    if not os.path.isdir(ROE_DIR):
        os.makedirs(ROE_DIR)
    cred_path = os.path.join(ROE_DIR, "credentials.yaml")

    # Check if a filename was passed through
    if file:
        click.echo("Loading credentials from file: " + file)
        docker_creds = basic_utils.load_yaml(file)
        try:
            return cred_check(docker_creds, cred_path, api_version)
        except requests.exceptions.HTTPError:
            click.echo("Provided credentials file failed to authenticate.")
        except DockerHubAccountError:
            click.echo("Provided credentials do not have access to the API on Docker Hub."
                       " Please use the correct account.")

    # Check if credentials were previously successfully provided.
    if os.path.exists(cred_path):
        click.echo("Loading credentials from: " + cred_path)
        docker_creds = basic_utils.load_yaml(cred_path)
        docker_creds["docker_pw"] = keyring.get_password("ROE", docker_creds["docker_user"])
        try:
            return cred_check(docker_creds, cred_path, api_version)
        except requests.exceptions.HTTPError:
            click.echo("Saved credentials failed to authenticate.")
        except DockerHubAccountError:
            click.echo("Saved credentials do not have access to the API on Docker Hub. Please use the correct account.")
    # Final solution is to ask for credentials
    click.echo("These credentials are used to check if you have access to ChainOpt artifacts on Docker Hub.")
    docker_creds = dict()
    docker_creds["docker_user"] = input("Enter your Docker Username: ")
    docker_creds["docker_pw"] = stdiomask.getpass(prompt='Enter your Docker Password: ', mask='*')
    try:
        return cred_check(docker_creds, cred_path, api_version)
    except requests.exceptions.HTTPError:
        raise BadCredError()


def cred_check(docker_creds, cred_path, api_version):
    # Get local docker client setup
    docker_client = docker_client_init()

    docker_client.login(username=docker_creds.get("docker_user"), password=docker_creds.get("docker_pw"))

    # Check if account has access to Docker Hub API image
    try:
        docker_client.pull('chainopt/roe-api', tag=api_version)
    except docker.errors.ImageNotFound:
        raise DockerHubAccountError()

    # Only save credentials to a file if they work.
    keyring.set_password("ROE", docker_creds["docker_user"], docker_creds["docker_pw"])
    with open(cred_path, 'w') as f:
        yaml.dump({"docker_user": docker_creds["docker_user"]}, f)
        click.echo("Credentials successfully authenticated and saved!")
        f.close()
    return docker_client, docker_creds
