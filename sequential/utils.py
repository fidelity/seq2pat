# -*- coding: utf-8 -*-
# SPDX-License-Identifier: GPL-2.0

from typing import Union, NoReturn, List, Tuple, Dict
import statistics
import pandas as pd
import numpy as np

import sequential.seq2pat as sp

Num = Union[int, float]


class Constants:
    unique_pos = 'unique_positive'
    unique_neg = 'unique_negative'
    intersection = 'intersection'
    union = 'union'
    all_operations = 'all'


def check_true(expression: bool, exception: Exception) -> NoReturn:
    """
    Checks that given expression is true, otherwise raises the given exception.
    """
    if not expression:
        raise exception


def check_false(expression: bool, exception: Exception) -> NoReturn:
    """
        Checks that given expression is false, otherwise raises the given exception.
        """
    if expression:
        raise exception


def read_data(source: str, is_scientific: bool = False) -> List[list]:
    """
    Utility function to read in numeric data from files
    :param source: file path of file to be to be read in
    :param is_scientific: flag to indicate if input file contains values in scientific notation
    :return: a list of list containing values in source
    """
    # Read all rows at once
    with open(source, 'r') as input_file:
        all_rows = input_file.read().splitlines()

    # Automatically detect input type
    if all_rows[0].split()[0].isnumeric() or is_scientific:
        # For each row, split into list and convert to integer
        return [(list(map(float, row.split()))) for row in all_rows]

    # For each row, split into list and convert to string
    return [(list(map(str, row.split()))) for row in all_rows]


def string_to_int(mapping: map, items: List[List[int]]) -> List[list]:
    """
    Utility function to transform string input to int input to be used by sequential library
    :param mapping: map[str, int]
    :param items: a list of ints or a list of ints
    :return: a list of strings where each string is replaced by an integer 'id'
    """
    return [[mapping[i] for i in item] for item in items]


def int_to_string(mapping: map, results: List[List[int]]) -> List[list]:
    """
    Utility function to transform sequential pattern results into original string pattern while retaining the number of
    times each pattern was found
    :param mapping: map[int, str]
    :param results: the output of sequential library
    :return:  list of list in the form [str, str, ... int] where the strings represent a pattern and the int represents
    the number of time the pattern was found
    """
    return [[mapping[item[i]] if i < (len(item) - 1) else item[i] for i in range(len(item))] for item in results]


def get_max_column_size(items: List[List[int]]) -> int:
    """
    Finds and returns the longest row
    :param items: a list of list of ints
    :return: length of the longest row
    """
    return max(list(map(len, items)))


def check_sequence_feature_same_length(items: List[List[int]], attribute: List[List[int]]) -> bool:
    """
    Verifies attributes added to sequential that events in sequences in map one to one for values in attributes
    ie for each row len(items[i] == len(attribute[i])
    :param items: a list of sequences consisting of events
    :param attribute: a list of integer attributes
    :return: true if attributes satisfies requirements false otherwise
    """
    return list(map(len, items)) == list(map(len, attribute))


def check_attributes_int(attribute: List[List[int]]) -> bool:
    """
    Verifies attributes added to sequential are integer values
    :param attribute: a list of integer attributes
    :return: true if attributes satisfies requirements false otherwise
    """
    return all(all(isinstance(a, int) for a in seq) for seq in attribute)


def get_max_value(items: List[List[int]]) -> int:
    """
    Finds and returns maximum value in items
    :param items: a list of list of ints
    :return: max value in items
    """
    return max(list(map(max, items)))


def get_min_value(items: List[List[int]]) -> int:
    """
    Finds and returns minimun value in items
    :param items: a list of list of ints
    :return: max value in items
    """
    return min(list(map(min, items)))


def attr_min(attrs: List[List[int]]) -> list:
    """
    For each attribute: List[int]  in attributes: List finds the minimum value respectively
    :param attrs: A list of list of ints representing attributes
    :return: list where the value of index i is the minimum value for attribute i
    """
    return [min(list(map(min, att))) for att in attrs]


def attr_max(attrs: List[List[int]]) -> list:
    """
    For each attribute: List[int]  in attributes: List finds the maximum value respectively
    :param attrs: A list of list of ints representing attributes
    :return: list where the value of index i is the maximum value for attribute i
    """
    return [max(list(map(max, att))) for att in attrs]


def item_map(items: List[List[str]]) -> (dict, dict):
    """
    Creates a one to one mapping 'str_to_int' to translate list of list of string to list of list of int and another
    mapping 'int_to_str' to translate a list of list converted with 'str_to_int' back to its original
    string representation.
    :param items: List of list of strings
    :return: a maping from string to ints and the reverse mapping from int to string
    """
    # list[list[events]] -> set[events] Unpack all the events in items into a single list and remove duplicates
    # Fix the order of items for creating a deterministic item-ID map
    flat_set = sorted(set([item for sublist in items for item in sublist]))
    # map each event to a unique int ID
    str_to_int = dict([(y, x) for x, y in enumerate(flat_set, start=1)])
    # reverse dictionary where each int ID is mapped to its string representation
    int_to_string = dict([(value, key) for key, value in str_to_int.items()])

    return str_to_int, int_to_string


def compare_results(a: List[list], b: List[list]) -> (List[list], List[list]):
    """
    Compare results from sequential
    :param a: The result from calling sequential
    :param b: The result from calling sequential
    :return: Patterns found in a but not in b and sequences found in b but not in a
    """
    a_filtered = [[items[i] for i in range(len(items)) if i < (len(items) - 1)] for items in a]
    b_filtered = [[items[i] for i in range(len(items)) if i < (len(items) - 1)] for items in b]
    a_result = [item for item in a if item[:-1] not in b_filtered]
    b_result = [item for item in b if item[:-1] not in a_filtered]

    return a_result, b_result


def sort_pattern(patterns: List[list]) -> List[list]:
    """
    Sort sequential results
    :param patterns: The result from calling sequential
    :return: Patterns in descending order by frequency
    """
    # Fix the order of patterns without frequency
    patterns = sorted(patterns, key=lambda x: x[:-1])

    # Return the patterns in descending order by frequency
    return sorted(patterns, key=lambda x: x[-1], reverse=True)


def write_items(file_name: str, items: List[list]) -> NoReturn:
    """
    Simple utility function to write items, attributes, results, or any List[list] to file,
    optimized for very large inputs
    :param file_name: file name as a string should include format as no default is assumed
    :param items: A list of lists of any type
    """
    open_file = open(file_name, 'w')
    open_file.writelines([" ".join([(str(item[i])) if i < (len(item) - 1) else str(item[i]) + "\n"
                                    for i in range(len(item))]) for item in items])
    open_file.close()


def calc_average(result: List[list]) -> list:
    patterns = [row[:-1] for row in result]
    temp = list(map(statistics.mean, patterns))
    return temp


def calc_median(result: List[list]) -> list:
    patterns = [row[:-1] for row in result]
    temp = list(map(statistics.median, patterns))
    return temp


def calc_span(result: List[list]) -> list:
    patterns = [row[:-1] for row in result]
    return []


def drop_frequency(result: List[list]) -> list:
    return list(map(lambda x: x[:-1], result))


def is_subsequence(list1: list, list2: list) -> bool:
    """
    Check if list1 is a subsequence of list2.

    """
    len_list1 = len(list1)
    len_list2 = len(list2)
    index_list1 = 0
    index_list2 = 0

    # Traverse both list1 and list2
    while index_list1 < len_list1 and index_list2 < len_list2:
        # Compare current element of list2 with list1
        if list1[index_list1] == list2[index_list2]:
            # If matched, then move to next element in list1
            index_list1 = index_list1 + 1
        index_list2 = index_list2 + 1
    return index_list1 == len_list1


def is_subsequence_in_rolling(pattern: list, seq: list, seq_attr_ind: int,
                              rolling_window_size: int, constraints: Union[list, None]) -> bool:
    """
     Search the given pattern in a rolling_window of sequence

    """
    res = False

    if len(seq) <= rolling_window_size:
        res = subsequence_identifier(pattern, seq, seq_attr_ind, 0, rolling_window_size, constraints)

    else:
        num_iters = len(seq) - rolling_window_size
        for i in range(num_iters + 1):
            if subsequence_identifier(pattern, seq[i:i + rolling_window_size], seq_attr_ind, i, rolling_window_size,
                                      constraints):
                res = True
                break
    return res


def subsequence_identifier(pattern: list, seq: list, seq_attr_ind: int, seq_attr_start: int, rolling_window_size: int,
                           constraints: Union[list, None]) -> bool:
    """
    Identify if a pattern is in a given sequence, subject to the optional seq2pat._Constraint type of constraints.

    """
    res = False

    if not is_subsequence(pattern, seq):
        # if pattern is not a subsequence of seq, return False
        return res
    else:
        if not constraints:
            # if pattern is a subsequence and there is no constraint, return True
            return True
        else:
            res = meet_constraints_in_rolling(pattern, seq, seq_attr_ind, seq_attr_start, rolling_window_size,
                                              constraints)

    return res


def meet_constraints_in_rolling(pattern: list, sequence: list, seq_attr_ind: int, window_start_ind: int,
                                rolling_window_size: int, constraints: Union[list, None]) -> bool:
    """
    Check if a pattern is in an individual sequence of items, subject to defined constraints.

    Parameters
    ----------
    pattern: list
        A pattern that is going to be checked in the sequence.
    sequence: list
        A sequence of items within which a pattern is searched.
    seq_attr_ind: int
        The index of this sequence in the list of sequences, and also the index of attributes.
    window_start_ind: int
        The index where a rolling window starts.
    rolling_window_size: int
        The rolling window along a sequence within which patterns are detected.
    constraints: Union[list, None]
        A list of constraints

    Returns
    -------
    A boolean result to return if all constraints are met.

    """

    # Get all matched subsequences and their index
    _, item_subsequences_indices = get_matched_subsequences(sequence, pattern)

    meet_all_constraints = False
    for sub_ind, s in enumerate(item_subsequences_indices):

        # Check constraints
        res = [True]
        for constraint in constraints:
            # Get attributes
            attrs = constraint.attribute.values[seq_attr_ind]
            attrs = attrs[window_start_ind:window_start_ind + rolling_window_size]

            # Get subsequences of attributes
            attr_subsequence = [attrs[i] for i in s]

            if isinstance(constraint, sp._Constraint.Average):
                attr_info = get_average_one_seq(attr_subsequence)
                res.append(constraint.check_satisfaction(attr_info))

            if isinstance(constraint, sp._Constraint.Median):
                attr_info = get_median_one_seq(attr_subsequence)
                res.append(constraint.check_satisfaction(attr_info))

            if isinstance(constraint, sp._Constraint.Span):
                attr_info = get_span_one_seq(attr_subsequence)
                res.append(constraint.check_satisfaction(attr_info))

            if isinstance(constraint, sp._Constraint.Gap):
                attr_info = get_gap_one_seq(attr_subsequence)
                res.append(constraint.check_satisfaction(attr_info))

        if all(res):
            meet_all_constraints = True
            break

    return meet_all_constraints


def get_matched_subsequences(seq: list, pattern: list) -> Tuple[list, list]:
    """
    Find all possible subsequences of a sequence in a recursive way.
    For every element in the list, there are two choices, either to include it in the subsequence or not include it.
    Apply this for every element in the list, find the subsequences for the two cases separately.

    """
    res_seq = []
    res_ind = []
    indices = list(range(len(seq)))

    def get_subsequence(subsequence, output, ind_subsequence, ind_output):
        # Base Case
        # if the input is empty, append the output list
        if len(subsequence) == 0:
            if output == pattern:
                res_seq.append(output)
                res_ind.append(ind_output)
            return

        # output is passed with including the
        # 1st element of input list
        get_subsequence(subsequence[1:], output + [subsequence[0]],
                        ind_subsequence[1:], ind_output + [ind_subsequence[0]])

        # output is passed without including the
        # 1st element of input list
        get_subsequence(subsequence[1:], output,
                        ind_subsequence[1:], ind_output)

    get_subsequence(seq, [], indices, [])

    return res_seq, res_ind


def get_one_hot_encodings(items: List[list], patterns: List[list], constraints: Union[list, None] = None,
                          rolling_window_size: int = 10, drop_pattern_frequency=True) -> pd.DataFrame:
    """
    Create a data frame having one-hot encoding of sequences.

    Parameters
    ----------
    items: List[list]
        A list of sequences of items.
    patterns: List[list]
        A list of interested patterns, which defines the encoding space.
    constraints: Union[list, None]
        The constraints enforced in the creation of encoding
    rolling_window_size: int
        The rolling window along a sequence within which patterns are detected. It controls the length of
        sequence subject to the pattern detection and improve the performance in terms of runtime
        (rolling_window_size=10 by default).
    drop_pattern_frequency: bool
        Drop the frequency appended in the end of each input pattern, drop_pattern_frequency=True by default.

    Returns
    -------
    A data frame having one-hot encoding of sequences using the given patterns. The patterns are searched within a
    rolling window along the sequence by default (rolling_window_size=10 by default).

    """

    # Drop the frequency appended to the patterns by default
    if drop_pattern_frequency:
        patterns = drop_frequency(patterns)

    else:
        if isinstance(items[0][0], str):
            check_true(not isinstance(patterns[0][-1], int),
                       ValueError("Patterns should not contain integers! "
                                  "Check if the frequency is appended to the end of given patterns."))

    df = pd.DataFrame()
    df['sequence'] = items
    df['seq_ind'] = list(range(len(items)))

    for i, pattern in enumerate(patterns):
        # For each pattern, create encoding for all sequences
        df['feat' + str(i)] = df.apply(lambda row: is_subsequence_in_rolling(pattern, row['sequence'], row['seq_ind'],
                                                                             rolling_window_size, constraints), axis=1)
        # Cast bool type value to int
        df['feat' + str(i)] = df['feat' + str(i)].astype(int)

    df.drop(columns=['seq_ind'], inplace=True)

    return df


def run_pattern_mining(items: List[list], min_frequency: Num, constraints: Union[list, None] = None) -> List[list]:
    """
    Run pattern mining with constraints.

    Parameters
    ----------
    items: List[list]
        A list of sequences of items.
    min_frequency: Num
       If int, represents the minimum number of sequences (rows) a pattern should occur.
       If float, should be (0.0, 1.0] and represents
       the minimum percentage of sequences (rows) a pattern should occur.
    constraints: Union[list, None]
        The constraints enforced in pattern mining. constraints=None default.

    Returns
    -------
    Mined patterns

    """

    seq2pat = sp.Seq2Pat(sequences=items)

    if constraints:
        for constraint in constraints:
            seq2pat.add_constraint(constraint)

    patterns = seq2pat.get_patterns(min_frequency=min_frequency)

    return patterns


def dichotomic_pattern_mining(items: List[list], labels: List[int],
                              seq2pat_pos: object, seq2pat_neg: object,
                              min_frequency_pos: Num = 0.3, min_frequency_neg: Num = 0.3,
                              pattern_aggregation: str = 'union'):
    """
    Run dichotomic pattern mining (DPM)

    Parameters
    ----------
    items: List[list]
        A list of sequences of items. This input is kept for consistency to Seq2pat APIs, but will not be used in DPM.
    labels: List[int]
        A list of binary labels. This input is kept for consistency to Seq2pat APIs, but will not be used in DPM.
    seq2pat_pos: Seq2Pat object
        A constraint model to mine patterns in positive sequences
    seq2pat_neg: Seq2Pat object
        A constraint model to mine patterns in negative sequences
    min_frequency_pos: Num
        Minimum frequency threshold for positive sequences
        If int, represents the minimum number of sequences (rows) a pattern should occur
        If float, should be (0.0, 1.0] and represents
        the minimum percentage of sequences (rows) a pattern should occur.
    min_frequency_neg: Num
        Minimum frequency threshold for negative sequences
        If int, represents the minimum number of sequences (rows) a pattern should occur
        If float, should be (0.0, 1.0] and represents
        the minimum percentage of sequences (rows) a pattern should occur.
    pattern_aggregation: str
        If 'union', DPM returns the union of patterns from mining positive and negative sequences.
        If 'intersection', DPM returns the intersection of patterns from mining positive and negative sequences.
        If 'unique_positive', DPM returns patterns that are unique in positive sequences.
        If 'unique_negative', DPM returns patterns that are unique in negative sequences.
        If 'all', DPM returns all patterns in the above cases with a tuple, following the order (union, intersection,
        unique_positive, unique_negative)

    Returns
    -------
    Mined patterns by running DPM.

    """

    # Mine positive cohort
    patterns_pos = seq2pat_pos.get_patterns(min_frequency=min_frequency_pos)

    # Mine negative cohort
    patterns_neg = seq2pat_neg.get_patterns(min_frequency=min_frequency_neg)

    # Drop frequencies in the end of mined patterns
    patterns_pos = drop_frequency(patterns_pos)
    patterns_neg = drop_frequency(patterns_neg)

    # Find pattern aggregations
    if pattern_aggregation == Constants.unique_pos:
        dpm_patterns = set(map(tuple, patterns_pos)) - set(map(tuple, patterns_neg))

    elif pattern_aggregation == Constants.unique_neg:
        dpm_patterns = set(map(tuple, patterns_neg)) - set(map(tuple, patterns_pos))

    elif pattern_aggregation == Constants.intersection:
        dpm_patterns = set(map(tuple, patterns_pos)).intersection(set(map(tuple, patterns_neg)))

    elif pattern_aggregation == Constants.union:
        dpm_patterns = set(map(tuple, patterns_pos)).union(set(map(tuple, patterns_neg)))

    elif pattern_aggregation == Constants.all_operations:

        union_patterns = set(map(tuple, patterns_pos)).union(set(map(tuple, patterns_neg)))
        union_patterns = sorted(list(map(list, union_patterns)))

        intersection_patterns = set(map(tuple, patterns_pos)).intersection(set(map(tuple, patterns_neg)))
        intersection_patterns = sorted(list(map(list, intersection_patterns)))

        unique_pos_patterns = set(map(tuple, patterns_pos)) - set(map(tuple, patterns_neg))
        unique_pos_patterns = sorted(list(map(list, unique_pos_patterns)))

        unique_neg_patterns = set(map(tuple, patterns_neg)) - set(map(tuple, patterns_pos))
        unique_neg_patterns = sorted(list(map(list, unique_neg_patterns)))

        return union_patterns, intersection_patterns, unique_pos_patterns, unique_neg_patterns

    else:
        raise ValueError("Invalid pattern_aggregation! It should be chosen from one of the following options: "
                         "'unique_positive', 'unique_negative', 'intersection', 'union' and 'all'.")

    return sorted(list(map(list, dpm_patterns)))


def get_average_one_seq(seq):
    return statistics.mean(seq)


def get_median_one_seq(seq):
    return statistics.median(seq)


def get_gap_one_seq(seq):
    return [i - j for i, j in zip(seq[1:], seq[:-1])]


def get_span_one_seq(seq):
    return max(seq) - min(seq)


def validate_attribute_values(values: List[list]):
    """
    Validate attribute values

    """
    check_true(values is not None, ValueError("Values cannot be null"))
    check_true(isinstance(values, list), ValueError("Values need to be a list of lists"))
    check_true(len(values) >= 1, ValueError("Values cannot be an empty list."))
    not_list = [("index: " + str(i), values[i]) for i in range(len(values)) if not isinstance(values[i], list)]
    check_true(len(not_list) == 0, ValueError("Values need to be a list of lists. ", not_list))
    is_empty_list = any([len(values[i]) == 0 for i in range(len(values))])
    check_false(is_empty_list, ValueError("Values cannot contain any empty list."))


def validate_sequences(sequences: List[list]):
    """
    Validate sequences

    """
    check_true(sequences is not None, ValueError("Sequences cannot be null."))
    check_true(isinstance(sequences, list), ValueError("Sequences need to be a list of lists."))
    check_true(len(sequences) >= 1, ValueError("Sequences cannot be an empty list."))
    not_list = [(sequences[i], i) for i in range(len(sequences)) if not (isinstance(sequences[i], list))]
    check_true(len(not_list) == 0, ValueError("Sequences need to be a list of lists.", not_list))
    is_empty_list = any([len(sequences[i]) == 0 for i in range(len(sequences))])
    check_false(is_empty_list, ValueError("Sequences cannot contain any empty list."))
