#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import find_packages, setup

import python_ddd

setup(
    name="dddes",
    version=python_ddd.__version__,
    packages=find_packages(),
    author="Laurent Evrard",
    description="DDD tools for python",
    long_description=open("README.md").read(),
    install_requires=["pymongo"],
    url="https://github.com/owlint/dddes",
    classifiers=[
        "Programming Language :: Python",
        "Development Status :: 1 - Planning",
        "License :: OSI Approved",
        "Natural Language :: French",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.10",
        "Topic :: Communications",
    ],
    license="Apache-2.0 License",
)
