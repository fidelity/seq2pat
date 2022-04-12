import unittest

import os
import unittest
import pandas as pd

from sequential.seq2pat import Seq2Pat, Attribute
from sequential.utils import (get_one_hot_encodings, dichotomic_pattern_mining)


class TestDPMUtils(unittest.TestCase):
    TEST_DIR = os.path.dirname(os.path.abspath(__file__))
    DATA_DIR = TEST_DIR + os.sep + "data" + os.sep

    def test_one_hot_encoding_with_constraints(self):

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
        encodings = get_one_hot_encodings(sequences, patterns, constraints=[price_ct])
        # sequence      feat0
        # [A,A,B,A,D]    1
        # [C, B, A]      0
        # [C, A, C, D]   1

        self.assertListEqual([[1], [0], [1]], encodings.values[:, 1:].tolist())

    def test_one_hot_encoding_without_constraints(self):
        sequences = [["A", "A", "B", "A", "D"],
                     ["C", "B", "A"],
                     ["C", "A", "C", "D"]]

        # Seq2Pat over 3 sequences
        seq2pat = Seq2Pat(sequences)

        # Find sequences with min_frequency=2
        patterns = seq2pat.get_patterns(min_frequency=2)

        # Create encoding
        encodings = get_one_hot_encodings(sequences, patterns)
        # encoding is a data frame
        # sequence      feat0 feat1 feat2
        # [A,A,B,A,D]    1    1     0
        # [C, B, A]      0    1     1
        # [C, A, C, D]   1    0     1

        self.assertListEqual([[1, 1, 0], [0, 1, 1], [1, 0, 1]], encodings.values[:, 1:].tolist())

    def test_one_hot_encoding_random_patterns_without_constraints(self):
        # Define the sequences and their attributes to create one-hot encoding
        sequences = [["A", "A", "B", "A", "D"],
                     ["C", "B", "A"],
                     ["C", "A", "C", "D"]]

        seq2pat = Seq2Pat(sequences)

        patterns = [['B', 'D'], ['A', 'C', 'D']]

        # Create encoding, do not need to drop frequency in the end of each pattern
        encodings = get_one_hot_encodings(sequences, patterns, drop_pattern_frequency=False)

        self.assertListEqual([[1, 0], [0, 0], [0, 1]], encodings.values[:, 1:].tolist())

    def test_one_hot_encoding_random_patterns_with_constraints(self):
        # Define the sequences and their attributes to create one-hot encoding
        sequences = [["A", "A", "B", "A", "D"],
                     ["C", "B", "A"],
                     ["C", "A", "C", "D"]]

        attributes = [[5, 5, 3, 8, 2],
                      [1, 3, 3],
                      [4, 5, 2, 1]]

        seq2pat = Seq2Pat(sequences)

        # Create price attributes
        price = Attribute(values=attributes)

        price_ct = price.median() <= 2

        patterns = [['B', 'D'], ['A', 'C', 'D']]

        # Create encoding
        encodings = get_one_hot_encodings(sequences, patterns, constraints=[price_ct], drop_pattern_frequency=False)

        self.assertListEqual([[0, 0], [0, 0], [0, 1]], encodings.values[:, 1:].tolist())

    def test_one_hot_encoding_string_patterns_without_dropping_frequency(self):
        # Define the sequences and their attributes to create one-hot encoding
        sequences = [["A", "A", "B", "A", "D"],
                     ["C", "B", "A"],
                     ["C", "A", "C", "D"]]

        attributes = [[5, 5, 3, 8, 2],
                      [1, 3, 3],
                      [4, 5, 2, 1]]

        seq2pat = Seq2Pat(sequences=sequences)

        # Create price attributes
        price = Attribute(values=attributes)

        price_ct = price.median() <= 2

        patterns = [['B', 'D', 1], ['A', 'C', 'D', 1]]

        # Create encoding
        with self.assertRaises(ValueError):
            # This should fail when patterns have frequency appended to the end of patterns
            encodings = get_one_hot_encodings(sequences, patterns, constraints=[price_ct], drop_pattern_frequency=False)

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
        encodings = get_one_hot_encodings(sequences, patterns, [price_ct])

        self.assertListEqual([[1], [0], [1]], encodings.values[:, 1:].tolist())

    def test_dichotomic_pattern_mining_union(self):
        sequences_pos = [["A", "A", "B", "A", "D"],
                         ["C", "B", "A"],
                         ["C", "A", "C", "D"]]

        # update attributes in the 2nd and 3rd row to add ['C', 'A']
        values_pos = [[5, 5, 3, 8, 2],
                      [3, 3, 3],
                      [3, 5, 2, 1]]

        sequences_neg = [["A", "A", "B", "A", "D"],
                         ["C", "B", "A"],
                         ["C", "A", "C", "D"]]

        # Updating attributes in the first row to add ['B', 'A']
        values_neg = [[5, 5, 3, 3, 2],
                      [1, 3, 3],
                      [4, 5, 2, 1]]

        # Sequence data frame
        sequences_df = pd.DataFrame({'sequence': sequences_pos + sequences_neg, 'price': values_pos + values_neg,
                                     'label': [1]*3 + [0]*3})

        # Define constraints on attribute columns in data frame
        price = Attribute(sequences_df['price'].values.tolist())
        price_ct = 3 <= price.median() <= 4
        attr_col_to_constraints = {'price': [price_ct]}

        # patterns_pos: [['A', 'D'], ['C', 'A']]
        # patterns_neg: [['A', 'D'], ['B', 'A']]
        dpm_patterns = dichotomic_pattern_mining(sequences_df, sequence_col_name='sequence', label_col_name='label',
                                                 attr_col_to_constraints=attr_col_to_constraints, min_frequency=2,
                                                 pattern_aggregation='union')

        self.assertListEqual([['A', 'D'], ['B', 'A'], ['C', 'A']], dpm_patterns)

    def test_dichotomic_pattern_mining_intersection(self):
        sequences_pos = [["A", "A", "B", "A", "D"],
                         ["C", "B", "A"],
                         ["C", "A", "C", "D"]]

        # update attributes in the 2nd and 3rd row to add ['C', 'A']
        values_pos = [[5, 5, 3, 8, 2],
                      [3, 3, 3],
                      [3, 5, 2, 1]]

        sequences_neg = [["A", "A", "B", "A", "D"],
                         ["C", "B", "A"],
                         ["C", "A", "C", "D"]]

        # Updating attributes in the first row to add ['B', 'A']
        values_neg = [[5, 5, 3, 3, 2],
                      [1, 3, 3],
                      [4, 5, 2, 1]]

        # Sequence data frame
        sequences_df = pd.DataFrame({'sequence': sequences_pos + sequences_neg, 'price': values_pos + values_neg,
                                     'label': [1] * 3 + [0] * 3})

        # Define constraints on attribute columns in data frame
        price = Attribute(sequences_df['price'].values.tolist())
        price_ct = 3 <= price.median() <= 4
        attr_col_to_constraints = {'price': [price_ct]}

        # patterns_pos: [['A', 'D'], ['C', 'A']]
        # patterns_neg: [['A', 'D'], ['B', 'A']]
        dpm_patterns = dichotomic_pattern_mining(sequences_df, sequence_col_name='sequence', label_col_name='label',
                                                 attr_col_to_constraints=attr_col_to_constraints, min_frequency=2,
                                                 pattern_aggregation='intersection')

        self.assertListEqual([['A', 'D']], dpm_patterns)

    def test_dichotomic_pattern_mining_unique_pos(self):
        sequences_pos = [["A", "A", "B", "A", "D"],
                         ["C", "B", "A"],
                         ["C", "A", "C", "D"]]

        # update attributes in the 2nd and 3rd row to add ['C', 'A']
        values_pos = [[5, 5, 3, 8, 2],
                      [3, 3, 3],
                      [3, 5, 2, 1]]

        sequences_neg = [["A", "A", "B", "A", "D"],
                         ["C", "B", "A"],
                         ["C", "A", "C", "D"]]

        # Updating attributes in the first row to add ['B', 'A']
        values_neg = [[5, 5, 3, 3, 2],
                      [1, 3, 3],
                      [4, 5, 2, 1]]

        # Sequence data frame
        sequences_df = pd.DataFrame({'sequence': sequences_pos + sequences_neg, 'price': values_pos + values_neg,
                                     'label': [1] * 3 + [0] * 3})

        # Define constraints on attribute columns in data frame
        price = Attribute(sequences_df['price'].values.tolist())
        price_ct = 3 <= price.median() <= 4
        attr_col_to_constraints = {'price': [price_ct]}

        # patterns_pos: [['A', 'D'], ['C', 'A']]
        # patterns_neg: [['A', 'D'], ['B', 'A']]
        dpm_patterns = dichotomic_pattern_mining(sequences_df, sequence_col_name='sequence', label_col_name='label',
                                                 attr_col_to_constraints=attr_col_to_constraints, min_frequency=2,
                                                 pattern_aggregation='unique_positive')

        self.assertListEqual([['C', 'A']], dpm_patterns)

    def test_dichotomic_pattern_mining_unique_neg(self):
        sequences_pos = [["A", "A", "B", "A", "D"],
                         ["C", "B", "A"],
                         ["C", "A", "C", "D"]]

        # update attributes in the 2nd and 3rd row to add ['C', 'A']
        values_pos = [[5, 5, 3, 8, 2],
                      [3, 3, 3],
                      [3, 5, 2, 1]]

        sequences_neg = [["A", "A", "B", "A", "D"],
                         ["C", "B", "A"],
                         ["C", "A", "C", "D"]]

        # Updating attributes in the first row to add ['B', 'A']
        values_neg = [[5, 5, 3, 3, 2],
                      [1, 3, 3],
                      [4, 5, 2, 1]]

        # Sequence data frame
        sequences_df = pd.DataFrame({'sequence': sequences_pos + sequences_neg, 'price': values_pos + values_neg,
                                     'label': [1] * 3 + [0] * 3})

        # Define constraints on attribute columns in data frame
        price = Attribute(sequences_df['price'].values.tolist())
        price_ct = 3 <= price.median() <= 4
        attr_col_to_constraints = {'price': [price_ct]}

        # patterns_pos: [['A', 'D'], ['C', 'A']]
        # patterns_neg: [['A', 'D'], ['B', 'A']]
        dpm_patterns = dichotomic_pattern_mining(sequences_df, sequence_col_name='sequence', label_col_name='label',
                                                 attr_col_to_constraints=attr_col_to_constraints, min_frequency=2,
                                                 pattern_aggregation='unique_negative')

        self.assertListEqual([['B', 'A']], dpm_patterns)

    def test_dpm_and_encoding_usage_union(self):
        sequences_pos = [["A", "A", "B", "A", "D"],
                         ["C", "B", "A"],
                         ["C", "A", "C", "D"]]

        # update attributes in the 2nd and 3rd row to add ['C', 'A']
        values_pos = [[5, 5, 3, 8, 2],
                      [3, 3, 3],
                      [3, 5, 2, 1]]

        sequences_neg = [["A", "A", "B", "A", "D"],
                         ["C", "B", "A"],
                         ["C", "A", "C", "D"]]

        # Updating attributes in the first row to add ['B', 'A']
        values_neg = [[5, 5, 3, 3, 2],
                      [1, 3, 3],
                      [4, 5, 2, 1]]

        # Sequence data frame
        sequences_df = pd.DataFrame({'sequence': sequences_pos + sequences_neg, 'price': values_pos + values_neg,
                                     'label': [1] * 3 + [0] * 3})

        # Define constraints on attribute columns in data frame
        price = Attribute(sequences_df['price'].values.tolist())
        price_ct = 3 <= price.median() <= 4
        attr_col_to_constraints = {'price': [price_ct]}

        # patterns_pos: [['A', 'D'], ['C', 'A']]
        # patterns_neg: [['A', 'D'], ['B', 'A']]
        dpm_patterns = dichotomic_pattern_mining(sequences_df, sequence_col_name='sequence', label_col_name='label',
                                                 attr_col_to_constraints=attr_col_to_constraints, min_frequency=2,
                                                 pattern_aggregation='union')

        # Create encoding
        sequences = sequences_df['sequence'].values.tolist()
        price = Attribute(sequences_df['price'].values.tolist())
        price_ct = 3 <= price.median() <= 4

        encodings = get_one_hot_encodings(sequences, dpm_patterns, constraints=[price_ct],
                                          drop_pattern_frequency=False)

        self.assertListEqual([[1, 0, 0], [0, 1, 1], [1, 0, 1],
                              [1, 1, 0], [0, 1, 0], [1, 0, 0]], encodings.values[:, 1:].tolist())

    def test_dpm_and_encoding_usage_intersection(self):
        sequences_pos = [["A", "A", "B", "A", "D"],
                         ["C", "B", "A"],
                         ["C", "A", "C", "D"]]

        # update attributes in the 2nd and 3rd row to add ['C', 'A']
        values_pos = [[5, 5, 3, 8, 2],
                      [3, 3, 3],
                      [3, 5, 2, 1]]

        sequences_neg = [["A", "A", "B", "A", "D"],
                         ["C", "B", "A"],
                         ["C", "A", "C", "D"]]

        # Updating attributes in the first row to add ['B', 'A']
        values_neg = [[5, 5, 3, 3, 2],
                      [1, 3, 3],
                      [4, 5, 2, 1]]

        # Sequence data frame
        sequences_df = pd.DataFrame({'sequence': sequences_pos + sequences_neg, 'price': values_pos + values_neg,
                                     'label': [1] * 3 + [0] * 3})

        # Define constraints on attribute columns in data frame
        price = Attribute(sequences_df['price'].values.tolist())
        price_ct = 3 <= price.median() <= 4
        attr_col_to_constraints = {'price': [price_ct]}

        # patterns_pos: [['A', 'D'], ['C', 'A']]
        # patterns_neg: [['A', 'D'], ['B', 'A']]
        dpm_patterns = dichotomic_pattern_mining(sequences_df, sequence_col_name='sequence', label_col_name='label',
                                                 attr_col_to_constraints=attr_col_to_constraints, min_frequency=2,
                                                 pattern_aggregation='intersection')

        # Create encoding
        sequences = sequences_df['sequence'].values.tolist()
        price = Attribute(sequences_df['price'].values.tolist())
        price_ct = 3 <= price.median() <= 4

        encodings = get_one_hot_encodings(sequences, dpm_patterns, constraints=[price_ct],
                                          drop_pattern_frequency=False)

        self.assertListEqual([[1], [0], [1],
                              [1], [0], [1]], encodings.values[:, 1:].tolist())

    def test_dpm_and_encoding_usage_unique_pos(self):
        sequences_pos = [["A", "A", "B", "A", "D"],
                         ["C", "B", "A"],
                         ["C", "A", "C", "D"]]

        # update attributes in the 2nd and 3rd row to add ['C', 'A']
        values_pos = [[5, 5, 3, 8, 2],
                      [3, 3, 3],
                      [3, 5, 2, 1]]

        sequences_neg = [["A", "A", "B", "A", "D"],
                         ["C", "B", "A"],
                         ["C", "A", "C", "D"]]

        # Updating attributes in the first row to add ['B', 'A']
        values_neg = [[5, 5, 3, 3, 2],
                      [1, 3, 3],
                      [4, 5, 2, 1]]

        # Sequence data frame
        sequences_df = pd.DataFrame({'sequence': sequences_pos + sequences_neg, 'price': values_pos + values_neg,
                                     'label': [1] * 3 + [0] * 3})

        # Define constraints on attribute columns in data frame
        price = Attribute(sequences_df['price'].values.tolist())
        price_ct = 3 <= price.median() <= 4
        attr_col_to_constraints = {'price': [price_ct]}

        # patterns_pos: [['A', 'D'], ['C', 'A']]
        # patterns_neg: [['A', 'D'], ['B', 'A']]
        dpm_patterns = dichotomic_pattern_mining(sequences_df, sequence_col_name='sequence', label_col_name='label',
                                                 attr_col_to_constraints=attr_col_to_constraints, min_frequency=2,
                                                 pattern_aggregation='unique_positive')

        # Create encoding
        sequences = sequences_df['sequence'].values.tolist()
        price = Attribute(sequences_df['price'].values.tolist())
        price_ct = 3 <= price.median() <= 4

        encodings = get_one_hot_encodings(sequences, dpm_patterns, constraints=[price_ct],
                                          drop_pattern_frequency=False)

        self.assertListEqual([[0], [1], [1],
                              [0], [0], [0]], encodings.values[:, 1:].tolist())

    def test_dpm_and_encoding_usage_unique_neg(self):
        sequences_pos = [["A", "A", "B", "A", "D"],
                         ["C", "B", "A"],
                         ["C", "A", "C", "D"]]

        # update attributes in the 2nd and 3rd row to add ['C', 'A']
        values_pos = [[5, 5, 3, 8, 2],
                      [3, 3, 3],
                      [3, 5, 2, 1]]

        sequences_neg = [["A", "A", "B", "A", "D"],
                         ["C", "B", "A"],
                         ["C", "A", "C", "D"]]

        # Updating attributes in the first row to add ['B', 'A']
        values_neg = [[5, 5, 3, 3, 2],
                      [1, 3, 3],
                      [4, 5, 2, 1]]

        # Sequence data frame
        sequences_df = pd.DataFrame({'sequence': sequences_pos + sequences_neg, 'price': values_pos + values_neg,
                                     'label': [1] * 3 + [0] * 3})

        # Define constraints on attribute columns in data frame
        price = Attribute(sequences_df['price'].values.tolist())
        price_ct = 3 <= price.median() <= 4
        attr_col_to_constraints = {'price': [price_ct]}

        # patterns_pos: [['A', 'D'], ['C', 'A']]
        # patterns_neg: [['A', 'D'], ['B', 'A']]
        dpm_patterns = dichotomic_pattern_mining(sequences_df, sequence_col_name='sequence', label_col_name='label',
                                                 attr_col_to_constraints=attr_col_to_constraints, min_frequency=2,
                                                 pattern_aggregation='unique_negative')

        # Create encoding
        sequences = sequences_df['sequence'].values.tolist()
        price = Attribute(sequences_df['price'].values.tolist())
        price_ct = 3 <= price.median() <= 4

        encodings = get_one_hot_encodings(sequences, dpm_patterns, constraints=[price_ct],
                                          drop_pattern_frequency=False)

        self.assertListEqual([[0], [1], [0],
                              [1], [1], [0]], encodings.values[:, 1:].tolist())

    def test_dpm_and_encoding_usage_union_wo_constraints(self):
        sequences_pos = [["A", "A", "B", "A", "D"],
                         ["C", "B", "A"],
                         ["C", "A", "C", "D"]]

        # update attributes in the 2nd and 3rd row to add ['C', 'A']
        values_pos = [[5, 5, 3, 8, 2],
                      [3, 3, 3],
                      [3, 5, 2, 1]]

        sequences_neg = [["A", "A", "B", "A", "D"],
                         ["C", "B", "A"],
                         ["C", "A", "C", "D"]]

        # Updating attributes in the first row to add ['B', 'A']
        values_neg = [[5, 5, 3, 3, 2],
                      [1, 3, 3],
                      [4, 5, 2, 1]]

        # Sequence data frame
        sequences_df = pd.DataFrame({'sequence': sequences_pos + sequences_neg, 'price': values_pos + values_neg,
                                     'label': [1] * 3 + [0] * 3})

        # Define constraints on attribute columns in data frame
        price = Attribute(sequences_df['price'].values.tolist())
        price_ct = 3 <= price.median() <= 4
        attr_col_to_constraints = {'price': [price_ct]}

        # patterns_pos: [['A', 'D'], ['C', 'A']]
        # patterns_neg: [['A', 'D'], ['B', 'A']]
        dpm_patterns = dichotomic_pattern_mining(sequences_df, sequence_col_name='sequence', label_col_name='label',
                                                 attr_col_to_constraints=attr_col_to_constraints, min_frequency=2,
                                                 pattern_aggregation='union')

        # Create encoding
        sequences = sequences_df['sequence'].values.tolist()

        encodings = get_one_hot_encodings(sequences, dpm_patterns,
                                          drop_pattern_frequency=False)

        self.assertListEqual([[1, 1, 0], [0, 1, 1], [1, 0, 1],
                              [1, 1, 0], [0, 1, 1], [1, 0, 1]], encodings.values[:, 1:].tolist())

    def test_dpm_usage_all_aggregate_operations(self):
        sequences_pos = [["A", "A", "B", "A", "D"],
                         ["C", "B", "A"],
                         ["C", "A", "C", "D"]]

        # update attributes in the 2nd and 3rd row to add ['C', 'A']
        values_pos = [[5, 5, 3, 8, 2],
                      [3, 3, 3],
                      [3, 5, 2, 1]]

        sequences_neg = [["A", "A", "B", "A", "D"],
                         ["C", "B", "A"],
                         ["C", "A", "C", "D"]]

        # Updating attributes in the first row to add ['B', 'A']
        values_neg = [[5, 5, 3, 3, 2],
                      [1, 3, 3],
                      [4, 5, 2, 1]]

        # Sequence data frame
        sequences_df = pd.DataFrame({'sequence': sequences_pos + sequences_neg, 'price': values_pos + values_neg,
                                     'label': [1] * 3 + [0] * 3})

        # Define constraints on attribute columns in data frame
        price = Attribute(sequences_df['price'].values.tolist())
        price_ct = 3 <= price.median() <= 4
        attr_col_to_constraints = {'price': [price_ct]}

        # patterns_pos: [['A', 'D'], ['C', 'A']]
        # patterns_neg: [['A', 'D'], ['B', 'A']]
        dpm_patterns = dichotomic_pattern_mining(sequences_df, sequence_col_name='sequence', label_col_name='label',
                                                 attr_col_to_constraints=attr_col_to_constraints, min_frequency=2,
                                                 pattern_aggregation='all')

        self.assertEqual(len(dpm_patterns), 4)
        self.assertListEqual([['A', 'D'], ['B', 'A'], ['C', 'A']], dpm_patterns[0])
        self.assertListEqual([['A', 'D']], dpm_patterns[1])
        self.assertListEqual([['C', 'A']], dpm_patterns[2])
        self.assertListEqual([['B', 'A']], dpm_patterns[3])


if __name__ == '__main__':
    unittest.main()