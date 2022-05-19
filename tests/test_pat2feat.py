# -*- coding: utf-8 -*-
# SPDX-License-Identifier: GPL-2.0

import os
import unittest

from sequential.seq2pat import Seq2Pat, Attribute
from sequential.pat2feat import Pat2Feat, OneHotEncoding


class TestDPMUtils(unittest.TestCase):
    TEST_DIR = os.path.dirname(os.path.abspath(__file__))
    DATA_DIR = TEST_DIR + os.sep + "data" + os.sep

    def test_pat2feat_usage(self):

        sequences = [["A", "A", "B", "A", "D"],
                     ["C", "B", "A"],
                     ["C", "A", "C", "D"]]

        values = [[5, 5, 3, 8, 2],
                  [1, 3, 3],
                  [4, 5, 2, 1]]

        # Seq2Pat over 3 sequences
        seq2pat = Seq2Pat(sequences)

        # Create price attributes
        price = Attribute(values)

        # Create price constraint
        price_ct = 3 <= price.median() <= 4

        # Constraint to specify the median of prices in a pattern
        seq2pat.add_constraint(price_ct)

        # Find sequences with min_frequency=2
        patterns = seq2pat.get_patterns(min_frequency=2)

        # Create encoding
        pat2feat = Pat2Feat(featurization=OneHotEncoding())
        encodings = pat2feat.get_features(sequences, patterns, constraints=[price_ct])
        # sequence      feat0
        # [A,A,B,A,D]    1
        # [C, B, A]      0
        # [C, A, C, D]   1

        self.assertListEqual([[1], [0], [1]], encodings.values[:, 1:].tolist())

    def test_one_hot_encoding_csp_global_with_constraints(self):

        sequences = [["A", "A", "B", "A", "D"],
                     ["C", "B", "A"],
                     ["C", "A", "C", "D"]]

        values = [[5, 5, 3, 8, 2],
                  [1, 3, 3],
                  [4, 5, 2, 1]]

        # Seq2Pat over 3 sequences
        seq2pat = Seq2Pat(sequences)

        # Create price attributes
        price = Attribute(values)

        # Create price constraint
        price_ct = 3 <= price.median() <= 4

        # Constraint to specify the median of prices in a pattern
        seq2pat.add_constraint(price_ct)

        # Find sequences with min_frequency=2
        patterns = seq2pat.get_patterns(min_frequency=2)

        # Create encoding with csp_global when rolling_window_size=None
        pat2feat = Pat2Feat(featurization=OneHotEncoding(rolling_window_size=None))
        encodings = pat2feat.get_features(sequences, patterns, constraints=[price_ct])
        # sequence      feat0
        # [A,A,B,A,D]    1
        # [C, B, A]      0
        # [C, A, C, D]   1

        self.assertListEqual([[1], [0], [1]], encodings.values[:, 1:].tolist())

    def test_one_hot_encoding_csp_local_without_constraints(self):
        sequences = [["A", "A", "B", "A", "D"],
                     ["C", "B", "A"],
                     ["C", "A", "C", "D"]]

        # Seq2Pat over 3 sequences
        seq2pat = Seq2Pat(sequences)

        # Find sequences with min_frequency=2
        patterns = seq2pat.get_patterns(min_frequency=2)

        # Create encoding
        pat2feat = Pat2Feat(featurization=OneHotEncoding())
        encodings = pat2feat.get_features(sequences, patterns)
        # encoding is a data frame
        # sequence      feat0 feat1 feat2
        # [A,A,B,A,D]    1    1     0
        # [C, B, A]      0    1     1
        # [C, A, C, D]   1    0     1

        self.assertListEqual([[1, 1, 0], [0, 1, 1], [1, 0, 1]], encodings.values[:, 1:].tolist())


if __name__ == "__main__":
    unittest.main()
