#!/usr/bin/env python

from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="download_giab",
    version="0.6.0",

    python_requires="~=3.6",
    install_requires=[
        "requests>=2.20,<3",
    ],

    description="Utility Python package to download Genome-in-a-Bottle data from their index files.",
    long_description=long_description,
    long_description_content_type="text/markdown",

    url="https://github.com/davidlougheed/download_giab",
    license="GPLv3",
    classifiers=[
        "Programming Language :: Python :: 3 :: Only",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],

    author="David Lougheed",
    author_email="david.lougheed@gmail.com",

    packages=find_packages(exclude="tests"),

    entry_points={
        "console_scripts": ["download_giab=download_giab.entry:main"],
    },
)
