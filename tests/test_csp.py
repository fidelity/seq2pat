# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0

import unittest
import numpy as np
from sequential.seq2pat import Attribute
from sequential.csp_global import is_satisfiable


class TestSeq2Pat(unittest.TestCase):

    def test_csp_example(self):

        sequence = [1, 2, 3, 4]
        pattern = [1, 2, 3]

        values = [1, 2, 3, 4]

        attrs1 = Attribute(values=[list(np.array(values) * 1)])
        attrs_avg_ct = 0 <= attrs1.average() <= 2

        attrs2 = Attribute(values=[list(np.array(values) * 10)])
        attrs_gap_ct = 0 <= attrs2.gap() <= 100

        attrs3 = Attribute(values=[list(np.array(values) * 100)])
        attrs_median_ct = 0 <= attrs3.median() <= 1000

        attrs4 = Attribute(values=[list(np.array(values) * 1000)])
        attrs_span_ct = 0 <= attrs4.span() <= 100000

        has_pattern = is_satisfiable(sequence, pattern, 0, [attrs_avg_ct, attrs_gap_ct, attrs_median_ct,
                                                            attrs_span_ct])

        self.assertEqual(has_pattern, True)


if __name__ == '__main__':
    unittest.main()




