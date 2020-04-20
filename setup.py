# -*- coding: utf-8 -*-
# SPDX-License-Identifer: GPL-2.0

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="seq2pat",
    description="Seq2Pat: Sequence-to-Pattern",
    long_description=long_description,
    version="1.0.0",
    url="https://",
    packages=setuptools.find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
    project_urls={
        "Source": "https://"
    }
)