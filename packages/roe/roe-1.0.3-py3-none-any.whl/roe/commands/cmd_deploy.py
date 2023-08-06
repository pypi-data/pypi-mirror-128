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

import click

from roe.utilities.running_utils import deploy


@click.command()
@click.option("-l", "--local", is_flag=True, type=bool, help="Deploy local package")
@click.option("-n", "--package_name", type=str, help="Name of package")
@click.option("-p", "--port", type=str, help="Specify a port")
@click.option("-q", "--quick", is_flag=True, type=bool, help="Skip opening the web page after deployment")
@click.argument('folder_path')
def cli(local, package_name, folder_path, port, quick):
    """Deploy and start a package."""
    deploy(local, package_name, folder_path, port, quick_deploy=quick)
    return
