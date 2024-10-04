# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0
import collections
import os
import unittest

from sequential.seq2pat import Seq2Pat, Attribute
from sequential.utils import (read_data, get_max_column_size, get_max_value, compare_results, sort_pattern)
from sequential.backend import seq_to_pat as stp


class TestSeq2Pat(unittest.TestCase):
    TEST_DIR = os.path.dirname(os.path.abspath(__file__))
    DATA_DIR = TEST_DIR + os.sep + "data" + os.sep

    def test_example(self):
        # Seq2Pat over 3 sequences
        seq2pat = Seq2Pat(sequences=[["A", "C", "B", "A", "D"],
                                     ["C", "B", "A"],
                                     ["C", "A", "C", "D"]])

        # Patterns
        patterns = seq2pat.get_patterns(min_frequency=2)
        # print("Initial Patterns: ", patterns, "\n")

        # Attribute - I: Price
        price = Attribute(values=[[5, 5, 3, 8, 2],
                                  [1, 3, 3],
                                  [4, 5, 2, 1]])

        # Attribute - II: Timestamp
        timestamp = Attribute(values=[[1, 1, 2, 3, 3],
                                      [3, 8, 9],
                                      [2, 5, 5, 7]])

        # Add Constraint
        avg_constraint = 3 <= price.average() <= 5
        # avg_constraint = 4 <= price.average() <= 4
        seq2pat.add_constraint(avg_constraint)

        # Patterns
        patterns = seq2pat.get_patterns(min_frequency=2)
        # print("Average Constraint:", patterns, "\n")
        self.assertListEqual([['A', 'C', 2], ['A', 'D', 2], ['C', 'A', 'D', 2]],
                             patterns)

        # Remove Constraint
        seq2pat.remove_constraint(avg_constraint)
        patterns = seq2pat.get_patterns(min_frequency=2)
        # print("No Constraint:", patterns, "\n")
        self.assertListEqual([['C', 'A', 3], ['A', 'C', 2], ['A', 'C', 'D', 2], ['A', 'D', 2],
                              ['B', 'A', 2], ['C', 'A', 'D', 2], ['C', 'B', 2], ['C', 'B', 'A', 2],
                              ['C', 'D', 2]], patterns)

    def test_usage_example_average(self):
        # Seq2Pat over 3 sequences
        seq2pat = Seq2Pat(sequences=[["A", "A", "B", "A", "D"],
                                     ["C", "B", "A"],
                                     ["C", "A", "C", "D"]])

        # Create price attributes
        price = Attribute(values=[[5, 5, 3, 8, 2],
                                  [1, 3, 3],
                                  [4, 5, 2, 1]])

        # Create a time attribute
        timestamp = Attribute(values=[[1, 1, 2, 3, 3],
                                      [3, 8, 9],
                                      [2, 5, 5, 7]])

        # Constraint to specify the average price of sequences
        avg_constraint = seq2pat.add_constraint(3 <= price.average() <= 4)

        # Find sequences that occur at least twice within average price range
        patterns = seq2pat.get_patterns(min_frequency=2)

        # Same solution as CMU commandline tool
        self.assertListEqual([['A', 'D', 2]], patterns)

    def test_usage_example_gap(self):
        # Seq2Pat over 3 sequences
        seq2pat = Seq2Pat(sequences=[["A", "A", "B", "A", "D"],
                                     ["C", "B", "A"],
                                     ["C", "A", "C", "D"]])

        # Create price attributes
        price = Attribute(values=[[5, 5, 3, 2, 8],
                                  [1, 3, 3],
                                  [4, 1, 2, 5]])

        # Create a time attribute
        timestamp = Attribute(values=[[1, 1, 2, 3, 3],
                                      [3, 8, 9],
                                      [2, 5, 5, 7]])

        # Constraint to specify the gap between two consecutive prices
        gap_constraint = seq2pat.add_constraint(4 <= price.gap() <= 6)

        # Find sequences that occur at least twice within gap between prices range
        patterns = seq2pat.get_patterns(min_frequency=2)

        # Same solution as CMU commandline tool
        self.assertListEqual([['A', 'D', 2]], patterns)

    def test_usage_example_span(self):
        # Seq2Pat over 3 sequences
        seq2pat = Seq2Pat(sequences=[["A", "A", "B", "A", "D"],
                                     ["C", "B", "A"],
                                     ["C", "A", "C", "D"]])

        # Create price attributes
        price = Attribute(values=[[5, 5, 3, 8, 2],
                                  [1, 3, 3],
                                  [4, 5, 2, 1]])

        # Create a time attribute
        timestamp = Attribute(values=[[1, 1, 2, 3, 3],
                                      [3, 8, 9],
                                      [2, 5, 5, 7]])

        # Constraint to specify the span of time in a pattern. Span is max(attributes) - min(attributes)
        span_constraint = seq2pat.add_constraint(0 <= timestamp.span() <= 2)

        # Find sequences that occur at least twice within span of time range
        patterns = seq2pat.get_patterns(min_frequency=2)

        # Same solution as CMU commandline tool
        self.assertListEqual([['A', 'D', 2], ['B', 'A', 2]], sorted(patterns))

    def test_usage_example_median(self):
        # Seq2Pat over 3 sequences
        seq2pat = Seq2Pat(sequences=[["A", "A", "B", "A", "D"],
                                     ["C", "B", "A"],
                                     ["C", "A", "C", "D"]])

        # Create price attributes
        price = Attribute(values=[[5, 5, 3, 8, 2],
                                  [1, 3, 3],
                                  [4, 5, 2, 1]])

        # Create a time attribute
        timestamp = Attribute(values=[[1, 1, 2, 3, 3],
                                      [3, 8, 9],
                                      [2, 5, 5, 7]])

        # Constraint to specify the median of prices in a pattern
        med_constraint = seq2pat.add_constraint(3 <= price.median() <= 4)

        # Find sequences that occur at least twice within median of prices range
        patterns = seq2pat.get_patterns(min_frequency=2)

        # Same solution as CMU commandline tool
        self.assertListEqual([['A', 'D', 2]], patterns)

    def test_quick_start_int(self):
        # Seq2Pat over 3 sequences
        seq2pat = Seq2Pat(sequences=[[1, 1, 2, 1, 4],
                                     [3, 2, 1],
                                     [3, 1, 3, 4]])

        # Price attribute corresponding to each event
        price = Attribute(values=[[5, 5, 3, 8, 2],
                                  [1, 3, 3],
                                  [4, 5, 2, 1]])

        # Constraint to specify average price of sequences
        seq2pat.add_constraint(-6 <= price.gap())
        # seq2pat.add_constraint(3 <= price.average() <= 6)

        # Find sequences that occur at least twice
        patterns = seq2pat.get_patterns(min_frequency=2)
        # print(patterns)
        self.assertListEqual([[1, 4, 2], [2, 1, 2], [3, 1, 2]], patterns)

    def test_quick_start(self):
        # Seq2Pat over 3 sequences
        seq2pat = Seq2Pat(sequences=[["A", "A", "B", "A", "D"],
                                     ["C", "B", "A"],
                                     ["C", "A", "C", "D"]])

        # Price attribute corresponding to each event
        price = Attribute(values=[[5, 5, 3, 8, 2],
                                  [1, 3, 3],
                                  [4, 5, 2, 1]])

        # Constraint to specify average price of sequences
        seq2pat.add_constraint(-6 <= price.gap() <= -1)
        # seq2pat.add_constraint(3 <= price.average() <= 6)

        # Find sequences that occur at least twice
        patterns = seq2pat.get_patterns(min_frequency=2)
        # print(patterns)
        self.assertListEqual([['A', 'D', 2]], patterns)

    def test_usage_lb_ub(self):
        # List of sequences
        sequences = [[1, 2, 3],
                     [4, 5],
                     [1, 3, 6, 7]]

        # Sequential pattern finder
        seq2pat = Seq2Pat(sequences)

        # Attributes of sequences
        attributes = [[10, 20, 30],
                      [40, 50],
                      [10, 30, 60, 70]]

        att1 = Attribute(attributes)
        att2 = Attribute(attributes)

        # Add constraints on the attributes
        gap_constraint = 0 <= att1.gap() <= 10
        seq2pat.add_constraint(gap_constraint)
        avg_constraint = seq2pat.add_constraint(20 <= att1.average() <= 30)
        median_constraint = seq2pat.add_constraint(-1 <= att1.median() <= 1000)
        span_constraint = seq2pat.add_constraint(0 <= att1.span() <= 900)
        span_constraint2 = seq2pat.add_constraint(-10 <= att2.span() <= 5)
        # seq2pat.__str__()

        self.assertEqual(gap_constraint.lower_bound, 0)
        self.assertEqual(avg_constraint.lower_bound, 20)
        self.assertEqual(median_constraint.lower_bound, -1)
        self.assertEqual(span_constraint.lower_bound, 0)
        self.assertEqual(span_constraint2.lower_bound, -10)
        self.assertEqual(gap_constraint.upper_bound, 10)
        self.assertEqual(avg_constraint.upper_bound, 30)
        self.assertEqual(median_constraint.upper_bound, 1000)
        self.assertEqual(span_constraint.upper_bound, 900)
        self.assertEqual(span_constraint2.upper_bound, 5)

        # Remove constraints
        seq2pat.remove_constraint(gap_constraint)
        seq2pat.remove_constraint(avg_constraint)
        seq2pat.remove_constraint(median_constraint)
        seq2pat.remove_constraint(span_constraint)
        # seq2pat.__str__()

        # Add again
        seq2pat.add_constraint(gap_constraint)
        seq2pat.add_constraint(span_constraint)
        # seq2pat.__str__()

    def test_usage_lb(self):
        # List of sequences
        sequences = [[1, 2, 3],
                     [4, 5],
                     [1, 3, 6, 7]]

        # Sequential pattern finder
        seq2pat = Seq2Pat(sequences)

        # Attributes of sequences
        attributes = [[10, 20, 30],
                      [40, 50],
                      [10, 30, 60, 70]]

        att1 = Attribute(attributes)
        att2 = Attribute(attributes)

        # Add constraints on the attributes
        gap_constraint = 0 <= att1.gap()
        seq2pat.add_constraint(gap_constraint)
        avg_constraint = seq2pat.add_constraint(20 <= att1.average())
        median_constraint = seq2pat.add_constraint(-1 <= att1.median())
        span_constraint = seq2pat.add_constraint(0 <= att1.span())
        span_constraint2 = seq2pat.add_constraint(-10 <= att2.span())
        # seq2pat.__str__()

        self.assertEqual(gap_constraint.lower_bound, 0)
        self.assertEqual(avg_constraint.lower_bound, 20)
        self.assertEqual(median_constraint.lower_bound, -1)
        self.assertEqual(span_constraint.lower_bound, 0)
        self.assertEqual(span_constraint2.lower_bound, -10)

        # Remove constraints
        seq2pat.remove_constraint(gap_constraint)
        seq2pat.remove_constraint(avg_constraint)
        seq2pat.remove_constraint(median_constraint)
        seq2pat.remove_constraint(span_constraint)
        # seq2pat.__str__()

        # Add again
        seq2pat.add_constraint(gap_constraint)
        seq2pat.add_constraint(span_constraint)
        # seq2pat.__str__()

    def test_usage(self):
        # Pattern data
        patterns_file = self.DATA_DIR + "input.txt"
        sequences = read_data(patterns_file)
        # print("Patterns: ", sequences[:5])

        # Attribute data
        attribute_file = self.DATA_DIR + "input_att1.txt"
        attribute_1 = read_data(attribute_file)
        # print("Attribute_1: ", attribute_1[:5])

        # Sequential pattern finder
        seq2pat = Seq2Pat(sequences, max_span=None)

        # Constraints on attribute 1
        att1 = Attribute(attribute_1)

        avg_constraint = seq2pat.add_constraint(5 <= att1.average())
        gap_constraint = seq2pat.add_constraint(att1.gap() <= 10)
        median_constraint = seq2pat.add_constraint(10 <= att1.median() <= 15)
        span_constraint = seq2pat.add_constraint(att1.span() <= 20)

        # Print constraint store
        # seq2pat.__str__()

        seq2pat.get_patterns(min_frequency=100)

    def test_from_mpp(self):
        # Seq2Pat over 3 sequences
        seq2pat = Seq2Pat(sequences=[["A", "A", "B", "A", "D"],
                                     ["C", "B", "A"],
                                     ["C", "A", "C", "D"]])

        # Time attribute corresponding to each event
        time = Attribute(values=[[1, 1, 2, 3, 3],
                                 [3, 8, 9],
                                 [2, 5, 5, 7]])

        # Price attribute corresponding to each event
        price = Attribute(values=[[5, 5, 3, 8, 2],
                                  [1, 3, 3],
                                  [4, 5, 2, 1]])

        # Constraint to specify average price over the sequences
        # seq2pat.add_constraint(3 <= price.average() <= 4)
        # seq2pat.add_constraint(-1 <= price.span() <= -1)

        # Find sequences
        patterns = seq2pat.get_patterns(min_frequency=3)
        # print(patterns)
        self.assertListEqual([], patterns)

    def test_bounds_with_minus_1(self):
        # Seq2Pat over 3 sequences
        seq2pat = Seq2Pat(sequences=[["A", "A", "B", "A", "D"],
                                     ["C", "B", "A"],
                                     ["C", "A", "C", "D"]])

        # Create price attributes
        price = Attribute(values=[[5, 5, 3, 8, 2],
                                  [1, 3, 3],
                                  [4, 5, 2, 1]])

        # Create a time attribute
        timestamp = Attribute(values=[[1, 1, 2, 3, 3],
                                      [3, 8, 9],
                                      [2, 5, 5, 7]])

        # Constraint to specify the gap between two consecutive prices
        gap_constraint = seq2pat.add_constraint(-6 <= price.gap() <= -1)

        # Find sequences that occur at least twice within gap between prices range
        patterns = seq2pat.get_patterns(min_frequency=2)
        # print(patterns)

        # Same solution as CMU commandline tool
        self.assertListEqual([['A', 'D', 2]], patterns)

    def test_min_frequency_as_1_integer(self):
        # Seq2Pat over 3 sequences
        seq2pat = Seq2Pat(sequences=[["A", "A", "B", "A", "D"],
                                     ["C", "B", "A"],
                                     ["C", "A", "C", "D"]])

        # Create price attributes
        price = Attribute(values=[[5, 5, 3, 8, 2],
                                  [1, 3, 3],
                                  [4, 5, 2, 1]])

        # Create a time attribute
        timestamp = Attribute(values=[[1, 1, 2, 3, 3],
                                      [3, 8, 9],
                                      [2, 5, 5, 7]])

        # Find sequences with min_frequency=1
        patterns = seq2pat.get_patterns(min_frequency=1)

        # Same solution as CMU commandline tool
        results = [['A', 'D', 2], ['B', 'A', 2], ['C', 'A', 2], ['A', 'A', 1], ['A', 'A', 'A', 1],
                   ['A', 'A', 'A', 'D', 1], ['A', 'A', 'B', 1], ['A', 'A', 'B', 'A', 1], ['A', 'A', 'B', 'A', 'D', 1],
                   ['A', 'A', 'B', 'D', 1], ['A', 'A', 'D', 1], ['A', 'B', 1], ['A', 'B', 'A', 1],
                   ['A', 'B', 'A', 'D', 1], ['A', 'B', 'D', 1], ['A', 'C', 1], ['A', 'C', 'D', 1], ['B', 'A', 'D', 1],
                   ['B', 'D', 1], ['C', 'A', 'C', 1], ['C', 'A', 'C', 'D', 1], ['C', 'A', 'D', 1], ['C', 'B', 1],
                   ['C', 'B', 'A', 1], ['C', 'C', 1], ['C', 'C', 'D', 1], ['C', 'D', 1]]

        self.assertListEqual(patterns, results)

    def test_min_frequency_as_1dot0_float(self):
        # Seq2Pat over 3 sequences
        seq2pat = Seq2Pat(sequences=[["A", "A", "B", "A", "D"],
                                     ["C", "B", "A"],
                                     ["C", "A", "C", "D"]])

        # Create price attributes
        price = Attribute(values=[[5, 5, 3, 8, 2],
                                  [1, 3, 3],
                                  [4, 5, 2, 1]])

        # Create a time attribute
        timestamp = Attribute(values=[[1, 1, 2, 3, 3],
                                      [3, 8, 9],
                                      [2, 5, 5, 7]])

        # Find sequences with min_frequency=1.0
        patterns = seq2pat.get_patterns(min_frequency=1.0)
        # print(patterns)

        # Same solution as CMU commandline tool
        self.assertListEqual([], patterns)

    def test_string(self):
        # Seq2Pat
        seq2pat = Seq2Pat(sequences=[["A", "C", "B", "C"],
                                     ["D", "A", "E", "B", "W", "C"],
                                     ["W", "W", "C", "A", "A", "B", "S", "C"],
                                     ["D", "A", "C", "B", "A", "C"]])

        # Find sequences
        patterns = seq2pat.get_patterns(min_frequency=4)
        # print(patterns)
        self.assertEqual(4, len(patterns))
        self.assertTrue(['B', 'C', 4] in patterns)
        self.assertTrue(['A', 'C', 4] in patterns)
        self.assertTrue(['A', 'B', 4] in patterns)
        self.assertTrue(['A', 'B', 'C', 4] in patterns)

        self.assertListEqual([['A', 'B', 4], ['A', 'B', 'C', 4],
                              ['A', 'C', 4], ['B', 'C', 4]], patterns)

    def test_string_from_int(self):
        # Seq2Pat
        seq2pat = Seq2Pat(sequences=[[1, 3, 2, 3],
                                     [4, 1, 5, 2, 10, 3],
                                     [10, 10, 3, 1, 1, 2, 9, 3],
                                     [4, 1, 3, 2, 1, 3]])

        # Find sequences
        patterns = seq2pat.get_patterns(min_frequency=4)

        # Same solution as string version
        self.assertListEqual([[1, 2, 4], [1, 2, 3, 4], [1, 3, 4], [2, 3, 4]], patterns)

    def test_operator(self):
        # Attributes of sequences
        attributes = [[10, 20, 30],
                      [40, 50],
                      [10, 30, 60, 70]]

        attribute_1 = Attribute(attributes)

        c1 = 100 <= attribute_1.average() <= 500
        c2 = 200 <= attribute_1.span()
        c3 = attribute_1.span() <= 1456

        self.assertEqual(c1.lower_bound, 100)
        self.assertEqual(c2.lower_bound, 200)
        self.assertEqual(c3.lower_bound, None)
        self.assertEqual(c1.upper_bound, 500)
        self.assertEqual(c2.upper_bound, None)
        self.assertEqual(c3.upper_bound, 1456)

    def test_input(self):
        patterns_file = self.DATA_DIR + "input.txt"
        sequences = read_data(patterns_file)
        self.assertTrue(type(sequences) == list)
        self.assertTrue(len(sequences) == 52619)
        self.assertTrue(len(sequences[0]) == 5)
        # print(sequences[:5])

        attribute_file = self.DATA_DIR + "input_att1.txt"
        attribute_1 = read_data(attribute_file)
        self.assertTrue(type(attribute_1) == list)
        self.assertTrue(len(attribute_1) == 52619)
        self.assertTrue(len(attribute_1[0]) == 5)
        # print(attribute_1[:5])

    def test_input_item_variables(self):
        patterns_file = self.DATA_DIR + "input.txt"
        sequences = read_data(patterns_file)
        m = get_max_column_size(sequences)
        n = len(sequences)
        l = get_max_value(sequences)
        self.assertEqual(161, m)
        self.assertEqual(52619, n)
        self.assertEqual(3340, l)

    def test_invalid_freq(self):
        # Test get_patterns invalid input value error
        # List of sequences
        sequences = [[1, 2, 3],
                     [4, 5],
                     [1, 3, 6, 7]]

        # Sequential pattern finder
        seq2pat = Seq2Pat(sequences)

        with self.assertRaises(ValueError):
            seq2pat.get_patterns(-1)

        with self.assertRaises(ValueError):
            seq2pat.get_patterns(0)

    def test_invalid_patterns(self):
        # Testing invalid sequences on sequential
        sequences = None

        # null input as pattern input
        with self.assertRaises(ValueError):
            # Sequential pattern finder
            seq2pat = Seq2Pat(sequences)

        sequences = [[1, 2, 3],
                     'string',
                     [1, 3, 6, 7]]

        # non-list string input in the middle index of pattern input
        with self.assertRaises(ValueError):
            # Sequential pattern finder
            seq2pat = Seq2Pat(sequences)

        # non-list integer input in the last index of pattern input
        sequences = [[1, 2, 3],
                     [1, 3, 6, 7],
                     1]

        with self.assertRaises(ValueError):
            # Sequential pattern finder
            seq2pat = Seq2Pat(sequences)

        # non-list object input in the first index of pattern input
        patterns = [set(),
                    [1, 2, 3],
                    [1, 3, 6, 7]]

        def test_invalid_patterns(self):
            # Testing invalid sequences on patternfinder
            sequences = None

            # null input as pattern input
            with self.assertRaises(ValueError):
                # Sequential pattern finder
                seq2pat = Seq2Pat(sequences)

            sequences = [[1, 2, 3],
                         'string',
                         [1, 3, 6, 7]]

            # non-list string input in the middle index of pattern input
            with self.assertRaises(ValueError):
                # Sequential pattern finder
                seq2pat = Seq2Pat(sequences)

            # non-list integer input in the last index of pattern input
            sequences = [[1, 2, 3],
                         [1, 3, 6, 7],
                         1]

            with self.assertRaises(ValueError):
                # Sequential pattern finder
                seq2pat = Seq2Pat(sequences)

            # non-list object input in the first index of pattern input
            patterns = [set(),
                        [1, 2, 3],
                        [1, 3, 6, 7]]

        # multiple invalid line in sequences
        with self.assertRaises(ValueError):
            patterns = [set(), "string", 1]
            seq2pat = Seq2Pat(sequences)

    def test_invalid_attributes(self):
        # Testing invalid sequences on sequential

        # null input as attribute input
        with self.assertRaises(ValueError):
            Attribute(None)

        # non-list string input in the middle index of attribute input
        attribute = [[1, 2, 3],
                     'string',
                     [1, 3, 6, 7]]
        with self.assertRaises(ValueError):
            Attribute(attribute)

        # non-list integer input in the last index of attribute input
        attribute = [[1, 2, 3],
                     [1, 3, 6, 7],
                     1]
        with self.assertRaises(ValueError):
            Attribute(attribute)

        # non-list object input in the first index of attribute input
        attribute = [set(),
                     [1, 2, 3],
                     [1, 3, 6, 7]]

        with self.assertRaises(ValueError):
            Attribute(attribute)

        # multiple invalid line in sequences
        attribute = [set(), "string", 1]
        with self.assertRaises(ValueError):
            Attribute(attribute)

    def test_setter(self):
        # Testing cython object setters and getters
        python_seq2pat = stp.PySeq2pat()
        patterns_file = self.DATA_DIR + "input.txt"
        sequences = read_data(patterns_file)
        seq2pat = Seq2Pat(sequences)

        python_seq2pat.lgap = [30]
        python_seq2pat.ugap = [900]
        python_seq2pat.lspn = [77]
        python_seq2pat.uspn = [9, 80]
        python_seq2pat.lavr = [9, 88]
        python_seq2pat.uavr = [7]
        python_seq2pat.lmed = [9, 9, 8]
        python_seq2pat.umed = [99999]
        self.assertListEqual(python_seq2pat.lgap, [30])
        self.assertListEqual(python_seq2pat.ugap, [900])
        self.assertListEqual(python_seq2pat.lspn, [77])
        self.assertListEqual(python_seq2pat.uspn, [9, 80])
        self.assertListEqual(python_seq2pat.lavr, [9, 88])
        self.assertListEqual(python_seq2pat.uavr, [7])
        self.assertListEqual(python_seq2pat.lmed, [9, 9, 8])
        self.assertListEqual(python_seq2pat.umed, [99999])

        python_seq2pat.lgapi = [0]
        python_seq2pat.ugapi = [0]
        python_seq2pat.lspni = [1]
        python_seq2pat.uspni = [1, 0]
        python_seq2pat.lavri = [0, 1]
        python_seq2pat.uavri = [0]
        python_seq2pat.lmedi = [0, 1, 2]
        python_seq2pat.umedi = [2]
        #
        self.assertListEqual(python_seq2pat.lgapi, [0])
        self.assertListEqual(python_seq2pat.ugapi, [0])
        self.assertListEqual(python_seq2pat.lspni, [1])
        self.assertListEqual(python_seq2pat.uspni, [1, 0])
        self.assertListEqual(python_seq2pat.lavri, [0, 1])
        self.assertListEqual(python_seq2pat.uavri, [0])
        self.assertListEqual(python_seq2pat.lmedi, [0, 1, 2])
        self.assertListEqual(python_seq2pat.umedi, [2])

        python_seq2pat.num_minmax = [0, 0, 0]
        python_seq2pat.num_avr = [1, 1, 1]
        python_seq2pat.num_med = [0, 1, 2]
        python_seq2pat.tot_gap = [0, 1, 0]
        python_seq2pat.tot_spn = [2, 2, 2]
        python_seq2pat.tot_avr = [0, 1, 1]

        self.assertListEqual(python_seq2pat.num_minmax, [0, 0, 0])
        self.assertListEqual(python_seq2pat.num_avr, [1, 1, 1])
        self.assertListEqual(python_seq2pat.num_med, [0, 1, 2])
        self.assertListEqual(python_seq2pat.tot_gap, [0, 1, 0])
        self.assertListEqual(python_seq2pat.tot_spn, [2, 2, 2])
        self.assertListEqual(python_seq2pat.tot_avr, [0, 1, 1])

        python_seq2pat.num_att = 3
        python_seq2pat.N = 200
        python_seq2pat.M = 999
        python_seq2pat.L = 89
        python_seq2pat.theta = 89

        self.assertEqual(python_seq2pat.num_att, 3)
        self.assertEqual(python_seq2pat.N, 200)
        self.assertEqual(python_seq2pat.M, 999)
        self.assertEqual(python_seq2pat.L, 89)
        self.assertEqual(python_seq2pat.theta, 89)

    def test_seq2patfinder_default(self):
        # Command:
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
        seq2pat = Seq2Pat(sequences, max_span=None)

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

    def test_input_one_attribute_constraint(self):
        # Command: ./MPP -file input.txt -thr 0.001 -att input_att1.txt -lg 30 -ug 900 -ls 900 -out -write BMS_patt.txt,
        # to get results from original implementation with constraints on only one attribute
        # Results from original implementation and seq2pat should be the same

        # Seq2Pat
        patterns_file = self.DATA_DIR + "input.txt"
        sequences = read_data(patterns_file)
        seq2pat = Seq2Pat(sequences, max_span=None)

        # Load Attributes
        attribute_file = self.DATA_DIR + "input_att1.txt"
        attr1_data = read_data(attribute_file)
        att1 = Attribute(attr1_data)

        cts1 = seq2pat.add_constraint(30 <= att1.gap() <= 900)
        cts2 = seq2pat.add_constraint(900 <= att1.span())

        test_patterns = seq2pat.get_patterns(.001)
        results_file = self.DATA_DIR + "one_constraint_results.txt"
        control_patterns = read_data(results_file)
        sorted_controls = sort_pattern(control_patterns)
        self.assertListEqual(sorted_controls, test_patterns)
        self.assertFalse(test_patterns == read_data(self.DATA_DIR + "default_results.txt"))

    def test_input_no_constraint(self):
        # Command: ./MPP -file input.txt -thr 0.01 -out, to get results from original implementation with no constraints
        # Results from original implementation and seq2pat should be the same

        patterns_file = self.DATA_DIR + "input.txt"
        sequences = read_data(patterns_file)
        seq2pat = Seq2Pat(sequences, max_span=None)

        test_patterns = seq2pat.get_patterns(.01)
        results_file = self.DATA_DIR + "no_constraints_results.txt"
        control_patterns = read_data(results_file)
        sorted_results = sort_pattern(control_patterns)
        self.assertListEqual(sorted_results, test_patterns)
        self.assertFalse(test_patterns == read_data(self.DATA_DIR + "default_results.txt"))

    def test_input_diff_constraint(self):
        # Command: ./MPP -file input.txt -thr 0.001 -att input_att1.txt -lg 20 -ug 1000 -ls 800 - us 3700
        # -att input_att2.txt -la 20 -ua 80 -lm 30 -um 70 -out -write BMS_patt.txt, to get results from original implementation
        # These constraints are different from default usage example in original implementation
        # Results from original implementation and seq2pat should be the same

        # Seq2Pat
        patterns_file = self.DATA_DIR + "input.txt"
        sequences = read_data(patterns_file)
        seq2pat = Seq2Pat(sequences, max_span=None)

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

    def test_input_no_lower_constraint(self):
        # Command: ./MPP -file input.txt -thr 0.001 -att input_att1.txt -ug 900 - us 3600 -att input_att2.txt
        # -ua 70 -um 60 -out -write BMS_patt.txt, to get results from original implementation
        # Results from original implementation and seq2pat should be the same

        # Seq2Pat
        patterns_file = self.DATA_DIR + "input.txt"
        sequences = read_data(patterns_file)
        seq2pat = Seq2Pat(sequences, max_span=None)

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

    def test_input_no_upper_constraint(self):
        # Command: ./MPP -file input.txt -thr 0.001 -att input_att1.txt -lg 900 -ls 3600 -att input_att2.txt
        # -la 70 -lm 60 -out -write BMS_patt.txt, to get results from original implementation
        # Results from original implementation and seq2pat should be the same

        # Seq2Pat
        patterns_file = self.DATA_DIR + "input.txt"
        sequences = read_data(patterns_file)
        seq2pat = Seq2Pat(sequences, max_span=None)

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

    def test_compare_results(self):
        a = [1, 2]
        b = [4, 5]
        c = [6, 7, 8]

        list_a = [a, b, c]
        list_b = [c]
        a_b, b_a = compare_results(list_a, list_b)
        self.assertListEqual([a, b], a_b)
        self.assertEqual([], b_a)

    def test_attribute_mapping(self):
        # Test to verify that attributes that will be checked for constraint satisfaction
        # during mining are a one-to-one mapping between itself and items
        sequences = [[1, 2, 3],
                     [4, 5],
                     [1, 3, 6, 7]]
        # Sequential pattern finder
        seq2pat = Seq2Pat(sequences)

        # Number of values in row 1 in attribute is larger than the number of event in sequence one of sequences
        attribute = [[1, 2, 3, 5],
                     [4, 5],
                     [1, 3, 6, 7]]

        att1 = Attribute(attribute)
        with self.assertRaises(ValueError):
            seq2pat.add_constraint(0 <= att1.gap() <= 10)

        # Number of values in row 2 in attribute is less than the number of event in sequence one of sequences
        attribute = [[1, 2, 3, 5],
                     [4],
                     [1, 3, 6, 7]]
        att1 = Attribute(attribute)
        with self.assertRaises(ValueError):
            seq2pat.add_constraint(0 <= att1.gap() <= 10)

    def test_gap_inequality(self):
        # List of sequences
        sequences = [[11, 12, 13]]

        # Sequential pattern finder
        seq2pat = Seq2Pat(sequences)

        unconstrained_result = seq2pat.get_patterns(1)

        self.assertListEqual([[11, 12, 1],
                              [11, 12, 13, 1],
                              [11, 13, 1],
                              [12, 13, 1]], unconstrained_result)

        # Attributes of sequences min gap is 10 between any two events,
        # max gap is between event 11 and 13 with a value of 20
        attributes = [[10, 20, 30]]

        att1 = Attribute(attributes)

        # Should be empty upper and lower bounds exceed gaps between any two events
        gap_constraint = seq2pat.add_constraint(11 <= att1.gap() <= 19)
        self.assertListEqual([], seq2pat.get_patterns(1))

        seq2pat.remove_constraint(11 <= att1.gap() <= 19)

        # Should include any sequence with gaps between any two events with a value equal to or greater than 10
        # and equal to or less than 19
        gap_constraint = seq2pat.add_constraint(10 <= att1.gap() <= 11)

        self.assertListEqual([[11, 12, 1],
                              [11, 12, 13, 1],
                              [12, 13, 1]], seq2pat.get_patterns(1))

        seq2pat.remove_constraint(10 <= att1.gap() <= 11)

        # Should include any sequence with gaps between any two events with a value equal to or greater than 11
        # and equal to or less than 20
        gap_constraint = seq2pat.add_constraint(11 <= att1.gap() <= 20)

        self.assertListEqual([[11, 13, 1]], seq2pat.get_patterns(1))

        seq2pat.remove_constraint(11 <= att1.gap() <= 20)

        # Equivalent to unconstrained call to get pattern since values of att1 fall between bounds
        seq2pat.add_constraint(10 <= att1.gap() <= 20)

        self.assertListEqual([[11, 12, 1],
                              [11, 12, 13, 1],
                              [11, 13, 1],
                              [12, 13, 1]], seq2pat.get_patterns(1))

    def test_span_inequality(self):
        # List of sequences
        sequences = [[11, 12, 13]]

        # Sequential pattern finder
        seq2pat = Seq2Pat(sequences)

        unconstrained_result = seq2pat.get_patterns(1)

        self.assertListEqual([[11, 12, 1],
                              [11, 12, 13, 1],
                              [11, 13, 1],
                              [12, 13, 1]], unconstrained_result)

        # Attributes of sequences min span is 10 between any two events,
        # max span is between event 11 and 13 with a value of 20
        attributes = [[10, 20, 30]]

        att1 = Attribute(attributes)

        # Should be empty upper and lower bounds exceed span between any two events
        span_constraint = seq2pat.add_constraint(11 <= att1.span() <= 19)

        self.assertListEqual([], seq2pat.get_patterns(1))

        seq2pat.remove_constraint(11 <= att1.span() <= 19)

        # Should include any sequence with span between any two events with a value equal to or greater than 10
        # and equal to or less than 19
        span_constraint = seq2pat.add_constraint(10 <= att1.span() <= 19)

        self.assertListEqual([[11, 12, 1],
                              [12, 13, 1]], seq2pat.get_patterns(1))

        seq2pat.remove_constraint(10 <= att1.span() <= 11)

        # Should include any sequence with span between any two events with a value equal to or greater than 11
        # and equal to or less than 20
        span_constraint = seq2pat.add_constraint(11 <= att1.span() <= 20)

        self.assertListEqual([[11, 12, 13, 1],
                              [11, 13, 1]], seq2pat.get_patterns(1))

        seq2pat.remove_constraint(11 <= att1.span() <= 20)

        # Equivalent to unconstrained span to get pattern since values of att1 fall between bounds
        span_constraint = seq2pat.add_constraint(10 <= att1.span() <= 20)

        self.assertListEqual([[11, 12, 1],
                              [11, 12, 13, 1],
                              [11, 13, 1],
                              [12, 13, 1]], seq2pat.get_patterns(1))

    def test_average_inequality(self):
        # List of sequences
        sequences = [[11, 12, 13]]

        # Sequential pattern finder
        seq2pat = Seq2Pat(sequences)

        unconstrained_result = seq2pat.get_patterns(1)

        self.assertListEqual([[11, 12, 1],
                              [11, 12, 13, 1],
                              [11, 13, 1],
                              [12, 13, 1]], unconstrained_result)

        # Attributes of sequences min average is 15 for sequence [11, 12],
        # max average is 25 for sequence [12, 13]
        attributes = [[10, 20, 30]]

        att1 = Attribute(attributes)
        # Should be empty upper and lower bounds exceed average between any two events
        gap_constraint = seq2pat.add_constraint(16 <= att1.average() <= 19)
        self.assertListEqual([], seq2pat.get_patterns(1))

        seq2pat.remove_constraint(16 <= att1.average() <= 24)

        # Should include any sequence with average between any two events with a value equal to or greater than 15
        # and equal to or less than 19
        gap_constraint = seq2pat.add_constraint(15 <= att1.average() <= 19)

        self.assertListEqual([[11, 12, 1]], seq2pat.get_patterns(1))

        seq2pat.remove_constraint(15 <= att1.average() <= 19)

        # Should include any sequence with average between any two events with a value equal to or greater than 16
        # and equal to or less than 20
        seq2pat.add_constraint(16 <= att1.average() <= 20)

        self.assertListEqual([[11, 12, 13, 1],
                              [11, 13, 1]], seq2pat.get_patterns(1))

        seq2pat.remove_constraint(16 <= att1.average() <= 20)

        # Equivalent to unconstrained span to get pattern since values of att1 fall between bounds
        seq2pat.add_constraint(15 <= att1.average() <= 25)

        self.assertListEqual([[11, 12, 1],
                              [11, 12, 13, 1],
                              [11, 13, 1],
                              [12, 13, 1]], seq2pat.get_patterns(1))

    def test_median_inequality(self):
        # List of sequences
        sequences = [[11, 12, 13]]

        # Sequential pattern finder
        seq2pat = Seq2Pat(sequences)

        unconstrained_result = seq2pat.get_patterns(1)

        self.assertListEqual([[11, 12, 1],
                              [11, 12, 13, 1],
                              [11, 13, 1],
                              [12, 13, 1]], unconstrained_result)

        # Attributes of sequences min median is 15 for sequence [11, 12],
        # max median is 25 for sequence [12, 13]
        attributes = [[10, 20, 30]]

        att1 = Attribute(attributes)

        # Should be empty upper and lower bounds exceed median between any two events
        gap_constraint = seq2pat.add_constraint(16 <= att1.median() <= 19)
        self.assertListEqual([], seq2pat.get_patterns(1))

        seq2pat.remove_constraint(16 <= att1.median() <= 19)

        # Should include any sequence with median between any two events with a value equal to or greater than 15
        # and equal to or less than 19
        gap_constraint = seq2pat.add_constraint(15 <= att1.median() <= 19)

        self.assertListEqual([[11, 12, 1]], seq2pat.get_patterns(1))

        seq2pat.remove_constraint(15 <= att1.median() <= 19)

        # Should include any sequence with median between any two events with a value equal to or greater than 16
        # and equal to or less than 20
        seq2pat.add_constraint(16 <= att1.median() <= 20)

        self.assertListEqual([[11, 12, 13, 1],
                              [11, 13, 1]], seq2pat.get_patterns(1))

        seq2pat.remove_constraint(16 <= att1.median() <= 20)

        # Equivalent to unconstrained span to get pattern since values of att1 fall between bounds
        seq2pat.add_constraint(15 <= att1.median() <= 25)

        self.assertListEqual([[11, 12, 1],
                              [11, 12, 13, 1],
                              [11, 13, 1],
                              [12, 13, 1]], seq2pat.get_patterns(1))

    def test_simultaneaous_mining(self):
        # List of sequences
        sequences = [[11, 12, 13]]

        # Sequential pattern finder
        seq2pat = Seq2Pat(sequences)
        seq2pat2 = Seq2Pat(sequences)
        unconstrained_result = seq2pat.get_patterns(1)
        unconstrained_result2 = seq2pat2.get_patterns(1)
        self.assertListEqual(unconstrained_result, unconstrained_result2)
        self.assertListEqual([[11, 12, 1],
                              [11, 12, 13, 1],
                              [11, 13, 1],
                              [12, 13, 1]], unconstrained_result)

    def test_min_frequence_negative(self):
        # Seq2Pat over 3 sequences
        seq2pat = Seq2Pat(sequences=[[1, 1, 2, 1, 4],
                                     [3, 2, 1],
                                     [3, 1, 3, 4]])

        # Price attribute corresponding to each event
        price = Attribute(values=[[5, 5, 3, 8, 2],
                                  [1, 3, 3],
                                  [4, 5, 2, 1]])

        with self.assertRaises(ValueError):
            patterns = seq2pat.get_patterns(min_frequency=-1)

    def test_min_frequence_zero_int(self):
        # Seq2Pat over 3 sequences
        seq2pat = Seq2Pat(sequences=[[1, 1, 2, 1, 4],
                                     [3, 2, 1],
                                     [3, 1, 3, 4]])

        # Find sequences that occur at least twice
        with self.assertRaises(ValueError):
            patterns = seq2pat.get_patterns(min_frequency=0)

    def test_min_frequence_zero_float(self):
        # Seq2Pat over 3 sequences
        seq2pat = Seq2Pat(sequences=[[1, 1, 2, 1, 4],
                                     [3, 2, 1],
                                     [3, 1, 3, 4]])

        # Find sequences that occur at least twice
        with self.assertRaises(ValueError):
            patterns = seq2pat.get_patterns(min_frequency=0.0)

    def test_min_frequence_float_large(self):
        # Seq2Pat over 3 sequences
        seq2pat = Seq2Pat(sequences=[[1, 1, 2, 1, 4],
                                     [3, 2, 1],
                                     [3, 1, 3, 4]])

        # Price attribute corresponding to each event
        price = Attribute(values=[[5, 5, 3, 8, 2],
                                  [1, 3, 3],
                                  [4, 5, 2, 1]])

        # Constraint to specify average price of sequences
        seq2pat.add_constraint(-6 <= price.gap())

        # Find sequences that occur at least twice
        with self.assertRaises(ValueError):
            patterns = seq2pat.get_patterns(min_frequency=2.5)

    def test_sequence_with_empty_list(self):
        # List of sequences
        sequences = [[11, 12, 13], []]

        with self.assertRaises(ValueError):
            seq2pat = Seq2Pat(sequences)

        # List of attributes
        values = [[11, 12, 13], []]
        with self.assertRaises(ValueError):
            price = Attribute(values)

    def test_min_frequence_float_one_row(self):
        # List of sequences
        sequences = [[11, 12, 13]]
        min_frequency = 0.9

        # Sequential pattern finder
        seq2pat = Seq2Pat(sequences)

        with self.assertRaises(ValueError):
            patterns = seq2pat.get_patterns(min_frequency=min_frequency)

        min_frequency = 1.0

        self.assertListEqual([[11, 12, 1],
                              [11, 12, 13, 1],
                              [11, 13, 1],
                              [12, 13, 1]], seq2pat.get_patterns(min_frequency=min_frequency))

    def test_min_frequence_float_theta_ge_one(self):
        # List of sequences
        sequences = [[11, 12, 13], [11, 12, 13, 14]]
        min_frequency = 0.9

        # Sequential pattern finder
        seq2pat = Seq2Pat(sequences)

        unconstrained_result = seq2pat.get_patterns(min_frequency=min_frequency)

        self.assertListEqual([[11, 12, 2], [11, 12, 13, 2], [11, 13, 2], [12, 13, 2], [11, 12, 13, 14, 1],
                              [11, 12, 14, 1], [11, 13, 14, 1], [11, 14, 1], [12, 13, 14, 1], [12, 14, 1],
                              [13, 14, 1]], unconstrained_result)

        # Attributes of sequences min gap is 10 between any two events,
        attributes = [[10, 20, 30], [10, 20, 30, 40]]

        att1 = Attribute(attributes)

        # Should include any sequence with gaps between any two events with a value equal to or greater than 10
        # and equal to or less than 11
        gap_constraint = seq2pat.add_constraint(10 <= att1.gap() <= 11)
        self.assertListEqual([[11, 12, 2], [11, 12, 13, 2], [12, 13, 2], [11, 12, 13, 14, 1],
                              [12, 13, 14, 1], [13, 14, 1]], seq2pat.get_patterns(min_frequency=min_frequency))

    def test_min_frequence_float_theta_le_one(self):
        # List of sequences
        sequences = [[11, 12, 13], [11, 12, 13, 14]]
        min_frequence = 0.4

        # Sequential pattern finder
        seq2pat = Seq2Pat(sequences)

        with self.assertRaises(ValueError):
            patterns = seq2pat.get_patterns(min_frequency=min_frequence)

    def test_num_rows_ge_one(self):
        # List of sequences
        sequences = []
        min_frequency = 1

        with self.assertRaises(ValueError):
            seq2pat = Seq2Pat(sequences)

        seq2pat = Seq2Pat(sequences=[[11, 12, 13]])

        # In case num_rows becomes 0.
        seq2pat._num_rows = 0
        with self.assertRaises(ValueError):
            patterns = seq2pat.get_patterns(min_frequency=min_frequency)

    def test_repeated_calls_seq2pat(self):
        # List of sequences
        sequences = [[11, 12, 13], [11, 12, 13, 14]]

        # Sequential pattern finder
        seq2pat = Seq2Pat(sequences)

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

    def test_repeated_calls_seq2pat_add_remove_ct(self):
        # List of sequences
        sequences = [[11, 12, 13]]

        # Sequential pattern finder
        seq2pat = Seq2Pat(sequences)

        unconstrained_result = seq2pat.get_patterns(1)

        self.assertListEqual([[11, 12, 1],
                              [11, 12, 13, 1],
                              [11, 13, 1],
                              [12, 13, 1]], unconstrained_result)

        # Attributes of sequences min average is 15 for sequence [11, 12],
        # max average is 25 for sequence [12, 13]
        attributes = [[10, 20, 30]]

        att1 = Attribute(attributes)

        # Should include any sequence with median between any two events with a value equal to or greater than 15
        # and equal to or less than 19
        med_constraint = seq2pat.add_constraint(15 <= att1.median() <= 19)
        gap_constraint = seq2pat.add_constraint(5 <= att1.average() <= 15)

        self.assertListEqual([[11, 12, 1]], seq2pat.get_patterns(1))

        seq2pat.remove_constraint(med_constraint)
        seq2pat.remove_constraint(gap_constraint)

        self.assertListEqual([[11, 12, 1],
                              [11, 12, 13, 1],
                              [11, 13, 1],
                              [12, 13, 1]], seq2pat.get_patterns(1))

    def test_max_span(self):
        # List of sequences
        sequences = [[11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23]]

        # Sequential pattern finder having the default maximum span constraint on item index
        seq2pat = Seq2Pat(sequences)

        default_result = seq2pat.get_patterns(1)
        self.assertEqual(len(default_result), 2546)

    def test_max_span_none(self):
        # List of sequences
        sequences = [[11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23]]

        # Sequential pattern finder with no default maximum span constraint on item index
        seq2pat = Seq2Pat(sequences, max_span=None)

        unconstrained_result = seq2pat.get_patterns(1)
        self.assertEqual(len(unconstrained_result), 8178)

    def test_max_span_customize(self):
        # List of sequences
        sequences = [[11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30]]
        # print(sequences)

        # Sequential pattern finder having the default maximum span constraint on item index, 13 items
        seq2pat = Seq2Pat(sequences, max_span=13)

        result = seq2pat.get_patterns(1)
        self.assertEqual(len(result), 36843)
        # maximum length in result is 13 items plus the frequency
        self.assertEqual(max(list(map(len, result))), 14)

    def test_sequence_contain_zeros(self):
        sequences = [[1, 0], [0, 1]]

        with self.assertRaises(ValueError):
            seq2pat = Seq2Pat(sequences)


if __name__ == '__main__':
    unittest.main()
