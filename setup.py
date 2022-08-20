# coding=utf-8
import os
import shutil
from intelliw import __version__
from setuptools import setup, find_packages


def move_base_file(infile, outfile):
    """move intelliw/scaffolding/resources/iw.py to workdir """
    shutil.copy(infile, outfile)


def parse_requirements(filename):
    """ load requirements from a pip requirements file. (replacing from pip.req import parse_requirements)"""
    lines = (line.strip() for line in open(filename))
    return [line for line in lines if line and not line.startswith("#")]


def long_description_load(filename):
    with open(filename, "r") as fh:
        long_description = fh.read()
    return long_description


def purge_pycache(path):
    for file_name in os.listdir(path):
        abs_path = os.path.join(path, file_name)
        if file_name == "__pycache__":
            shutil.rmtree(abs_path)
        elif os.path.isdir(abs_path):
            purge_pycache(abs_path)


reqs = parse_requirements('intelliw/requirements.txt')
long_description = long_description_load('README.md')
purge_pycache('intelliw')

setup(
    name='intelliw',
    version=__version__,
    author='yonyou',
    author_email='yonyou@yonyou.com',
    url="http://git.yonyou.com/iuapaipaas/iw-algo-fx",
    python_requires='>=3.6',


    description='An easy to start Intelligent Workshop Algorithm Framework',
    long_description=long_description,
    long_description_content_type="text/markdown",


    classifiers=[
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Operating System :: OS Independent',
    ],


    packages=find_packages(),
    install_requires=reqs,
    include_package_data=True,

    entry_points={
        'console_scripts': [
            'intelliw = intelliw.interface.entrypoint:run'
        ]
    },

)

