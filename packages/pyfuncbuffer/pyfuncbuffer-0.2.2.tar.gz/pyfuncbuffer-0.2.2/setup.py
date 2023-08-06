#!/usr/bin/env python

from distutils.core import setup
from setuptools import find_packages


setup(
    name='pyfuncbuffer',
    version='0.2.2',
    packages=find_packages(exclude=["tests", "*.tests", "*.tests.*", "tests.*"]),
    license='GPLv3',
    description="A library for buffering function calls",
    author="Jupsista",
    url="https://github.com/Jupsista/pyfuncbuffer",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        "Typing :: Typed",
        "Topic :: Software Development :: Libraries",
        "Programming Language :: Python :: 3",
    ],
)
