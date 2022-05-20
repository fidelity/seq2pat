# -*- coding: utf-8 -*-
# SPDX-License-Identifier: GPL-2.0

from typing import List, Dict

from sequential.seq2pat import Seq2Pat
from sequential.utils import Num, drop_frequency


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
