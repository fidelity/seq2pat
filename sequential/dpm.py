# -*- coding: utf-8 -*-
# SPDX-License-Identifier: GPL-2.0

from typing import Union, List, Dict

import pandas as pd

from sequential.seq2pat import Seq2Pat, _Constraint
from sequential.csp_global import is_satisfiable
from sequential.csp_local import is_satisfiable_in_rolling
from sequential.utils import Num, drop_frequency, check_true, item_map, string_to_int


class DichotomicAggregation:
    intersection = 'intersection'
    union = 'union'
    unique_neg = 'unique_negative'
    unique_pos = 'unique_positive'


def dichotomic_pattern_mining(seq2pat_pos: Seq2Pat, seq2pat_neg: Seq2Pat,
                              min_frequency_pos: Num = 0.3, min_frequency_neg: Num = 0.3) -> Dict[str, List[list]]:
    """
    Run dichotomic pattern mining (DPM)

    Parameters
    ----------
    seq2pat_pos: Seq2Pat object
        A constraint model to mine patterns in positive sequences
    seq2pat_neg: Seq2Pat object
        A constraint model to mine patterns in negative sequences
    min_frequency_pos: Num
        Minimum frequency threshold for positive sequences. min_frequency_pos = 0.3 by default.
        If int, represents the minimum number of sequences (rows) a pattern should occur
        If float, should be (0.0, 1.0] and represents
        the minimum percentage of sequences (rows) a pattern should occur.
    min_frequency_neg: Num
        Minimum frequency threshold for negative sequences. min_frequency_neg = 0.3 by default.
        If int, represents the minimum number of sequences (rows) a pattern should occur
        If float, should be (0.0, 1.0] and represents
        the minimum percentage of sequences (rows) a pattern should occur.

    Returns
    -------
    Dictionary of DPM patterns with keys for union, intersection, unique_pos and unique_neg.
    Each aggregation has the patterns to be sorted.

    """

    # Mine positive cohort
    patterns_pos = seq2pat_pos.get_patterns(min_frequency=min_frequency_pos)

    # Mine negative cohort
    patterns_neg = seq2pat_neg.get_patterns(min_frequency=min_frequency_neg)

    # Drop frequencies in the end of mined patterns
    patterns_pos = drop_frequency(patterns_pos)
    patterns_neg = drop_frequency(patterns_neg)

    aggregation_to_patterns = dict()

    intersection_patterns = set(map(tuple, patterns_pos)).intersection(set(map(tuple, patterns_neg)))
    aggregation_to_patterns[DichotomicAggregation.intersection] = sorted(list(map(list, intersection_patterns)))

    union_patterns = set(map(tuple, patterns_pos)).union(set(map(tuple, patterns_neg)))
    aggregation_to_patterns[DichotomicAggregation.union] = sorted(list(map(list, union_patterns)))

    unique_neg_patterns = set(map(tuple, patterns_neg)) - set(map(tuple, patterns_pos))
    aggregation_to_patterns[DichotomicAggregation.unique_neg] = sorted(list(map(list, unique_neg_patterns)))

    unique_pos_patterns = set(map(tuple, patterns_pos)) - set(map(tuple, patterns_neg))
    aggregation_to_patterns[DichotomicAggregation.unique_pos] = sorted(list(map(list, unique_pos_patterns)))

    return aggregation_to_patterns


def get_one_hot_encodings(sequences: List[list], patterns: List[list],
                          constraints: Union[List[_Constraint], None] = None,
                          rolling_window_size: Union[int, None] = 10, drop_pattern_frequency=True) -> pd.DataFrame:
    """
    Create a data frame having one-hot encoding of sequences.

    Parameters
    ----------
    sequences: List[list]
        A list of sequences of items.
    patterns: List[list]
        A list of interested patterns, which defines the encoding space.
    constraints: Union[list, None]
        The constraints enforced in the creation of encoding
    rolling_window_size: Union[int, None]
        The rolling window along a sequence within which patterns are detected locally. It controls the length of
        sequence subject to the pattern detection, to speed up the encodings generation.
        (rolling_window_size=10 by default). When rolling_window_size=None, patterns are detected globally.
    drop_pattern_frequency: bool
        Drop the frequency appended in the end of each input pattern, drop_pattern_frequency=True by default.

    Returns
    -------
    A data frame having one-hot encoding of sequences using the given patterns.

    Example
        sequence      feature_0 feature_1 feature_2 ...
        [A,A,B,A,D]    1         1         0        ...
        [C,B,A]        0         1         1        ...
        [C,A,C,D]      1         0         1        ...

    """

    # Drop the frequency appended
    if drop_pattern_frequency:
        patterns = drop_frequency(patterns)

    str_sequences = None
    if isinstance(sequences[0][0], str):
        check_true(not isinstance(patterns[0][-1], int),
                   ValueError("Patterns should not contain integers! "
                              "Check if the frequency is appended to the end of given patterns."))
        check_true(isinstance(patterns[0][0], str),
                   ValueError("When items are strings, patterns should also be strings."))

        # If sequences contain strings, map strings to integers for running csp_global
        str_sequences = sequences.copy()
        str_to_int, int_to_str = item_map(sequences)
        sequences = string_to_int(str_to_int, sequences)
        patterns = string_to_int(str_to_int, patterns)

    df = pd.DataFrame()
    df['sequence'] = sequences

    # For each pattern, create encoding for all sequences
    for i, pattern in enumerate(patterns):

        # If window size is given, run the local/approximate model
        if rolling_window_size:
            df['feature_' + str(i)] = df.apply(lambda row: is_satisfiable_in_rolling(row['sequence'], pattern,
                                                                                     row.name, constraints,
                                                                                     rolling_window_size), axis=1)

        # Otherwise, run the global model
        else:
            df['feature_' + str(i)] = df.apply(lambda row: is_satisfiable(row['sequence'], pattern,
                                                                          row.name, constraints), axis=1)

        # Cast bool type value to int
        df['feature_' + str(i)] = df['feature_' + str(i)].astype(int)

    # If sequences are mapped from strings to integers, recover the original sequences
    if str_sequences:
        df['sequence'] = str_sequences

    return df
