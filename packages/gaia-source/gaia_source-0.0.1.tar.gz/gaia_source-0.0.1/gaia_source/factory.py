#!/usr/bin/env python

import argparse
import asyncio
import enum
import logging
import os
import sys
import uvloop

# Add current working path to include module libraries
sys.path.append(os.getcwd())

from gaia_source.constants import PROJECT_PATH, DEFAULT_DATA_PATH
from gaia_source.datatypes import DownloadOptions, InstallOptions
from gaia_source.utils import download_data, load_data

logger = logging.getLogger('')
sysHandler = logging.StreamHandler()
sysHandler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
logger.addHandler(sysHandler)
logger.setLevel(logging.INFO)
logger = logging.getLogger('Gaia Source Factory: 0.0.1')


def obtain_options() -> argparse.Namespace:
    parser = argparse.ArgumentParser('Gaia Source ETL Manager')
    parser.add_argument('-p', '--project-path', default=PROJECT_PATH, help="Which directory to create project files?")
    parser.add_argument('-l', '--data-path', default=DEFAULT_DATA_PATH, help="Where to store data?")
    parser.add_argument('-d', '--download-data', type=DownloadOptions, default=DownloadOptions.Zero, help="Dataset Download Options")
    parser.add_argument('-i', '--install-data', type=InstallOptions, default=InstallOptions.Nothing, help="Dataset Install Options")
    return parser.parse_args()


async def main(options: argparse.Namespace) -> None:
    logger.info(f'Project Directory: {options.project_path}')
    logger.info(f'Data Direttory: {options.data_path}')
    if not options.download_data is DownloadOptions.Zero:
        await download_data(options.data_path, options.download_data)

    if not options.install_data is InstallOptions.Nothing:
        await load_data(options.data_path, options.install_data)


def run_from_cli():
    uvloop.install()
    event_loop = asyncio.get_event_loop()
    options = obtain_options()
    event_loop.run_until_complete(main(options))

if __name__ == '__main__':
    run_from_cli()
    sys.exit(0)

