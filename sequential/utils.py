# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0
import collections
import numpy as np
from typing import Union, NoReturn, List, Optional

Num = Union[int, float]


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


def string_to_int(mapping: map, items: List[List[str]]) -> List[List[int]]:
    """
    Utility function to transform string input to int input to be used by sequential library
    :param mapping: map[str, int]
    :param items: a list of strings
    :return: a list of integers where each string is replaced by an integer 'id'
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
    Finds and returns minimum value in items
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


def drop_frequency(result: List[list]) -> list:
    """
    Drop the frequency appended to each mined pattern.

    Parameters
    ----------
    result: List[list]
        The mined patterns with each one having the count appended to the end

    Returns
    -------
    The list of mined patterns without appended frequency

    """
    return list(map(lambda x: x[:-1], result))


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
    if not isinstance(sequences[0][0], str):
        min_int = get_min_value(sequences)
        check_true(min_int > 0, ValueError("Integers in the sequence must be greater than 0."))


def validate_max_span(max_span: Union[int, None]):
    """
    Validate max_span

    """
    if max_span:
        check_true(isinstance(max_span, int), ValueError("Maximum span should be an integer."))
        check_true(max_span > 1, ValueError("Maximum span should be greater than 1."))


def validate_min_frequency(num_rows, min_frequency):
    """
    Validate min_frequency

    """
    # Check min_frequency conditions
    if isinstance(min_frequency, float):
        check_true(0.0 < min_frequency,
                   ValueError("Minimum frequency percentage should be greater than 0.0. "
                              "Current minimum frequency is {}.".format(min_frequency)))
        check_true(min_frequency <= 1.0, ValueError("Minimum frequency percentage should be less than 1.0. "
                                                    "Current minimum frequency is {}.".format(min_frequency)))
        check_true(min_frequency * num_rows >= 1.0, ValueError("Minimum frequency percentage should set the minimum "
                                                               "row count to be no less than 1.0. "
                                                               "Thus the percentage should be no less than "
                                                               "1/(number of sequences)."))
    elif isinstance(min_frequency, int):
        check_true(0 < min_frequency, ValueError("Minimum frequency should be greater than 0.0. "
                                                 "Current minimum frequency is {}.".format(min_frequency)))
        check_true(min_frequency <= num_rows, ValueError("Minimum frequency cannot be more than number of sequences. "
                                                         "Current minimum frequency is {}.".format(min_frequency)))
    else:
        raise TypeError("Minimum frequency should be integer (as a row count) or float (as a row percentage).")


def validate_batch_args(batch_size: Optional, discount_factor: float, n_jobs: int, seed: int) -> NoReturn:
    """
    Validate arguments for running seq2pat on batches.

    Parameters
    ----------
    batch_size: Optional
        The number of sequences in one batch. When it is None, seq2pat will run on entire set.
    n_jobs: int
        n_jobs defines the number of processes (n_jobs=2 by default) that are used when mining tasks are applied
        on batches in parallel. If -1 all CPUs are used. If -2, all CPUs but one are used.
    seed: int
        The random seed.
    discount_factor: float
        A discount factor is used to reduce the minimum row count (min_frequency) threshold when Seq2Pat is applied
        on a batch. A valid discount factor should be greater than 0 and <= 1.0.
    """
    if batch_size:
        check_true(isinstance(batch_size, int), TypeError("The batch_size must be an integer."))
        check_true(batch_size > 0, ValueError('The batch_size must be greater than zero.'))
    check_true(isinstance(n_jobs, int), TypeError("The n_jobs must be an integer."))
    check_true(n_jobs != 0, ValueError('The n_jobs cannot be zero.'))
    check_true(isinstance(seed, int), TypeError("The seed must be an integer."))
    check_true(isinstance(discount_factor, float), ValueError('The discount_factor must be a float.'))
    check_true(discount_factor > 0, ValueError('The discount_factor must be greater than zero.'))
    check_true(discount_factor <= 1.0, ValueError('The discount_factor must be less or equal to 1.0.'))


def update_min_frequency(num_rows: int, min_frequency: float, discount_factor: float) -> float:
    """
    Update min_frequency when Seq2Pat runs on batches.

    Parameters
    ----------
    num_rows: int
        The total number of sequences.
    min_frequency: float
        It should be float for mining batches. The minimum percentage of sequences (rows) a pattern should occur.
    discount_factor: float
        The discount factor is used to reduce the minimum row count (min_frequency)

    Returns
    -------
    The reduced min_frequency parameter

    """

    return max(min_frequency * discount_factor, 1.0/num_rows)


def list_to_counter(patterns: List[List]) -> collections.Counter:
    """
    Transform patterns to counter.

    Parameters
    ----------
    patterns: List[List]
        The mined patterns.

    Returns
    -------
    Return a counter of patterns, using pattern as the key.
    """
    patterns_without_frequency = list(map(lambda x: tuple(x[:-1]), patterns))
    frequencies = list(map(lambda x: x[-1], patterns))

    return collections.Counter(dict(zip(patterns_without_frequency, frequencies)))


def counter_to_list(patterns_counter: collections.Counter, min_row_count: int) -> List[List]:
    """
    Transform counter of patterns to list. Drop the patterns with frequency less than min_row_count.

    Parameters
    ----------
    patterns_counter: collections.Counter
        The counter of patterns, using pattern as the key.
    min_row_count: int
        The minimum frequency required for mining the original entire set.

    Returns
    -------
    Return a list of patterns, with all patterns satisfying a minimum frequency threshold.
    """
    results = []
    for key, value in patterns_counter.items():
        if value < min_row_count:
            continue
        results.append(list(key) + [value])

    return results


def aggregate_patterns(batch_patterns: List[List[List]], min_row_count: int) -> List[List]:
    """
    Aggregate patterns mined from different batches by counts. Use the summation of counts as final frequency.

    Parameters
    ----------
    batch_patterns: List[List[List]]
        The patterns mined from batches.
    min_row_count: int
        The minimum frequency required for mining the original entire set.

    Returns
    -------
    Return a list of patterns in the descending order by frequency, with all patterns satisfying minimum frequency
    required for mining the original entire set.
    """
    counter = collections.Counter()
    for patterns in batch_patterns:
        counter.update(list_to_counter(patterns))

    aggregated_patterns = counter_to_list(counter, min_row_count)

    return sort_pattern(aggregated_patterns)