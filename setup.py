# coding=utf-8
# author xin.he
#
# build:
#     rm -rf ./build ./dist ./dynamic_pip.egg-info/ && python setup.py sdist bdist_wheel
#
# upload:
#     twine check ./dist/*
#     twine upload dist/*
#
# install local:
#     pip install --upgrade dynamic_pip-XXXX-pyXX-none-any.whl
#
# install from PyPi:
#     pip install dynamic_pip
#
from dynamicPip import __version__
from setuptools import setup, find_packages

import sys


def long_description_load(filename):
    """
    long description loader
    """
    try:
        with open(filename, mode='r', encoding='utf-8') as f:
            _long_description = f.read()
    except FileNotFoundError:
        _long_description = ''

    RAW_LOGO = 'assets/logo.jpg'
    PYPI_LOGO = 'https://raw.githubusercontent.com/uguisu/dynamic-pip/main/assets/logo.jpg'
    RAW_MERMAID = '```mermaid'
    PYPI_MERMAID = '![mermaid](https://raw.githubusercontent.com/uguisu/dynamic-pip/main/assets/dependence_tree.jpg)'

    # remove logo
    _long_description = _long_description.replace(RAW_LOGO, PYPI_LOGO)
    _long_description = _long_description.replace(':point_left:', '')
    _long_description = _long_description.replace(':construction:', '')

    rtn = []
    is_mermaid_area = False
    for ln in _long_description.splitlines(keepends=False):

        if is_mermaid_area:
            if ln == '```':
                # rollback flag
                is_mermaid_area = False
                # use an image instead
                rtn.append(PYPI_MERMAID)
            continue

        if (not is_mermaid_area) and (RAW_MERMAID == ln):
            # find mermaid area
            is_mermaid_area = True
            continue

        rtn.append(ln)

    return '\n'.join(rtn)


def parse_requirements(filename):
    """
    load requirements from a pip requirements file. (replacing from pip.req import parse_requirements)
    """
    lines = (line.strip() for line in open(filename))
    return [line for line in lines if line and not line.startswith("#")]


# verify python version
if sys.version_info < (3, 6, 0):
    raise OSError(f'dynamic-pip requires Python >=3.6, but yours is {sys.version}')


pkg_name = 'dynamic-pip'
long_description = long_description_load('README.md')
reqs = parse_requirements('requirements.txt')

setup(
    name=pkg_name,
    version=__version__,
    author='xin.he',
    author_email='unknow@dynamic-pip.com',
    url='https://github.com/uguisu/dynamic-pip',
    download_url='https://github.com/uguisu/dynamic-pip/tags',
    python_requires='>=3.7',
    license='Apache 2.0',
    description='Help users to dynamically manage python package resources',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=find_packages(),
    zip_safe=False,
    setup_requires=['setuptools>=60.2.0', 'wheel'],
    install_requires=reqs,
    include_package_data=True,

    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Unix Shell',
        'Operating System :: OS Independent',
        'Topic :: Software Development',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],

    entry_points={
        'console_scripts': [
            'dypip = dynamicPip.__main__:main'
        ]
    },

    project_urls={
        'Documentation': 'https://github.com/uguisu/dynamic-pip',
        'Source': 'https://github.com/uguisu/dynamic-pip',
        'Tracker': 'https://github.com/uguisu/dynamic-pip/issues',
    },

    keywords='dynamic pip packages',
)