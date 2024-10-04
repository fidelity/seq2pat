# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0

import os
import unittest

from sequential.seq2pat import Seq2Pat, Attribute
from sequential.pat2feat import Pat2Feat
from sequential.dpm import dichotomic_pattern_mining, DichotomicAggregation


class TestDPMUtils(unittest.TestCase):
    TEST_DIR = os.path.dirname(os.path.abspath(__file__))
    DATA_DIR = TEST_DIR + os.sep + "data" + os.sep

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

        # Define seq2pat_pos for positive cohort
        seq2pat_pos = Seq2Pat(sequences=sequences_pos)
        price_attr_pos = Attribute(values=values_pos)
        price_attr_ct_pos = 3 <= price_attr_pos.median() <= 4
        seq2pat_pos.add_constraint(price_attr_ct_pos)

        # Define seq2pat_neg for negative cohort
        seq2pat_neg = Seq2Pat(sequences=sequences_neg)
        price_attr_neg = Attribute(values=values_neg)
        price_attr_ct_neg = 3 <= price_attr_neg.median() <= 4
        seq2pat_neg.add_constraint(price_attr_ct_neg)

        # patterns_pos: [['A', 'D'], ['C', 'A']]
        # patterns_neg: [['A', 'D'], ['B', 'A']]
        aggregation_to_patterns = dichotomic_pattern_mining(seq2pat_pos, seq2pat_neg,
                                                            min_frequency_pos=2, min_frequency_neg=2)
        dpm_patterns = aggregation_to_patterns[DichotomicAggregation.union]

        self.assertListEqual([['A', 'D'], ['B', 'A'], ['C', 'A']], dpm_patterns)

    def test_dichotomic_pattern_mining_union_diff_min_freq(self):
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

        # Define seq2pat_pos for positive cohort
        seq2pat_pos = Seq2Pat(sequences=sequences_pos)
        price_attr_pos = Attribute(values=values_pos)
        price_attr_ct_pos = 3 <= price_attr_pos.median() <= 4
        seq2pat_pos.add_constraint(price_attr_ct_pos)

        # Define seq2pat_neg for negative cohort
        seq2pat_neg = Seq2Pat(sequences=sequences_neg)
        price_attr_neg = Attribute(values=values_neg)
        price_attr_ct_neg = 3 <= price_attr_neg.median() <= 4
        seq2pat_neg.add_constraint(price_attr_ct_neg)

        # patterns_pos: [['A', 'D'], ['C', 'A']]
        # patterns_neg: [['A', 'D'], ['B', 'A']]
        aggregation_to_patterns = dichotomic_pattern_mining(seq2pat_pos, seq2pat_neg,
                                                            min_frequency_pos=1, min_frequency_neg=2)
        dpm_patterns = aggregation_to_patterns[DichotomicAggregation.union]

        self.assertListEqual([['A', 'A', 'B', 'D'], ['A', 'B'], ['A', 'B', 'A', 'D'], ['A', 'B', 'D'], ['A', 'C'],
                              ['A', 'D'], ['B', 'A'], ['B', 'A', 'D'], ['C', 'A'], ['C', 'A', 'C'],
                              ['C', 'A', 'D'], ['C', 'B'], ['C', 'B', 'A']], dpm_patterns)

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

        # Define seq2pat_pos for positive cohort
        seq2pat_pos = Seq2Pat(sequences=sequences_pos)
        price_attr_pos = Attribute(values=values_pos)
        price_attr_ct_pos = 3 <= price_attr_pos.median() <= 4
        seq2pat_pos.add_constraint(price_attr_ct_pos)

        # Define seq2pat_neg for negative cohort
        seq2pat_neg = Seq2Pat(sequences=sequences_neg)
        price_attr_neg = Attribute(values=values_neg)
        price_attr_ct_neg = 3 <= price_attr_neg.median() <= 4
        seq2pat_neg.add_constraint(price_attr_ct_neg)

        # patterns_pos: [['A', 'D'], ['C', 'A']]
        # patterns_neg: [['A', 'D'], ['B', 'A']]
        aggregation_to_patterns = dichotomic_pattern_mining(seq2pat_pos, seq2pat_neg,
                                                            min_frequency_pos=2, min_frequency_neg=2)
        dpm_patterns = aggregation_to_patterns[DichotomicAggregation.intersection]

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

        # Define seq2pat_pos for positive cohort
        seq2pat_pos = Seq2Pat(sequences=sequences_pos)
        price_attr_pos = Attribute(values=values_pos)
        price_attr_ct_pos = 3 <= price_attr_pos.median() <= 4
        seq2pat_pos.add_constraint(price_attr_ct_pos)

        # Define seq2pat_neg for negative cohort
        seq2pat_neg = Seq2Pat(sequences=sequences_neg)
        price_attr_neg = Attribute(values=values_neg)
        price_attr_ct_neg = 3 <= price_attr_neg.median() <= 4
        seq2pat_neg.add_constraint(price_attr_ct_neg)

        # patterns_pos: [['A', 'D'], ['C', 'A']]
        # patterns_neg: [['A', 'D'], ['B', 'A']]
        aggregation_to_patterns = dichotomic_pattern_mining(seq2pat_pos, seq2pat_neg,
                                                            min_frequency_pos=2, min_frequency_neg=2)
        dpm_patterns = aggregation_to_patterns[DichotomicAggregation.unique_pos]

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

        # Define seq2pat_pos for positive cohort
        seq2pat_pos = Seq2Pat(sequences=sequences_pos)
        price_attr_pos = Attribute(values=values_pos)
        price_attr_ct_pos = 3 <= price_attr_pos.median() <= 4
        seq2pat_pos.add_constraint(price_attr_ct_pos)

        # Define seq2pat_neg for negative cohort
        seq2pat_neg = Seq2Pat(sequences=sequences_neg)
        price_attr_neg = Attribute(values=values_neg)
        price_attr_ct_neg = 3 <= price_attr_neg.median() <= 4
        seq2pat_neg.add_constraint(price_attr_ct_neg)

        # patterns_pos: [['A', 'D'], ['C', 'A']]
        # patterns_neg: [['A', 'D'], ['B', 'A']]
        aggregation_to_patterns = dichotomic_pattern_mining(seq2pat_pos, seq2pat_neg,
                                                            min_frequency_pos=2, min_frequency_neg=2)
        dpm_patterns = aggregation_to_patterns[DichotomicAggregation.unique_neg]

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

        # Define seq2pat_pos for positive cohort
        seq2pat_pos = Seq2Pat(sequences=sequences_pos)
        price_attr_pos = Attribute(values=values_pos)
        price_attr_ct_pos = 3 <= price_attr_pos.median() <= 4
        seq2pat_pos.add_constraint(price_attr_ct_pos)

        # Define seq2pat_neg for negative cohort
        seq2pat_neg = Seq2Pat(sequences=sequences_neg)
        price_attr_neg = Attribute(values=values_neg)
        price_attr_ct_neg = 3 <= price_attr_neg.median() <= 4
        seq2pat_neg.add_constraint(price_attr_ct_neg)

        sequences = sequences_pos + sequences_neg

        # patterns_pos: [['A', 'D'], ['C', 'A']]
        # patterns_neg: [['A', 'D'], ['B', 'A']]
        aggregation_to_patterns = dichotomic_pattern_mining(seq2pat_pos, seq2pat_neg,
                                                            min_frequency_pos=2, min_frequency_neg=2)
        dpm_patterns = aggregation_to_patterns[DichotomicAggregation.union]

        # Create encoding
        price = Attribute(values=values_pos + values_neg)
        price_ct = 3 <= price.median() <= 4

        pat2feat = Pat2Feat()
        encodings = pat2feat.get_features(sequences, dpm_patterns, constraints=[price_ct],
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

        # Define seq2pat_pos for positive cohort
        seq2pat_pos = Seq2Pat(sequences=sequences_pos)
        price_attr_pos = Attribute(values=values_pos)
        price_attr_ct_pos = 3 <= price_attr_pos.median() <= 4
        seq2pat_pos.add_constraint(price_attr_ct_pos)

        # Define seq2pat_neg for negative cohort
        seq2pat_neg = Seq2Pat(sequences=sequences_neg)
        price_attr_neg = Attribute(values=values_neg)
        price_attr_ct_neg = 3 <= price_attr_neg.median() <= 4
        seq2pat_neg.add_constraint(price_attr_ct_neg)

        sequences = sequences_pos + sequences_neg

        # patterns_pos: [['A', 'D'], ['C', 'A']]
        # patterns_neg: [['A', 'D'], ['B', 'A']]
        aggregation_to_patterns = dichotomic_pattern_mining(seq2pat_pos, seq2pat_neg,
                                                            min_frequency_pos=2, min_frequency_neg=2)
        dpm_patterns = aggregation_to_patterns[DichotomicAggregation.intersection]

        # Create encoding
        price = Attribute(values=values_pos + values_neg)
        price_ct = 3 <= price.median() <= 4

        pat2feat = Pat2Feat()
        encodings = pat2feat.get_features(sequences, dpm_patterns, constraints=[price_ct],
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

        # Define seq2pat_pos for positive cohort
        seq2pat_pos = Seq2Pat(sequences=sequences_pos)
        price_attr_pos = Attribute(values=values_pos)
        price_attr_ct_pos = 3 <= price_attr_pos.median() <= 4
        seq2pat_pos.add_constraint(price_attr_ct_pos)

        # Define seq2pat_neg for negative cohort
        seq2pat_neg = Seq2Pat(sequences=sequences_neg)
        price_attr_neg = Attribute(values=values_neg)
        price_attr_ct_neg = 3 <= price_attr_neg.median() <= 4
        seq2pat_neg.add_constraint(price_attr_ct_neg)

        sequences = sequences_pos + sequences_neg

        # patterns_pos: [['A', 'D'], ['C', 'A']]
        # patterns_neg: [['A', 'D'], ['B', 'A']]
        aggregation_to_patterns = dichotomic_pattern_mining(seq2pat_pos, seq2pat_neg,
                                                            min_frequency_pos=2, min_frequency_neg=2)
        dpm_patterns = aggregation_to_patterns[DichotomicAggregation.unique_pos]

        # Create encoding
        price = Attribute(values=values_pos + values_neg)
        price_ct = 3 <= price.median() <= 4

        pat2feat = Pat2Feat()
        encodings = pat2feat.get_features(sequences, dpm_patterns, constraints=[price_ct],
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

        # Define seq2pat_pos for positive cohort
        seq2pat_pos = Seq2Pat(sequences=sequences_pos)
        price_attr_pos = Attribute(values=values_pos)
        price_attr_ct_pos = 3 <= price_attr_pos.median() <= 4
        seq2pat_pos.add_constraint(price_attr_ct_pos)

        # Define seq2pat_neg for negative cohort
        seq2pat_neg = Seq2Pat(sequences=sequences_neg)
        price_attr_neg = Attribute(values=values_neg)
        price_attr_ct_neg = 3 <= price_attr_neg.median() <= 4
        seq2pat_neg.add_constraint(price_attr_ct_neg)

        sequences = sequences_pos + sequences_neg

        # patterns_pos: [['A', 'D'], ['C', 'A']]
        # patterns_neg: [['A', 'D'], ['B', 'A']]
        aggregation_to_patterns = dichotomic_pattern_mining(seq2pat_pos, seq2pat_neg,
                                                            min_frequency_pos=2, min_frequency_neg=2)
        dpm_patterns = aggregation_to_patterns[DichotomicAggregation.unique_neg]

        # Create encoding
        price = Attribute(values=values_pos + values_neg)
        price_ct = 3 <= price.median() <= 4

        pat2feat = Pat2Feat()
        encodings = pat2feat.get_features(sequences, dpm_patterns, constraints=[price_ct],
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

        # Define seq2pat_pos for positive cohort
        seq2pat_pos = Seq2Pat(sequences=sequences_pos)
        price_attr_pos = Attribute(values=values_pos)
        price_attr_ct_pos = 3 <= price_attr_pos.median() <= 4
        seq2pat_pos.add_constraint(price_attr_ct_pos)

        # Define seq2pat_neg for negative cohort
        seq2pat_neg = Seq2Pat(sequences=sequences_neg)
        price_attr_neg = Attribute(values=values_neg)
        price_attr_ct_neg = 3 <= price_attr_neg.median() <= 4
        seq2pat_neg.add_constraint(price_attr_ct_neg)

        sequences = sequences_pos + sequences_neg

        # patterns_pos: [['A', 'D'], ['C', 'A']]
        # patterns_neg: [['A', 'D'], ['B', 'A']]
        aggregation_to_patterns = dichotomic_pattern_mining(seq2pat_pos, seq2pat_neg,
                                                            min_frequency_pos=2, min_frequency_neg=2)
        dpm_patterns = aggregation_to_patterns[DichotomicAggregation.union]

        pat2feat = Pat2Feat()
        encodings = pat2feat.get_features(sequences, dpm_patterns,
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

        # Define seq2pat_pos for positive cohort
        seq2pat_pos = Seq2Pat(sequences=sequences_pos)
        price_attr_pos = Attribute(values=values_pos)
        price_attr_ct_pos = 3 <= price_attr_pos.median() <= 4
        seq2pat_pos.add_constraint(price_attr_ct_pos)

        # Define seq2pat_neg for negative cohort
        seq2pat_neg = Seq2Pat(sequences=sequences_neg)
        price_attr_neg = Attribute(values=values_neg)
        price_attr_ct_neg = 3 <= price_attr_neg.median() <= 4
        seq2pat_neg.add_constraint(price_attr_ct_neg)

        # patterns_pos: [['A', 'D'], ['C', 'A']]
        # patterns_neg: [['A', 'D'], ['B', 'A']]
        aggregation_to_patterns = dichotomic_pattern_mining(seq2pat_pos, seq2pat_neg, min_frequency_pos=2,
                                                            min_frequency_neg=2)

        self.assertEqual(len(aggregation_to_patterns), 4)
        self.assertListEqual([['A', 'D'], ['B', 'A'], ['C', 'A']], aggregation_to_patterns[DichotomicAggregation.union])
        self.assertListEqual([['A', 'D']], aggregation_to_patterns[DichotomicAggregation.intersection])
        self.assertListEqual([['C', 'A']], aggregation_to_patterns[DichotomicAggregation.unique_pos])
        self.assertListEqual([['B', 'A']], aggregation_to_patterns[DichotomicAggregation.unique_neg])

    def test_dichotomic_pattern_mining_quick_start(self):
        # Create seq2pat model for positive sequences
        sequences_pos = [["A", "A", "B", "A", "D"]]
        seq2pat_pos = Seq2Pat(sequences=sequences_pos)

        # Create seq2pat model for negative sequences
        sequences_neg = [["C", "B", "A"], ["C", "A", "C", "D"]]
        seq2pat_neg = Seq2Pat(sequences=sequences_neg)

        # Run DPM to get mined patterns
        aggregation_to_patterns = dichotomic_pattern_mining(seq2pat_pos, seq2pat_neg,
                                                            min_frequency_pos=1, min_frequency_neg=2)

        # DPM patterns with Union aggregation
        dpm_patterns = aggregation_to_patterns[DichotomicAggregation.union]

        # Encodings of all sequences
        sequences = sequences_pos + sequences_neg
        pat2feat = Pat2Feat()
        encodings = pat2feat.get_features(sequences, dpm_patterns,
                                          drop_pattern_frequency=False)

        self.assertListEqual([['A', 'A'], ['A', 'A', 'A'], ['A', 'A', 'A', 'D'], ['A', 'A', 'B'],
                              ['A', 'A', 'B', 'A'], ['A', 'A', 'B', 'A', 'D'], ['A', 'A', 'B', 'D'],
                              ['A', 'A', 'D'], ['A', 'B'], ['A', 'B', 'A'], ['A', 'B', 'A', 'D'],
                              ['A', 'B', 'D'], ['A', 'D'], ['B', 'A'], ['B', 'A', 'D'],
                              ['B', 'D'], ['C', 'A']], dpm_patterns)

        self.assertListEqual([[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
                              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1],
                              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1]],
                             encodings.values[:, 1:].tolist())


if __name__ == '__main__':
    unittest.main()
