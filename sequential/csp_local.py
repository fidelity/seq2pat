# -*- coding: utf-8 -*-
# SPDX-License-Identifier: GPL-2.0

import statistics
from typing import Union, Tuple, List

from sequential.seq2pat import _Constraint


def _get_average(sequence):
    return statistics.mean(sequence)


def _get_median(sequence):
    return statistics.median(sequence)


def _get_gap(sequence):
    return [i - j for i, j in zip(sequence[1:], sequence[:-1])]


def _get_span(sequence):
    return max(sequence) - min(sequence)


def _is_subsequence(list1: list, list2: list) -> bool:
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


def _subsequence_identifier(sequence: list, pattern: list, seq_attr_ind: int, constraints: Union[list, None],
                            rolling_window_size: int, seq_attr_start: int) -> bool:
    """
    Identify if a pattern is in a given sequence, subject to the optional seq2pat._Constraint type of constraints.

    """
    res = False

    if not _is_subsequence(pattern, sequence):
        # if pattern is not a subsequence of seq, return False
        return res
    else:
        if not constraints:
            # if pattern is a subsequence and there is no constraint, return True
            return True
        else:
            res = _meet_constraints_in_rolling(sequence, pattern, seq_attr_ind, constraints, rolling_window_size,
                                               seq_attr_start)

    return res


def _meet_constraints_in_rolling(sequence: list, pattern: list, seq_attr_ind: int,
                                 constraints: Union[List[_Constraint], None],
                                 rolling_window_size: int, window_start_ind: int) -> bool:
    """
    Check if a pattern is in an individual sequence of items, subject to defined constraints.

    Parameters
    ----------
    sequence: list
        A sequence of items within which a pattern is searched.
    pattern: list
        A pattern that is going to be checked in the sequence.
    seq_attr_ind: int
        The index of this sequence in the list of sequences, and also the index of attributes.
    constraints: Union[list, None]
        A list of constraints
    rolling_window_size: int
        The rolling window along a sequence within which patterns are detected.
    window_start_ind: int
        The index where a rolling window starts.

    Returns
    -------
    A boolean result to return if all constraints are met.

    """

    # Get all matched subsequences and their index
    _, item_subsequences_indices = _get_matched_subsequences(sequence, pattern)

    meet_all_constraints = False
    for sub_ind, s in enumerate(item_subsequences_indices):

        # Check constraints
        res = True
        for constraint in constraints:
            # Get attributes
            attrs = constraint.attribute.values[seq_attr_ind]
            attrs = attrs[window_start_ind:window_start_ind + rolling_window_size]

            # Get subsequences of attributes
            attr_subsequence = [attrs[i] for i in s]

            if isinstance(constraint, _Constraint.Average):
                attr_info = _get_average(attr_subsequence)
                if not constraint.check_satisfaction(attr_info):
                    res = False
                    break

            if isinstance(constraint, _Constraint.Median):
                attr_info = _get_median(attr_subsequence)
                if not constraint.check_satisfaction(attr_info):
                    res = False
                    break

            if isinstance(constraint, _Constraint.Span):
                attr_info = _get_span(attr_subsequence)
                if not constraint.check_satisfaction(attr_info):
                    res = False
                    break

            if isinstance(constraint, _Constraint.Gap):
                attr_info = _get_gap(attr_subsequence)
                if not constraint.check_satisfaction(attr_info):
                    res = False
                    break

        if res:
            meet_all_constraints = True
            break

    return meet_all_constraints


def _get_matched_subsequences(sequence: list, pattern: list) -> Tuple[list, list]:
    """
    Find all possible subsequences of a sequence in a recursive way.
    For every element in the list, there are two choices, either to include it in the subsequence or not include it.
    Apply this for every element in the list, find the subsequences for the two cases separately.

    """
    res_seq = []
    res_ind = []
    indices = list(range(len(sequence)))

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

    get_subsequence(sequence, [], indices, [])

    return res_seq, res_ind


def is_satisfiable_in_rolling(sequence: list, pattern: list, seq_attr_ind: int,
                              constraints: Union[List[_Constraint], None],
                              rolling_window_size: int) -> bool:
    """
     Search the given pattern in a rolling_window of sequence

    """
    res = False

    if len(sequence) <= rolling_window_size:
        res = _subsequence_identifier(sequence, pattern, seq_attr_ind, constraints, rolling_window_size, 0)

    else:
        num_iters = len(sequence) - rolling_window_size
        for i in range(num_iters + 1):
            if _subsequence_identifier(sequence[i:i + rolling_window_size], pattern, seq_attr_ind, constraints,
                                       rolling_window_size, i):
                res = True
                break
    return res
