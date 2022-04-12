# -*- coding: utf-8 -*-
# SPDX-License-Identifier: GPL-2.0

import unittest

from sequential.seq2pat import Seq2Pat, Attribute
from sequential.csp import is_satisfiable


class TestSeq2Pat(unittest.TestCase):

    def test_csp_example(self):

        sequence = [2, 1, 3, 4]
        pattern = [2, 1, 3]

        has_pattern = is_satisfiable(sequence, pattern)

        print("has_pattern: ", has_pattern)
