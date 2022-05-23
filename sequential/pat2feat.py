# -*- coding: utf-8 -*-
# SPDX-License-Identifier: GPL-2.0

from typing import List, Union
import pandas as pd

from sequential.seq2pat import _Constraint
from sequential.utils import drop_frequency, check_true, item_map, string_to_int
from sequential.csp_global import is_satisfiable
from sequential.csp_local import is_satisfiable_in_rolling


class _OneHotEncoding:
    """
    The implementer class of one-hot encodings generation.
    """

    def __init__(self, rolling_window_size: Union[int, None] = 10):
        """
        Attributes
        ----------
        rolling_window_size: Union[int, None]
            The rolling window along a sequence within which patterns are detected locally. It controls the length of
            sequence subject to the pattern detection, to speed up the encodings generation.
            (rolling_window_size=10 by default). When rolling_window_size=None, patterns are detected globally.

        """

        self.rolling_window_size = rolling_window_size

    def transform(self, sequences: List[list], patterns: List[list],
                  constraints: Union[List[_Constraint], None] = None):
        """
        Create one-hot encodings of sequences with the provided patterns and constraints

        Parameters
        ----------
        sequences: List[list]
            A list of sequences of items.
        patterns: List[list]
            A list of interested patterns, which defines the encoding space.
        constraints: Union[list, None]
            The constraints enforced in the creation of encoding. constraints=None by default.

        Returns
        -------
        A data frame having one-hot encoding of sequences using the given patterns.

        Example
        sequence      feature_0 feature_1 feature_2 ...
        [A,A,B,A,D]    1         1         0        ...
        [C,B,A]        0         1         1        ...
        [C,A,C,D]      1         0         1        ...

        """

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
            if self.rolling_window_size:
                df['feature_' + str(i)] = df.apply(lambda row: is_satisfiable_in_rolling(row['sequence'], pattern,
                                                                                         row.name, constraints,
                                                                                         self.rolling_window_size),
                                                   axis=1)

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


class Pat2Feat:
    """
    **Pat2Feat: Pat2Feat: Pattern-to-Feature Generation**

    """

    def __init__(self):

        # Initialize the implementer of one-hot encodings generation
        self._imp = None

    def get_features(self, sequences: List[list], patterns: List[list],
                     constraints: Union[List[_Constraint], None] = None,
                     rolling_window_size: Union[int, None] = 10,
                     drop_pattern_frequency: bool = True):
        """
        Create a data frame having one-hot encoding of sequences.

        Parameters
        ----------
        sequences: List[list]
            A list of sequences of items.
        patterns: List[list]
            A list of interested patterns, which defines the encoding space.
        constraints: Union[list, None]
            The constraints enforced in the creation of encoding. constraints=None by default.
        rolling_window_size: Union[int, None]
            The rolling window along a sequence within which patterns are detected locally. It controls the length of
            sequence subject to the pattern detection, to speed up the encodings generation.
            (rolling_window_size=10 by default). When rolling_window_size=None, patterns are detected globally.
        drop_pattern_frequency: bool
            Drop the frequency appended in the end of each input pattern, drop_pattern_frequency=True by default.

        Returns
        -------
        A data frame having extracted features of sequences using the given patterns.

        Example of one_hot encodings as features
            sequence      feature_0 feature_1 feature_2 ...
            [A,A,B,A,D]    1         1         0        ...
            [C,B,A]        0         1         1        ...
            [C,A,C,D]      1         0         1        ...
        """

        if drop_pattern_frequency:
            patterns = drop_frequency(patterns)

        self._imp = _OneHotEncoding(rolling_window_size=rolling_window_size)

        return self._imp.transform(sequences, patterns, constraints=constraints)
