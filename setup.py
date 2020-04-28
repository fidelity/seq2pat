# -*- coding: utf-8 -*-
# SPDX-License-Identifer: GPL-2.0

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="seq2pat",
    description="Seq2Pat: Sequence-to-Pattern Generation Library",
    long_description=long_description,
    version="1.0.0",
    url="https://github.com/fmr-llc/seq2pat",
    packages=setuptools.find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
    project_urls={
        "Documentation": "https://fmr-llc.github.io/seq2pat/",
        "Source": "https://github.com/fmr-llc/seq2pat"
    }
)