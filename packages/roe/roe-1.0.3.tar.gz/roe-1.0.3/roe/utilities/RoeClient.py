import click
import pandas as pd
import requests

from roe.utilities import init_utils
from roe.utilities.errors import *


class RoeClient:
    def __init__(self, base_url=None):
        if not base_url:
            self.base_url = init_utils.get_roe_url()
        else:
            self.base_url = base_url

    def __str__(self):
        return self.base_url

    def get_base_url(self):
        return self.base_url

    def set_base_url(self, base_url):
        self.base_url = base_url

    def verify(self, package_name):
        url = f"{self.base_url}/verify/?package_name={package_name}"
        response = requests.get(url)
        if response.status_code != 200:
            raise APIError("Verify")
        return response.text

    def delete_all(self):
        response_containers_prune = requests.get(self.base_url + "/containers/remove/all")
        response_packages_prune = requests.get(self.base_url + '/packages/prune/')

        if response_packages_prune.status_code == 200 and response_containers_prune.status_code == 200:
            click.echo("Removed the following packages:")
            # Remove quote marks and show all packages removed
            click.echo(response_containers_prune.text[1:-1])

        else:
            raise APIError('Delete All')

    def delete_package(self, package_name):
        response = requests.get(f"{self.base_url}/packages/delete/?package_name={package_name}")

        if response.status_code != 200:
            raise APIError("Package Delete")

    def delete_container(self, package_name):
        response = requests.get(f"{self.base_url}/containers/remove/?package_name={package_name}")

        if response.status_code != 200:
            raise APIError("Container Delete")

    def delete_both(self, package_name):
        self.delete_container(package_name)
        self.delete_package(package_name)

    def undeploy(self, package_name):
        url = f"{self.base_url}/deploy/?package_name={package_name}"
        response = requests.get(url)

        if response.status_code != 200:
            raise APIError("Undeploy")

    def get_containers(self):
        response = requests.get(self.base_url + '/containers/?include_stopped=true')

        if response.status_code != 200:
            raise APIError("Container List")

        dfAllContainers = pd.read_json(response.text, orient='records')
        return dfAllContainers

    def get_packages(self):
        response = requests.get(self.base_url + '/packages/')

        if response.status_code != 200:
            raise APIError("Package List")

        dfPackages = pd.read_json(response.text, orient='records')
        return dfPackages

    def upload(self, package_name, file_path):
        url = f'{self.base_url}/upload/?package_name={package_name}'
        files = {'package': open(file_path, 'rb')}
        response = requests.post(url, files=files)

        files["package"].close()

        if response.status_code != 200:
            raise APIError('Upload')

    def logs(self, package_name, tail=None):
        url = f"{self.base_url}/containers/logs/?package_name={package_name}"
        if tail:
            url += f"&tail={tail}"

        response = requests.get(url)

        if response.status_code != 200:
            raise LoggingError()

        return response.text

    def stop(self, package_name):
        url = f"{self.base_url}/containers/stop/?package_name={package_name}"
        response = requests.get(url)

        if response.status_code != 200:
            raise PackageStopError(package_name)

    def start(self, package_name):
        url = f"{self.base_url}/containers/restart/?package_name={package_name}"
        response = requests.get(url)

        if response.status_code != 200:
            raise PackageStartError(package_name)

    def deploy(self, package_name, port):
        url = f"{self.base_url}/deploy/?package_name={package_name}&port={port}"
        response = requests.get(url)

        if response.status_code == 409:
            raise PackageNameConflictError()
        elif response.status_code != 200:
            raise APIError('Deploy')
