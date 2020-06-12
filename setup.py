# -*- coding: utf-8 -*-
# SPDX-License-Identifier: GPL-2.0

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="seq2pat",
    description="Seq2Pat: Sequence-to-Pattern Generation Library",
    long_description=long_description,
    version="1.1.0",
    url="https://github.com/fidelity/seq2pat",
    packages=setuptools.find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
    project_urls={
        "Documentation": "https://fidelity.github.io/seq2pat/",
        "Source": "https://github.com/fidelity/seq2pat"
    },
    include_package_data=True
)