# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0
import collections
import os
import unittest

from sequential.seq2pat import Seq2Pat, Attribute
from sequential.utils import read_data, sort_pattern, list_to_counter, counter_to_list


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
        # Test running seq2pat in batches under constraints
        # Command: ./MPP -file input.txt -thr 0.001 -att input_att1.txt -lg 900 -ls 3600 -att input_att2.txt
        # -la 70 -lm 60 -out -write BMS_patt.txt, to get results from original implementation
        # Results from original implementation and seq2pat should be the same

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
        # Test running seq2pat in batches under constraints
        # Command: ./MPP -file input.txt -thr 0.001 -att input_att1.txt -ug 900 - us 3600 -att input_att2.txt
        # -ua 70 -um 60 -out -write BMS_patt.txt, to get results from original implementation
        # Results from original implementation and seq2pat should be the same

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

    def test_seq2pat_batch_default_constraints(self):
        # Command line:
        #   > ./MPP.exe
        #       -file input.txt
        #       -thr 0.001
        #       -att input_att1.txt -lg 30 -ug 900 -ls 900 - us 3600
        #       -att input_att2.txt -la 30 -ua 70 -lm 40 -um 60
        #       -out -write BMS_patt.txt
        # This is default usage example in original implementation
        # Results from original implementation and seq2pat should be the same

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

        cts1 = seq2pat.add_constraint(30 <= att1.gap() <= 900)
        cts2 = seq2pat.add_constraint(900 <= att1.span())
        cts3 = seq2pat.add_constraint(30 <= att2.average() <= 70)
        cts4 = seq2pat.add_constraint(40 <= att2.median() <= 60)
        test_pf = seq2pat._get_cython_imp(-1)

        self.assertListEqual([30], test_pf.lgap)
        self.assertListEqual([900], test_pf.ugap)
        self.assertListEqual([30], test_pf.lavr)
        self.assertListEqual([70], test_pf.uavr)
        self.assertListEqual([900], test_pf.lspn)
        self.assertListEqual([], test_pf.uspn)
        self.assertListEqual([40], test_pf.lmed)

        self.assertListEqual([0], test_pf.ugapi)
        self.assertListEqual([0], test_pf.lgapi)
        self.assertListEqual([], test_pf.uspni)
        self.assertListEqual([0], test_pf.lspni)
        self.assertListEqual([1], test_pf.uavri)
        self.assertListEqual([1], test_pf.lavri)
        self.assertListEqual([1], test_pf.umedi)
        self.assertListEqual([1], test_pf.lmedi)

        self.assertListEqual([2, 0], test_pf.num_minmax)
        self.assertListEqual([0, 2], test_pf.num_avr)
        self.assertListEqual([0, 2], test_pf.num_med)
        self.assertListEqual([0], test_pf.tot_gap)
        self.assertListEqual([0], test_pf.tot_spn)
        self.assertListEqual([1], test_pf.tot_avr)

        self.assertEqual(161, test_pf.M)
        self.assertEqual(52619, test_pf.N)
        self.assertEqual(3340, test_pf.L)

        self.assertListEqual([284871, 100], test_pf.max_attrs)
        self.assertListEqual([0, 1], test_pf.min_attrs)

        test_patterns = seq2pat.get_patterns(.001)

        # Consistency sanity check
        dup_patterns = seq2pat.get_patterns(.001)
        self.assertListEqual(test_patterns, dup_patterns)

        results_file = self.DATA_DIR + "default_results.txt"

        control_patterns = read_data(results_file)
        sorted_control = sort_pattern(control_patterns)
        self.assertListEqual(sorted_control, test_patterns)

        # Remove constraint and test
        cts5 = seq2pat.remove_constraint(40 <= att2.median() <= 60)
        ct6 = seq2pat.remove_constraint(30 <= att2.average() <= 70)
        test_pf = seq2pat._get_cython_imp(-1)

        self.assertListEqual([], test_pf.umedi)
        self.assertListEqual([], test_pf.lmedi)
        self.assertListEqual([], test_pf.uavr)
        self.assertListEqual([], test_pf.uavri)
        self.assertListEqual([0], test_pf.num_med)

        one_constraint_result = seq2pat.get_patterns(.001)
        results_file = self.DATA_DIR + "one_constraint_results.txt"
        control_patterns = read_data(results_file)
        sorted_controls = sort_pattern(control_patterns)
        self.assertListEqual(sorted_controls, one_constraint_result)

    def test_seq2pat_batch_diff_constraint(self):
        # Test running seq2pat in batches under constraints
        # Command: ./MPP -file input.txt -thr 0.001 -att input_att1.txt -lg 20 -ug 1000 -ls 800 - us 3700
        # -att input_att2.txt -la 20 -ua 80 -lm 30 -um 70 -out -write BMS_patt.txt, to get results from original implementation
        # These constraints are different from default usage example in original implementation
        # Results from original implementation and seq2pat should be the same

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

    def test_seq2pat_batch_default_no_constraints(self):
        # Test running seq2pat in batches, by default, n_jobs=2, discount_factor=0.2
        # Command: ./MPP -file input.txt -thr 0.01 -out, to get results from original implementation with no constraints
        # Results from original implementation and seq2pat should be the same.

        patterns_file = self.DATA_DIR + "input.txt"
        sequences = read_data(patterns_file)
        seq2pat = Seq2Pat(sequences, max_span=None, batch_size=10000)

        test_patterns = seq2pat.get_patterns(.01)
        results_file = self.DATA_DIR + "no_constraints_results.txt"
        control_patterns = read_data(results_file)
        sorted_results = sort_pattern(control_patterns)
        self.assertListEqual(sorted_results, test_patterns)
        self.assertFalse(test_patterns == read_data(self.DATA_DIR + "default_results.txt"))

    def test_seq2pat_batch_default_no_constraints_large_batch(self):
        # Test running seq2pat in batches, batch_size is larger than data size, n_jobs=2, discount_factor=0.2
        # Command: ./MPP -file input.txt -thr 0.01 -out, to get results from original implementation with no constraints
        # Results from original implementation and seq2pat should be the same.

        patterns_file = self.DATA_DIR + "input.txt"
        sequences = read_data(patterns_file)
        seq2pat = Seq2Pat(sequences, max_span=None, batch_size=100000)

        test_patterns = seq2pat.get_patterns(.01)
        results_file = self.DATA_DIR + "no_constraints_results.txt"
        control_patterns = read_data(results_file)
        sorted_results = sort_pattern(control_patterns)
        self.assertListEqual(sorted_results, test_patterns)
        self.assertFalse(test_patterns == read_data(self.DATA_DIR + "default_results.txt"))

    def test_seq2pat_batch_default_no_constraints_dynamic_batch(self):
        # Test running seq2pat in batches, batch_size is set dynamically, n_jobs=2, discount_factor=0.2
        # Command: ./MPP -file input.txt -thr 0.01 -out, to get results from original implementation with no constraints
        # Results from original implementation and seq2pat should be the same.

        patterns_file = self.DATA_DIR + "input.txt"
        sequences = read_data(patterns_file)
        sequences = sequences * 10
        seq2pat = Seq2Pat(sequences)

        self.assertTrue(len(sequences) > 500000)
        self.assertTrue(seq2pat.batch_size == 10000)
        # test_patterns = seq2pat.get_patterns(0.1)

    def test_seq2pat_batch_n_jobs_all_cpus(self):
        # Test running seq2pat in batches with n_jobs=-1 (all cpus are used)
        # Command: ./MPP -file input.txt -thr 0.01 -out, to get results from original implementation with no constraints
        # Results from original implementation and seq2pat should be the same.

        patterns_file = self.DATA_DIR + "input.txt"
        sequences = read_data(patterns_file)
        seq2pat = Seq2Pat(sequences, max_span=None, batch_size=10000, n_jobs=-1)

        test_patterns = seq2pat.get_patterns(.01)
        results_file = self.DATA_DIR + "no_constraints_results.txt"
        control_patterns = read_data(results_file)
        sorted_results = sort_pattern(control_patterns)
        self.assertListEqual(sorted_results, test_patterns)
        self.assertFalse(test_patterns == read_data(self.DATA_DIR + "default_results.txt"))

    def test_seq2pat_batch_n_jobs_all_cpus_but_one(self):
        # Test running seq2pat in batches with n_jobs=-2 (all cpus but one are used)
        # Command: ./MPP -file input.txt -thr 0.01 -out, to get results from original implementation with no constraints
        # Results from original implementation and seq2pat should be the same.

        patterns_file = self.DATA_DIR + "input.txt"
        sequences = read_data(patterns_file)
        seq2pat = Seq2Pat(sequences, max_span=None, batch_size=10000, n_jobs=-2)

        test_patterns = seq2pat.get_patterns(.01)
        results_file = self.DATA_DIR + "no_constraints_results.txt"
        control_patterns = read_data(results_file)
        sorted_results = sort_pattern(control_patterns)
        self.assertListEqual(sorted_results, test_patterns)
        self.assertFalse(test_patterns == read_data(self.DATA_DIR + "default_results.txt"))

    def test_seq2pat_batch_discount_factor_large(self):
        # Test running seq2pat in batches with a large discount factor
        # Command: ./MPP -file input.txt -thr 0.01 -out, to get results from original implementation with no constraints
        # Results from original implementation and seq2pat should be the same.

        patterns_file = self.DATA_DIR + "input.txt"
        sequences = read_data(patterns_file)
        seq2pat = Seq2Pat(sequences, max_span=None, batch_size=10000, n_jobs=-1, discount_factor=0.8)

        test_patterns = seq2pat.get_patterns(.01)
        results_file = self.DATA_DIR + "no_constraints_results.txt"
        control_patterns = read_data(results_file)
        sorted_results = sort_pattern(control_patterns)
        self.assertListEqual(sorted_results[:14], test_patterns[:14])
        self.assertFalse(sorted_results[14] == test_patterns[14])
        self.assertFalse(test_patterns == read_data(self.DATA_DIR + "default_results.txt"))

    def test_seq2pat_batch_discount_factor_small(self):
        # Test running seq2pat in batches with a small discount factor
        # Command: ./MPP -file input.txt -thr 0.01 -out, to get results from original implementation with no constraints
        # Results from original implementation and seq2pat should be the same.

        patterns_file = self.DATA_DIR + "input.txt"
        sequences = read_data(patterns_file)
        seq2pat = Seq2Pat(sequences, max_span=None, batch_size=10000, n_jobs=-1, discount_factor=0.2)

        test_patterns = seq2pat.get_patterns(.01)
        results_file = self.DATA_DIR + "no_constraints_results.txt"
        control_patterns = read_data(results_file)
        sorted_results = sort_pattern(control_patterns)
        self.assertListEqual(sorted_results, test_patterns)
        self.assertFalse(test_patterns == read_data(self.DATA_DIR + "default_results.txt"))

    def test_seq2pat_batch_integer_min_frequency(self):
        # Test running seq2pat in batches with a small discount factor, min_frequency is an integer
        # Command: ./MPP -file input.txt -thr 0.01 -out, to get results from original implementation with no constraints
        # Results from original implementation and seq2pat should be the same.

        patterns_file = self.DATA_DIR + "input.txt"
        sequences = read_data(patterns_file)
        seq2pat = Seq2Pat(sequences, max_span=None, batch_size=10000, n_jobs=-1, discount_factor=0.2)

        test_patterns = seq2pat.get_patterns(min_frequency=int(len(sequences)*0.01))
        results_file = self.DATA_DIR + "no_constraints_results.txt"
        control_patterns = read_data(results_file)
        sorted_results = sort_pattern(control_patterns)
        self.assertListEqual(sorted_results, test_patterns)
        self.assertFalse(test_patterns == read_data(self.DATA_DIR + "default_results.txt"))


if __name__ == '__main__':
    unittest.main()