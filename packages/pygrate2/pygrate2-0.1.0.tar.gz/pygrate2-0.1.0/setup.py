#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import find_packages, setup

import pygrate2 

setup(
    name="pygrate2",
    version=pygrate2.__version__,
    packages=find_packages(),
    author="Laurent Evrard",
    description="Migration tools for python",
    long_description=open("README.md").read(),
    install_requires=[],
    url="https://git.fenrys.io/fenrys/back/python_ddd",
    scripts=["bin/pygrate"],
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
