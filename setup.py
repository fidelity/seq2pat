# -*- coding: utf-8 -*-
# SPDX-License-Identifier: GPL-2.0

import setuptools
import platform
import os
from setuptools.extension import Extension
from Cython.Build import cythonize


with open("README.md", "r") as fh:
    long_description = fh.read()

with open("requirements.txt") as fh:
    required = fh.read().splitlines()

with open(os.path.join('sequential', '_version.py')) as fp:
    exec(fp.read())

compile_extra_args = []
link_extra_args = []

# Set compiler arguments for different platforms
if platform.system() == "Windows":
    # compile_extra_args = ["/std:c++latest", "/EHsc"]
    compile_extra_args = []
    link_extra_args = []
elif platform.system() == "Linux" or platform.system() == "Darwin":
    compile_extra_args = ["-std=c++0x"]
    # link_extra_args = ["-stdlib=libc++"]
    link_extra_args = []

# Set compile files for cython
compile_files = [
    "sequential/backend/seq_to_pat.pyx",
]

# Set compiler options
ext_options = {"compiler_directives": {"profile": True}, "annotate": True}

# Build extension modules
ext_modules = cythonize([Extension("sequential.backend.seq_to_pat", compile_files,
                                   language="c++",
                                   extra_compile_args=compile_extra_args,
                                   extra_link_args=link_extra_args)
                         ], language_level="3", **ext_options)

setuptools.setup(
    name="seq2pat",
    description="Seq2Pat: Sequence-to-Pattern Generation Library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    version=__version__,
    author="FMR LLC",
    url="https://github.com/fidelity/seq2pat",
    install_requires=required,
    setup_requires=required,
    packages=setuptools.find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
    classifiers=[
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
        "Programming Language :: Python :: 3.6",
        "Operating System :: OS Independent",
    ],
    project_urls={
        "Documentation": "https://fidelity.github.io/seq2pat/",
        "Source": "https://github.com/fidelity/seq2pat"
    },
    include_package_data=True,
    ext_modules=ext_modules
)
