import os
import sys

from setuptools import find_packages, setup

# sourced from
# https://github.com/django/django/blob/master/setup.py#L7

MODULE_NAME = 'gaia_source'
CURRENT_PYTHON = sys.version_info[:2]
REQUIRED_PYTHON = (3, 9)
ENCODING = 'utf-8'

if CURRENT_PYTHON < REQUIRED_PYTHON:
    raise NotImplementedError(f'Required Python Version: {REQUIRED_PYTHON}')


EXCLUDE_FROM_PACKAGES = []
version = '0.0.1'

INSTALL_REQUIRES = ['uvloop', 'asyncpg', 'httpx', 'bs4', 'aiofiles', 'aiocsv']
description = 'A utility to manage gaia_source/csv'

def read(fname):
  with open(os.path.join(os.path.dirname(__file__), fname)) as f:
    return f.read()

setup(
    name=MODULE_NAME,
    version=version,
    python_requires='>={}.{}'.format(*REQUIRED_PYTHON),
    url='https://github.com/jbcurtin/gaia_source',
    author="Joseph Curtin <josephbcurtin@gmail.com>",
    author_email='josephbcurtin@gmail.com',
    description=description,
    long_description=read('README.md'),
    long_description_content_type='text/markdown',
    license=read('LICENSE'),
    packages=find_packages(exclude=EXCLUDE_FROM_PACKAGES),
    include_package_data=True,
    scripts=[],
    install_requires=INSTALL_REQUIRES,
    entry_points={
        'console_scripts': [
            'gaia-source = gaia_source.factory:run_from_cli',
        ],
    },
    zip_safe=False,
    classifiers=[
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3 :: Only',
    'Programming Language :: Python :: 3.9',
  ],
  project_urls={}
)
