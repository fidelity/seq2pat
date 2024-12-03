# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0

import os
import unittest

from sequential.seq2pat import Seq2Pat, Attribute
from sequential.pat2feat import Pat2Feat


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
        pat2feat = Pat2Feat()
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

        # Create encoding with csp_global when max_span=None
        pat2feat = Pat2Feat()
        encodings = pat2feat.get_features(sequences, patterns, constraints=[price_ct], max_span=None)
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
        pat2feat = Pat2Feat()
        encodings = pat2feat.get_features(sequences, patterns)
        # encoding is a data frame
        # sequence      feat0 feat1 feat2
        # [A,A,B,A,D]    1    1     0
        # [C, B, A]      0    1     1
        # [C, A, C, D]   1    0     1

        self.assertListEqual([[1, 1, 0], [0, 1, 1], [1, 0, 1]], encodings.values[:, 1:].tolist())

    def test_one_hot_encoding_csp_global_without_constraints(self):
        sequences = [["A", "A", "B", "A", "D"],
                     ["C", "B", "A"],
                     ["C", "A", "C", "D"]]

        # Seq2Pat over 3 sequences
        seq2pat = Seq2Pat(sequences)

        # Find sequences with min_frequency=2
        patterns = seq2pat.get_patterns(min_frequency=2)

        # Create encoding
        pat2feat = Pat2Feat()
        encodings = pat2feat.get_features(sequences, patterns, max_span=None,
                                          drop_pattern_frequency=True)
        # encoding is a data frame
        # sequence      feat0 feat1 feat2
        # [A,A,B,A,D]    1    1     0
        # [C, B, A]      0    1     1
        # [C, A, C, D]   1    0     1

        self.assertListEqual([[1, 1, 0], [0, 1, 1], [1, 0, 1]], encodings.values[:, 1:].tolist())

    def test_one_hot_encoding_csp_local_random_patterns_without_constraints(self):
        # Define the sequences and their attributes to create one-hot encoding
        sequences = [["A", "A", "B", "A", "D"],
                     ["C", "B", "A"],
                     ["C", "A", "C", "D"]]

        patterns = [['B', 'D'], ['A', 'C', 'D']]

        # Create encoding, do not need to drop frequency in the end of each pattern
        pat2feat = Pat2Feat()
        encodings = pat2feat.get_features(sequences, patterns, drop_pattern_frequency=False)

        self.assertListEqual([[1, 0], [0, 0], [0, 1]], encodings.values[:, 1:].tolist())

    def test_one_hot_encoding_csp_global_random_patterns_without_constraints(self):
        # Define the sequences and their attributes to create one-hot encoding
        sequences = [["A", "A", "B", "A", "D"],
                     ["C", "B", "A"],
                     ["C", "A", "C", "D"]]

        patterns = [['B', 'D'], ['A', 'C', 'D']]

        # Create encoding, do not need to drop frequency in the end of each pattern
        pat2feat = Pat2Feat()
        encodings = pat2feat.get_features(sequences, patterns, max_span=None,
                                          drop_pattern_frequency=False)

        self.assertListEqual([[1, 0], [0, 0], [0, 1]], encodings.values[:, 1:].tolist())

    def test_one_hot_encoding_csp_local_random_patterns_with_constraints(self):
        # Define the sequences and their attributes to create one-hot encoding
        sequences = [["A", "A", "B", "A", "D"],
                     ["C", "B", "A"],
                     ["C", "A", "C", "D"]]

        attributes = [[5, 5, 3, 8, 2],
                      [1, 3, 3],
                      [4, 5, 2, 1]]

        # Create price attributes
        price = Attribute(values=attributes)

        price_ct = price.median() <= 2

        patterns = [['B', 'D'], ['A', 'C', 'D']]

        # Create encoding
        pat2feat = Pat2Feat()
        encodings = pat2feat.get_features(sequences, patterns, constraints=[price_ct], drop_pattern_frequency=False)

        self.assertListEqual([[0, 0], [0, 0], [0, 1]], encodings.values[:, 1:].tolist())

    def test_one_hot_encoding_csp_global_random_patterns_with_constraints(self):
        # Define the sequences and their attributes to create one-hot encoding
        sequences = [["A", "A", "B", "A", "D"],
                     ["C", "B", "A"],
                     ["C", "A", "C", "D"]]

        attributes = [[5, 5, 3, 8, 2],
                      [1, 3, 3],
                      [4, 5, 2, 1]]

        # Create price attributes
        price = Attribute(values=attributes)

        price_ct = price.median() <= 2

        patterns = [['B', 'D'], ['A', 'C', 'D']]

        # Create encoding
        pat2feat = Pat2Feat()
        encodings = pat2feat.get_features(sequences, patterns, constraints=[price_ct],
                                          max_span=None, drop_pattern_frequency=False)

        self.assertListEqual([[0, 0], [0, 0], [0, 1]], encodings.values[:, 1:].tolist())

    def test_one_hot_encoding_string_patterns_without_dropping_frequency(self):
        # Define the sequences and their attributes to create one-hot encoding
        sequences = [["A", "A", "B", "A", "D"],
                     ["C", "B", "A"],
                     ["C", "A", "C", "D"]]

        attributes = [[5, 5, 3, 8, 2],
                      [1, 3, 3],
                      [4, 5, 2, 1]]

        # Create price attributes
        price = Attribute(values=attributes)

        price_ct = price.median() <= 2

        patterns = [['B', 'D', 1], ['A', 'C', 'D', 1]]

        # Create encoding
        with self.assertRaises(ValueError):
            # This should fail when patterns have frequency appended to the end of patterns
            pat2feat = Pat2Feat()
            encodings = pat2feat.get_features(sequences, patterns, constraints=[price_ct], drop_pattern_frequency=False)
            print(encodings)

    def test_constraints_as_positional_arg(self):
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
        # Create price attributes
        price_ct = 3 <= price.median() <= 4
        # Constraint to specify the median of prices in a pattern
        seq2pat.add_constraint(price_ct)
        # Find sequences with min_frequency=2
        patterns = seq2pat.get_patterns(min_frequency=2)

        # Create encoding with/without constraints
        pat2feat = Pat2Feat()
        encodings = pat2feat.get_features(sequences, patterns, [price_ct], drop_pattern_frequency=True)

        self.assertListEqual([[1], [0], [1]], encodings.values[:, 1:].tolist())


if __name__ == "__main__":
    unittest.main()
