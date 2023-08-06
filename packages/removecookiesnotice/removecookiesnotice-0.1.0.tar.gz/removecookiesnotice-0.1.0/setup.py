#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import find_packages, setup

import removecookiesnotice

setup(
    name="removecookiesnotice",
    version=removecookiesnotice.__version__,
    packages=find_packages(),
    author="Laurent Evrard",
    author_email="laurent@owlint.fr",
    description="Tool to remove cookies notice in html pages",
    long_description=open("README.md").read(),
    install_requires=[],
    url="https://github.com/owlint/CookiesNoticeRemover",
    classifiers=[
        "Programming Language :: Python",
        "Development Status :: 1 - Planning",
        "License :: OSI Approved",
        "Natural Language :: French",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.10",
        "Topic :: Communications",
    ],
    license="Apache License 2.0",
)
