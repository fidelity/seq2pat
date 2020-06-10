# -*- coding: utf-8 -*-
# SPDX-License-Identifer: GPL-2.0

# from distutils.core import setup
# from Cython.Build import cythonize

# # python setup.py build_ext --inplace
# ext_options = {"compiler_directives": {"profile": True}, "annotate": True}
# setup(
#     ext_modules=cythonize("seq_to_pat.pyx", language_level="3", **ext_options)
# )

import platform
from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext
from Cython.Build import cythonize

compile_extra_args = []
link_extra_args = []

# Set compiler arguments for different platforms
if platform.system() == "Windows":
    # compile_extra_args = ["/std:c++latest", "/EHsc"]
    compile_extra_args = []
    link_extra_args = []
elif platform.system() == "Linux" or platform.system() == "Darwin":
    compile_extra_args = ['-std=c++0x']
    link_extra_args = ["-stdlib=libc++"]

compile_files = [
    "seq_to_pat.pyx",
]

ext_modules = [Extension("seq_to_pat", compile_files,
                         language="c++",
                         extra_compile_args=compile_extra_args,
                         extra_link_args=link_extra_args)]

ext_options = {"compiler_directives": {"profile": True}, "annotate": True}

setup(ext_modules=cythonize(ext_modules, language_level="3", **ext_options))

# Run python setup.py build_ext --inplace to build backend