# -*- coding: utf-8 -*-
# SPDX-License-Identifier: GPL-2.0
import collections
import os
import unittest

from sequential.seq2pat import Seq2Pat, Attribute
from sequential.utils import (read_data, get_max_column_size, get_max_value, compare_results, sort_pattern,
                              list_to_counter, counter_to_list)
from sequential.backend import seq_to_pat as stp


class TestSeq2PatBatch(unittest.TestCase):
    TEST_DIR = os.path.dirname(os.path.abspath(__file__))
    DATA_DIR = TEST_DIR + os.sep + "data" + os.sep

    def test_list_to_counter(self):
        patterns = [[11, 12, 1],
                    [11, 12, 13, 1],
                    [11, 13, 1],
                    [12, 13, 1]]

        counter = list_to_counter(patterns)

        self.assertEqual(counter, collections.Counter({(11, 12): 1, (11, 12, 13): 1, (11, 13): 1, (12, 13): 1}))

    def test_counter_to_list(self):
        counter = collections.Counter({(11, 12): 1, (11, 12, 13): 2, (11, 13): 1, (12, 13): 1})

        results = counter_to_list(counter, min_row_count=2)

        self.assertEqual(results, [[11, 12, 13, 2]])

    def test_batch_patterns_default_equal(self):
        # Seq2Pat over 3 sequences
        seq2pat = Seq2Pat(sequences=[["A", "C", "B", "A", "D"],
                                     ["C", "B", "A"],
                                     ["C", "A", "C", "D"]])

        # Patterns
        patterns = seq2pat.get_patterns(min_frequency=1.0)

        seq2pat = Seq2Pat(sequences=[["A", "C", "B", "A", "D"],
                                     ["C", "B", "A"],
                                     ["C", "A", "C", "D"]], batch_size=2)

        # Patterns
        batch_patterns = seq2pat.get_patterns(min_frequency=1.0)

        self.assertEqual(patterns, batch_patterns)

    def test_batch_patterns_constraints_equal(self):
        # Seq2Pat over 3 sequences
        seq2pat = Seq2Pat(sequences=[["A", "C", "B", "A", "D"],
                                     ["C", "B", "A"],
                                     ["C", "A", "C", "D"]])

        # Attribute - I: Price
        price = Attribute(values=[[5, 5, 3, 8, 2],
                                  [1, 3, 3],
                                  [4, 5, 2, 1]])

        # Attribute - II: Timestamp
        timestamp = Attribute(values=[[1, 1, 2, 3, 3],
                                      [3, 8, 9],
                                      [2, 5, 5, 7]])

        # Add Constraint
        avg_constraint = 3 <= price.average() <= 4
        seq2pat.add_constraint(avg_constraint)

        # Patterns
        patterns = seq2pat.get_patterns(min_frequency=0.8)

        seq2pat = Seq2Pat(sequences=[["A", "C", "B", "A", "D"],
                                     ["C", "B", "A"],
                                     ["C", "A", "C", "D"]], batch_size=2)

        # Attribute - I: Price
        price = Attribute(values=[[5, 5, 3, 8, 2],
                                  [1, 3, 3],
                                  [4, 5, 2, 1]])

        # Attribute - II: Timestamp
        timestamp = Attribute(values=[[1, 1, 2, 3, 3],
                                      [3, 8, 9],
                                      [2, 5, 5, 7]])

        # Add Constraint
        avg_constraint = 3 <= price.average() <= 4
        seq2pat.add_constraint(avg_constraint)

        # Patterns
        batch_patterns = seq2pat.get_patterns(min_frequency=0.8)

        self.assertEqual(patterns, batch_patterns)

    def test_input_no_upper_constraint_batch(self):
        # API and Cython object test. Replicates command line:
        # ./MPP -file input.txt -thr 0.01 -att input_att1.txt -lg 30 -ls 900 -att input_att2.txt -la 30 -lm 40 -out -write BMS_patt.txt
        # input on Main.cpp and verifies output with data captured from original implementation
        # Similar to default but no upper constraints imposed

        # Seq2Pat
        patterns_file = self.DATA_DIR + "input.txt"
        sequences = read_data(patterns_file)
        seq2pat = Seq2Pat(sequences, max_span=None, batch_size=30000)

        # Load Attributes
        attribute_file = self.DATA_DIR + "input_att1.txt"
        attr1_data = read_data(attribute_file)
        att1 = Attribute(attr1_data)

        attribute_file = self.DATA_DIR + "input_att2.txt"
        attr2_data = read_data(attribute_file)
        att2 = Attribute(attr2_data)

        cts1 = seq2pat.add_constraint(30 <= att1.gap())
        cts2 = seq2pat.add_constraint(900 <= att1.span())
        cts3 = seq2pat.add_constraint(30 <= att2.average())
        cts4 = seq2pat.add_constraint(40 <= att2.median())

        test_patterns = seq2pat.get_patterns(.01)
        results_file = self.DATA_DIR + "no_upper_constraint_results.txt"
        control_patterns = read_data(results_file)
        sorted_control = sort_pattern(control_patterns)
        self.assertListEqual(sorted_control, test_patterns)

    def test_input_no_lower_constraint_batch(self):
        # API and Cython object test. Replicates command line:
        # ./MPP -file input.txt -thr 0.001 -att input_att1.txt -ug 900 - us 3600 -att input_att2.txt -ua 70 -um 60 -out -write BMS_patt.txt
        # input on Main.cpp and verifies output with data captured from original implementation
        # Similar to default but no lower constraints imposed

        # Seq2Pat
        patterns_file = self.DATA_DIR + "input.txt"
        sequences = read_data(patterns_file)
        seq2pat = Seq2Pat(sequences, max_span=None, batch_size=30000)

        # Load Attributes
        attribute_file = self.DATA_DIR + "input_att1.txt"
        attr1_data = read_data(attribute_file)
        att1 = Attribute(attr1_data)

        attribute_file = self.DATA_DIR + "input_att2.txt"
        attr2_data = read_data(attribute_file)
        att2 = Attribute(attr2_data)

        cts1 = seq2pat.add_constraint(att1.gap() <= 900)
        cts2 = seq2pat.add_constraint(att1.span() <= 3600)
        cts3 = seq2pat.add_constraint(att2.average() <= 70)
        cts4 = seq2pat.add_constraint(att2.median() <= 60)

        test_patterns = seq2pat.get_patterns(.001)
        results_file = self.DATA_DIR + "no_lower_constraint_results.txt"
        control_patterns = read_data(results_file)
        sorted_control = sort_pattern(control_patterns)
        self.assertListEqual(sorted_control, test_patterns)

    def test_repeated_calls_seq2pat_batch(self):
        # List of sequences
        sequences = [[11, 12, 13], [11, 12, 13, 14]]

        # Sequential pattern finder
        seq2pat = Seq2Pat(sequences, batch_size=2)

        unconstrained_result_1 = seq2pat.get_patterns(0.9)

        self.assertListEqual([[11, 12, 2], [11, 12, 13, 2], [11, 13, 2], [12, 13, 2], [11, 12, 13, 14, 1],
                              [11, 12, 14, 1], [11, 13, 14, 1], [11, 14, 1], [12, 13, 14, 1], [12, 14, 1],
                              [13, 14, 1]], unconstrained_result_1)

        unconstrained_result_2 = seq2pat.get_patterns(0.9)

        self.assertListEqual([[11, 12, 2], [11, 12, 13, 2], [11, 13, 2], [12, 13, 2], [11, 12, 13, 14, 1],
                              [11, 12, 14, 1], [11, 13, 14, 1], [11, 14, 1], [12, 13, 14, 1], [12, 14, 1],
                              [13, 14, 1]], unconstrained_result_2)

        unconstrained_result_3 = seq2pat.get_patterns(2)

        self.assertListEqual([[11, 12, 2], [11, 12, 13, 2], [11, 13, 2], [12, 13, 2]], unconstrained_result_3)

    def test_input_diff_constraint(self):
        # API and Cython object test. Replicates command line:
        # ./MPP -file input.txt -thr 0.001 -att input_att1.txt -lg 20 -ug 1000 -ls 800 - us 3700 -att input_att2.txt -la 20 -ua 80 -lm 30 -um 70 -out -write BMS_patt.txt
        # input on Main.cpp and verifies output with data captured from original implementation
        # Similar to default but all lower constraints lowered by 10 all upper constraints raised 10.
        # Significantly different results to default.

        # Seq2Pat
        patterns_file = self.DATA_DIR + "input.txt"
        sequences = read_data(patterns_file)
        seq2pat = Seq2Pat(sequences, max_span=None, batch_size=30000)

        # Load Attributes
        attribute_file = self.DATA_DIR + "input_att1.txt"
        attr1_data = read_data(attribute_file)
        att1 = Attribute(attr1_data)

        attribute_file = self.DATA_DIR + "input_att2.txt"
        attr2_data = read_data(attribute_file)
        att2 = Attribute(attr2_data)

        cts1 = seq2pat.add_constraint(20 <= att1.gap() <= 1000)
        cts2 = seq2pat.add_constraint(800 <= att1.span() <= 3700)
        cts3 = seq2pat.add_constraint(20 <= att2.average() <= 80)
        cts4 = seq2pat.add_constraint(30 <= att2.median() <= 70)

        test_patterns = seq2pat.get_patterns(.001)
        results_file = self.DATA_DIR + "diff_constraints_results.txt"
        control_patterns = read_data(results_file)
        sorted_control = sort_pattern(control_patterns)
        self.assertListEqual(sorted_control, test_patterns)

    def test_input_no_constraint_batch(self):
        # API and Cython object test. Replicates command line:
        # ./MPP -file input.txt -thr 0.01 -out
        # input on Main.cpp and verifies output with data captured from original implementation
        # Unconstrained call. Significantly different and larger results.
        # Seq2Pat
        patterns_file = self.DATA_DIR + "input.txt"
        sequences = read_data(patterns_file)
        seq2pat = Seq2Pat(sequences, max_span=None, batch_size=10000)

        test_patterns = seq2pat.get_patterns(.01)
        results_file = self.DATA_DIR + "no_constraints_results.txt"
        control_patterns = read_data(results_file)
        sorted_results = sort_pattern(control_patterns)
        self.assertListEqual(sorted_results, test_patterns)
        self.assertFalse(test_patterns == read_data(self.DATA_DIR + "default_results.txt"))

    def test_input_no_constraint_n_jobs(self):
        # API and Cython object test. Replicates command line:
        # ./MPP -file input.txt -thr 0.01 -out
        # input on Main.cpp and verifies output with data captured from original implementation
        # Unconstrained call. Significantly different and larger results.
        # Seq2Pat
        patterns_file = self.DATA_DIR + "input.txt"
        sequences = read_data(patterns_file)
        seq2pat = Seq2Pat(sequences, max_span=None, batch_size=10000, n_jobs=2)

        test_patterns = seq2pat.get_patterns(.01)
        results_file = self.DATA_DIR + "no_constraints_results.txt"
        control_patterns = read_data(results_file)
        sorted_results = sort_pattern(control_patterns)
        self.assertListEqual(sorted_results, test_patterns)
        self.assertFalse(test_patterns == read_data(self.DATA_DIR + "default_results.txt"))

    def test_seq2pat_batch_min_frequency_df_large(self):
        # API and Cython object test. Replicates command line:
        # ./MPP -file input.txt -thr 0.01 -out
        # input on Main.cpp and verifies output with data captured from original implementation
        # Unconstrained call. Significantly different and larger results.
        # Seq2Pat
        patterns_file = self.DATA_DIR + "input.txt"
        sequences = read_data(patterns_file)
        seq2pat = Seq2Pat(sequences, max_span=None, batch_size=10000, n_jobs=2, min_frequency_df=0.8)

        test_patterns = seq2pat.get_patterns(.01)
        results_file = self.DATA_DIR + "no_constraints_results.txt"
        control_patterns = read_data(results_file)
        sorted_results = sort_pattern(control_patterns)
        self.assertListEqual(sorted_results[:60], test_patterns[:60])
        self.assertFalse(sorted_results[61] == test_patterns[61])
        self.assertFalse(test_patterns == read_data(self.DATA_DIR + "default_results.txt"))

    def test_seq2pat_batch_min_frequency_df_small(self):
        # API and Cython object test. Replicates command line:
        # ./MPP -file input.txt -thr 0.01 -out
        # input on Main.cpp and verifies output with data captured from original implementation
        # Unconstrained call. Significantly different and larger results.
        # Seq2Pat
        patterns_file = self.DATA_DIR + "input.txt"
        sequences = read_data(patterns_file)
        seq2pat = Seq2Pat(sequences, max_span=None, batch_size=10000, n_jobs=2, min_frequency_df=0.2)

        test_patterns = seq2pat.get_patterns(.01)
        results_file = self.DATA_DIR + "no_constraints_results.txt"
        control_patterns = read_data(results_file)
        sorted_results = sort_pattern(control_patterns)
        self.assertListEqual(sorted_results, test_patterns)
        self.assertFalse(test_patterns == read_data(self.DATA_DIR + "default_results.txt"))


if __name__ == '__main__':
    unittest.main()