# -*- coding: utf-8 -*-
# SPDX-License-Identifier: GPL-2.0
import gc
import numpy as np
from typing import NamedTuple, List, Dict, NoReturn, Optional, Tuple
from multiprocessing import Process, Queue
from copy import deepcopy
from joblib import Parallel, delayed

from sequential.backend import seq_to_pat as stp
from sequential.utils import Num, check_true, get_max_column_size, \
    get_min_value, get_max_value, sort_pattern, item_map, \
    string_to_int, int_to_string, check_sequence_feature_same_length, \
    validate_attribute_values, validate_sequences, validate_max_span, \
    aggregate_patterns, validate_min_frequency, validate_batch_args, update_min_frequency

from sequential._version import __author__, __copyright__, __email__, __version__

__author__ = __author__
__copyright__ = __copyright__
__email__ = __email__
__version__ = __version__


# IMPORTANT: Constant values should not be changed
# These represent parameters in C++ backend that need to be set by matching exact names
class _Constants:
    # List where values correspond to the value of upper gap constraints on an attribute, and
    # whose id can be found in ugapi at the same index
    ugap = 'ugap'

    # List where values are attribute ids of attributes that have upper gap constraints, and
    # where the value of the constraint can be found in ugap at the same index
    ugapi = 'ugapi'

    # List where values correspond to the value of lower gap constraints on an attribute, and
    # whose id can be found in lgapi at the same index
    lgap = 'lgap'

    # List where values values are attribute ids of attributes that have lower gap constraints, and
    # where the value of the constraint can be found in lgap at the same index
    lgapi = 'lgapi'

    # List where values correspond to the value of lower average constraints on an attribute, and
    # whose id can be found in lavri at the same index
    lavr = 'lavr'

    # List where values values are attribute ids of attributes that have lower average constraints, and
    # where the value of the constraint can be found in lavr at the same index
    lavri = 'lavri'

    # List where values correspond to the value of upper average constraints on an attribute, and
    # whose id can be found in uavri at the same index
    uavr = 'uavr'

    # List where values values are attribute ids of attributes that have  upper average constraints, and
    # where the value of the constraint can be found in uavr at the same index
    uavri = 'uavri'

    # List where values correspond to the value of lower span constraints on an attribute, and
    # whose id can be found in lspni at the same index
    lspn = 'lspn'

    # List where values values are attribute ids of attributes that have  lower span constraints, and
    # where the value of the constraint can be found in lspn at the same index
    lspni = 'lspni'

    # List where values correspond to the value of lower span constraints on an attribute, and
    # whose id can be found in uspni at the same index
    uspn = 'uspn'

    # List where values values are attribute ids of attributes that have upper span constraints, and
    # where the value of the constraint can be found in uspn at the same index
    uspni = 'uspni'

    # List where values correspond to the value of lower median constraints on an attribute, and
    # whose id can be found in lmedi at the same index
    lmed = 'lmed'

    # List where values correspond to the value of upper median constraints on an attribute, and
    # whose id can be found in umedi at the same index
    umed = 'umed'

    # List where values values are attribute ids of attributes that have  upper median constraints, and
    # where the value of the constraint can be found in umed at the same index
    umedi = 'umedi'

    # List where values values are attribute ids of attributes that have  upper median constraints, and
    # where the value of the constraint can be found in lmed at the same index
    lmedi = 'lmedi'

    # List where the indexes correspond to the attribute ids and values correspond to the number of
    # upper span constraints on that attribute
    num_minmax = 'num_minmax'

    # List where the indexes correspond to the attribute ids and the values correspond to the number of
    # average constraints on that attribute
    num_avr = 'num_avr'

    # List where the indexes correspond to the attribute ids and values correspond to the number of
    # median constraints on that attribute
    num_med = 'num_med'

    # List where values are attribute ids of attribute that have gap constraints
    tot_gap = 'tot_gap'

    # List where values are attribute ids of attribute that have span constraints
    tot_spn = 'tot_spn'

    # List where values are attribute ids of attribute that have average constraints
    tot_avr = 'tot_avr'

    # Number of attributes that constraint are enforced on
    num_att = 'num_att'

    # List of sequences that will be mined for sequences
    items = 'items'

    # List of attributes that constraints will be imposed on during mining
    attrs = 'attrs'

    # Length of the largest sequence in items
    M = 'M'

    # Number of sequences in items
    N = 'N'

    # If integer sequences, the largest value, if string sequences the number of events
    L = 'L'

    # List where index correspond to attribute ids and values to the maximum value for that attribute
    max_attrs = 'max_attrs'

    # List where index correspond to the attribute ids and values to the minimum value for that attribute
    min_attrs = 'min_attrs'

    # The data size threshold to dynamically decide if batch processing is needed to ease mining task
    dynamic_batch_threshold = 500000

    # If batch_size is not set while the dataset has more than dynamic_batch_threshold sequences,
    # batch_size is set to be default_batch_size, to apply batch processing
    default_batch_size = 10000

    # Default seed to define a random state
    default_seed = 123456


class Attribute:

    def __init__(self, values: List[list]):
        """Attribute with given values.

        Attributes
        ----------
        values: List[list]
            A list of lists corresponding to the values of each event.
        """
        # Validate input values
        validate_attribute_values(values)

        self._values = values
        self._max = get_max_value(values)
        self._min = get_min_value(values)

    @property
    def values(self):
        """Values

        The values of the attribute
        """
        return self._values

    def _set_values(self, values):
        """Set values of attribute

        This function is used when Seq2Pat runs on batches of sequences. In each batch, the attributes and constraints
        need to be reset to be consistent to the sequences. Since the upper and lower bound are set on the entire set,
        it would be easier to copy the existing constraints but only reset the attribute values in a batch. It would be
        prevented to set values directly, thus we add the function to reset the attribute values.
        """
        self._values = values

    def average(self):
        """The Average Constraint

        Restricts the average value of a pattern.
        """
        return _Constraint.Average(self)

    def gap(self):
        """The Gap Constraint

        Restricts the difference between every two consecutive event values in a pattern.
        """
        return _Constraint.Gap(self)

    def median(self):
        """The Median Constraint

        Restricts the median value of a pattern.
        """
        return _Constraint.Median(self)

    def span(self):
        """The Span Constraint

        Restricts the difference between the maximum and the minimum value in a pattern.
        """
        return _Constraint.Span(self)


class _BaseConstraint:

    def __init__(self, attribute: Attribute):
        self._attribute = attribute
        self._lower_bound = None
        self._upper_bound = None

    @property
    def attribute(self):
        return self._attribute

    @property
    def lower_bound(self):
        return self._lower_bound

    @property
    def upper_bound(self):
        return self._upper_bound

    def has_lower_bound(self):
        return self.lower_bound is not None

    def has_upper_bound(self):
        return self.upper_bound is not None

    def check_satisfaction(self, value):
        # Initialize returned results. When there are no constraints, result is explicitly set to be true.
        res = True

        if self.has_upper_bound():
            if value > self.upper_bound:
                return False

        if self.has_lower_bound():
            if value < self.lower_bound:
                return False

        return res

    def __le__(self, other):
        self._upper_bound = other
        return self

    def __ge__(self, other):
        self._lower_bound = other
        return self


class _Constraint(NamedTuple):
    class Average(_BaseConstraint):

        def __init__(self, attribute: Attribute):
            super().__init__(attribute)

    class Gap(_BaseConstraint):

        def __init__(self, attribute: Attribute):
            super().__init__(attribute)

        def check_satisfaction(self, value):
            # Initialize returned results to be true.
            res = True

            if self.has_upper_bound():
                if max(value) > self.upper_bound:
                    return False

            if self.has_lower_bound():
                if min(value) < self.lower_bound:
                    return False

            return res

    class Median(_BaseConstraint):

        def __init__(self, attribute: Attribute):
            super().__init__(attribute)

    class Span(_BaseConstraint):

        def __init__(self, attribute: Attribute):
            super().__init__(attribute)


class Seq2Pat:
    """**Seq2Pat: Sequence-to-Pattern Generation Library**

    Attributes
    ----------
    sequences: List[list]
        A list of sequences each with a list of events.
        The event values can be all strings or all integers.
    max_span: Optional[int]
        The value for applying a built-in maximum span constraint to the length of items in mining, max_span=10 by
        default (10 items). This is going to avoid regular users to run into a scaling issue when data contains long
        sequences but no constraints are used to run the mining efficiently and practically.
        Power users can choose to drop this constraint by setting it to be None or increase the maximum span
        as the system has resources to support.
    batch_size: Optional[int]
        The batch_size parameter is set to be None by default, then a mining task runs on the entire data set using a
        single thread. When batch_size is set, Seq2Pat runs on batches of sequences instead for improving scalability.
        Each batch contains `batch_size` sequences as a **random** sample of entire set. This is achieved by shuffling
        the entire set uniformly before we sequentially split the sequences into batches. A mining task will run on each
        batch with a reduced minimum row count (min_frequency) threshold. Please refer to description of discount_factor
        parameter for how min_frequency is reduced. Resulted patterns will be aggregated from the mining results of
        each batch by calculating the sum of the occurrences. Finally the original minimum row count threshold is
        applied to the patterns after aggregation. When batch_size is None but the dataset has more than
        _Constants.dynamic_batch_threshold sequences, batch_size is dynamically set to be _Constants.default_batch_size to
        ease the mining task on the large dataset by default. Power users can define specific batch_size,
        discount_factor and n_jobs for gaining more runtime benefit.
    discount_factor: float
        A discount factor is used to reduce the minimum row count (min_frequency) threshold when Seq2Pat is applied
        on a batch. The new threshold for a batch is defined to be max(min_frequency * discount_factor, 1.0/batch_size),
        where an integer min_frequency will be converted to a ratio first by min_frequency/number_total_sequences.
        Final results will be based on the aggregation of patterns from each batch by calculating the sum of the
        occurrences. Theoretically there is a chance that the batching results will be different from non-batching
        results. But a small discount_factor parameter will make the chance to be minimal and thus we have the same
        results as running on entire set in practices. A small value of discount_factor is thus recommended.
        discount_factor=0.2 by default.
    n_jobs: int
        n_jobs defines the number of processes (n_jobs=2 by default) that are used when mining tasks are applied
        on batches in parallel. If -1 all CPUs are used. If -2, all CPUs but one are used.
    seed: int
        Random seed to make sequences uniformly distributed among batches.

    Note
    ----
        For power users who have interests to learn more about the designed batch processing behavior, an Experimental\
        Results Summary in the following would be useful.

        - We have experimental analysis for batch_size vs. discount_factor vs. runtime tested on a data set with \
        100k sequences.

        - The results show that when batch_size increases, e.g. from 10000 to 100000, we observe an increase in runtime,\
        while the mined patterns are all the same as mining on the entire set using single thread.

        - When batch_size=10000, we get the most runtime benefit compared to running on entire set.

        - On the same 100k sequences, we set batch_size=10000 and change discount_factor from 0.1 to 1.0. We observe\
        that the runtime decreases as discount_factor increases. Only when discount_factor=1.0, the batching mode will\
        miss some patterns compared to running on entire set. We would recommend discount_factor=0.2 by default for\
        the robustness in results, at the expenses of runtime.

        - In an even larger test on ~1M sequences, we set batch_size=10000, discount_factor=0.8, n_jobs=8.\
        Batch mode saves 60% of the runtime compared to running on entire set, while the resulted patterns from the\
        two processes are the same.

        - When data size is small, e.g., a few thousand sequences, there is no benefit to run batch mode.\
        Thus, we would recommend using the batch mode only when data has at least hundreds of thousands of sequences\
        for gaining the runtime benefit.
    """

    def __init__(self, sequences: List[list], max_span: Optional[int] = 10,
                 batch_size=None, discount_factor=0.2, n_jobs=2, seed=_Constants.default_seed):
        # Validate input
        validate_sequences(sequences)
        validate_max_span(max_span)
        validate_batch_args(batch_size, discount_factor, n_jobs, seed)

        # Input sequences
        self._sequences: List[list] = sequences

        # Sequences as strings or integers
        self._is_string = isinstance(sequences[0][0], str)

        # If string, internal mapping to between strings and integers
        if self._is_string:
            self._str_to_int, self._int_to_str = item_map(self.sequences)
            self._sequences = string_to_int(self._str_to_int, self.sequences)

        # Set size variables
        self._num_rows = len(self.sequences)
        self._max_num_columns = get_max_column_size(self.sequences)
        self._max_value = get_max_value(self.sequences)

        # Constraint store: attribute_id -> constraint_name -> Constraint
        self.attr_to_cts: Dict[Attribute, Dict[str, _Constraint]] = dict()

        # Cython implementor object
        self._cython_imp = None

        if max_span:
            # Create index attribute
            index_attr = Attribute([[i for i in range(len(seq))] for seq in sequences])

            # Add built-in maximum span constraint on index.
            # The minimum span is at least 1 between two indices. Here we add it explicitly.
            # Given max_span items, the maximum difference on the index is (max_span - 1)
            self.add_constraint(1 <= index_attr.span() <= (max_span - 1))

        # Dynamically set batch_size to ease the mining task on a large dataset by default
        # If batch_size is None and num_rows > dynamic_batch_threshold, set batch_size to apply batch processing
        # For dataset having num_rows <= dynamic_batch_threshold, mining task runs on entire set if batch_size=None
        # Power users can define specific batch_size, discount_factor and n_jobs for gaining more runtime benefit
        if not batch_size and self._num_rows > _Constants.dynamic_batch_threshold:
            self.batch_size = _Constants.default_batch_size
        else:
            self.batch_size = batch_size
        self.discount_factor = discount_factor
        self.n_jobs = n_jobs
        self.seed = seed

        # Set an internal rng object
        self._rng = np.random.default_rng(self.seed)

    @property
    def sequences(self) -> List[List]:
        """Sequence
        The sequences of Seq2Pat.
        """
        return self._sequences

    def add_constraint(self, constraint: _BaseConstraint) -> _BaseConstraint:
        """Adds the given constraint to the constraint store.

        Parameters
        ----------
        constraint: _BaseConstraint
            A constraint on an attribute object

        Returns
        -------
        The constraint handle.

        Raises
        ------
        TypeError: If the constraint is already defined on this attribute.
        ValueError: If there is a mismatch in length of sequences and their attributes.

        """

        # Attribute and constraint id
        attr_id = constraint.attribute
        ct_id = constraint.__class__.__name__

        # Create the attribute field, if not created already
        if attr_id not in self.attr_to_cts:
            self.attr_to_cts[attr_id] = dict()

        # If the same constraint type exists on this attribute already, raise error
        if ct_id in self.attr_to_cts[attr_id]:
            raise TypeError(ct_id + " constraint is already defined on this attribute.")

        # Verify that attribute
        check_true(check_sequence_feature_same_length(self.sequences, constraint.attribute.values),
                   ValueError("Each sequence should match given attributes in event length."))

        # Add the constraint
        self.attr_to_cts[attr_id][ct_id] = constraint

        # Return constraint handle (so that one can remove it)
        return constraint

    def remove_constraint(self, constraint: _BaseConstraint) -> NoReturn:
        """Removes the given constraint from the constraint store.

        Parameters
        ----------
        constraint: _BaseConstraint
            A constraint on an attribute object

        Raises
        ------
        KeyError: If the given constraint does not exist in the constraint store.

        """

        # Attribute and constraint id
        attribute_id = constraint.attribute
        constraint_id = constraint.__class__.__name__

        try:
            # Remove the constraint from the attribute
            del self.attr_to_cts[attribute_id][constraint_id]

            # If no constraint left on the attribute, remove the attribute
            if len(self.attr_to_cts[attribute_id]) == 0:
                del self.attr_to_cts[attribute_id]

        except KeyError:
            raise KeyError("No " + constraint_id + " constraint to remove on this attribute.")

    def _run_thread(self, min_frequency, q):

        # Cython implementor object with input parameters set
        self._cython_imp = self._get_cython_imp(min_frequency)

        # Frequent mining
        q.put(self._cython_imp.mine())

    def get_patterns(self, min_frequency: Num) -> List[list]:
        """Performs the mining operation enforcing the constraints and returns the most frequent patterns.

        Parameters
        ----------
        min_frequency: Num
           If int, represents the minimum number of sequences (rows) a pattern should occur.
           If float, should be (0.0, 1.0] and represents
           the minimum percentage of sequences (rows) a pattern should occur.

        Returns
        -------
        Each inner list represents a frequent pattern in the form\
        [event_1, event_2, event_3, ... event_n, frequency].\
        The last element is the frequency of the pattern.\
        Sequences are sored by decreasing frequency, i.e., most frequent pattern first.
        """

        # Check num_rows
        check_true(self._num_rows >= 1, ValueError("Sequences should not be empty."))

        # Check min_frequency conditions
        # Given a set of `num_rows` sequences, we need to validate min_frequency.
        # In edge cases when min_frequency is not set properly, e.g. 0 or less than 1/num_rows, program will fail.
        validate_min_frequency(self._num_rows, min_frequency)

        if not self.batch_size:

            # Call Cython backend in a child process, write results to queue
            q = Queue()
            thread = Process(target=self._run_thread, args=(min_frequency, q))
            thread.start()

            # Get results from queue
            patterns = q.get()
            # Wait for process to finish and join the main process
            thread.join()

        else:
            # When min_frequency is an integer, convert to float before it is applied to batches
            if isinstance(min_frequency, int):
                min_frequency = float(min_frequency) / len(self.sequences)

            patterns = self._get_patterns_batch(min_frequency)

        # Map back to strings, if original is strings
        if self._is_string:
            patterns = int_to_string(self._int_to_str, patterns)

        # Sort sequences, most frequent pattern first
        patterns_sorted = sort_pattern(patterns)

        # Clean up memory
        gc.collect()

        # Return frequent sequences
        return patterns_sorted

    def _get_patterns_batch(self, min_frequency: float) -> List[list]:
        """Get patterns from each batch with a relaxed min_frequency threshold, then aggregate pattern frequencies
        by using the summation of frequencies from batches.

        Attributes
        ----------
        min_frequency: float
           Min_frequency should be a float in (0.0, 1.0] for batch processing.
           It represents the minimum percentage of sequences (rows) a pattern should occur.

        Returns
        -------
        List[list] where each inner list represents a frequent pattern in the form
        [event_1, event_2, event_3, ... event_n, frequency].
        """

        # Shuffle sequences uniformly to make each batch have similar pattern occurrences
        sequences, attr_to_cs = self._shuffle_data()

        # Get number of chunks
        n_sequences = len(sequences)
        num_chunks = n_sequences // self.batch_size
        if n_sequences % self.batch_size > 0:
            num_chunks += 1

        # Run Seq2Pat in parallel on each chunk, with a lower min_frequency threshold to get a larger set of patterns
        batch_patterns = Parallel(n_jobs=self.n_jobs, require='sharedmem')(
            delayed(self._mining_batch)(i, sequences, attr_to_cs, min_frequency)
            for i in range(0, num_chunks))

        # Aggregate patterns from each chunk over the counts and apply min_frequency threshold
        min_row_count = int(n_sequences * min_frequency)
        agg_patterns = aggregate_patterns(batch_patterns, min_row_count)

        return agg_patterns

    def _shuffle_data(self) -> Tuple[List[List], Dict[Attribute, Dict[str, _Constraint]]]:
        """Shuffle sequences and attributes before running seq2pat on batches.

        Returns
        -------
        shuffled_sequences: List[List]
            The shuffled sequences.
        shuffled_attr_to_cs: Dict[Attribute, Dict[str, _Constraint]]
            The shuffled constraints.
        """
        indices = list(range(len(self.sequences)))
        self._rng.shuffle(indices)

        shuffled_sequences = [self.sequences[i] for i in indices]
        shuffled_attr_to_cts = deepcopy(self.attr_to_cts)
        for attr in shuffled_attr_to_cts:
            for cs in shuffled_attr_to_cts[attr]:
                old_constraint = shuffled_attr_to_cts[attr][cs]
                new_constraint = deepcopy(old_constraint)
                shuffled_values = [old_constraint.attribute.values[i] for i in indices]
                new_constraint.attribute._set_values(shuffled_values)
                shuffled_attr_to_cts[attr][cs] = new_constraint

        return shuffled_sequences, shuffled_attr_to_cts

    def _mining_batch(self, chunk_ind: int, sequences: List[List], attr_to_cs: Dict[Attribute, Dict[str, _Constraint]],
                      min_frequency: float) -> List[List]:
        """Implementor of pattern mining on each batch

        Attributes
        ----------
        chunk_ind: int
           chunk index
        sequences: List[list]
           A list of sequences each with a list of events.
           The event values can be all strings or all integers.
        attr_to_cs: Dict[Attribute, Dict[str, _Constraint]]
        min_frequency: float
           Min_frequency should be a float in (0.0, 1.0] for batch processing
           It represents the minimum percentage of sequences (rows) a pattern should occur.

        Returns:
        -------
        List[list] where each inner list represents a frequent pattern in the form
        [event_1, event_2, event_3, ... event_n, frequency].
        The last element is the frequency of the pattern.
        Sequences are sored by decreasing frequency, i.e., most frequent pattern first.
        """

        # Get one batch of sequences
        batch_sequences = sequences[chunk_ind * self.batch_size:(chunk_ind + 1) * self.batch_size]

        # Create seq2pat instance for one batch
        batch_seq2pat = Seq2Pat(batch_sequences, max_span=None, batch_size=None)

        # Create constraints for one batch
        for attr in attr_to_cs:
            for cs in attr_to_cs[attr]:
                old_constraint = attr_to_cs[attr][cs]
                new_constraint = deepcopy(old_constraint)
                new_constraint.attribute._set_values(old_constraint.attribute.values[chunk_ind * self.batch_size:
                                                                                    (chunk_ind + 1) * self.batch_size])
                batch_seq2pat.add_constraint(new_constraint)

        # Reduce min_frequency to be min_frequency * discount_factor, 0 < discount_factor < 1
        adjusted_min_frequency = update_min_frequency(len(batch_sequences), min_frequency,
                                                      self.discount_factor)

        return batch_seq2pat.get_patterns(adjusted_min_frequency)

    def _get_cython_imp(self, min_frequency) -> stp.PySeq2pat:
        """Creates and populates a Cython PySeq2Pat object based on the user inputs
        by translating sequential attribute into their appropriate PySeq2Pat
        representation and setting them.
        :param min_frequency: the minimum number of sequences(rows) to observe the pattern
        :return: PySeq2Pat object with all the necessary inputs set
        """

        cython_imp = stp.PySeq2pat()

        # Dictionary to hold all parameters that need to be set in seq_to_pat more information about what each
        # parameter represents can be found under Constants declaration
        params = {_Constants.lgap: [], _Constants.ugap: [], _Constants.lavr: [], _Constants.uavr: [],
                  _Constants.lspn: [],
                  _Constants.uspn: [], _Constants.lmed: [], _Constants.umed: [], _Constants.ugapi: [],
                  _Constants.lgapi: [],
                  _Constants.uspni: [], _Constants.lspni: [], _Constants.uavri: [], _Constants.lavri: [],
                  _Constants.umedi: [], _Constants.lmedi: [], _Constants.num_minmax: [], _Constants.num_avr: [],
                  _Constants.num_med: [], _Constants.tot_gap: [], _Constants.tot_spn: [], _Constants.tot_avr: [],
                  _Constants.num_att: 0, _Constants.items: self.sequences, _Constants.attrs: [],
                  _Constants.M: self._max_num_columns, _Constants.N: self._num_rows, _Constants.L: self._max_value,
                  _Constants.max_attrs: [], _Constants.min_attrs: []}

        # Iterate through all attributes and constraint and build parameters required by seq_to_pat
        for attribute, constraints in self.attr_to_cts.items():

            params[_Constants.num_att] += 1

            params[_Constants.num_minmax].append(0)
            params[_Constants.num_avr].append(0)
            params[_Constants.num_med].append(0)

            params[_Constants.max_attrs].append(attribute._max)
            params[_Constants.min_attrs].append(attribute._min)
            params[_Constants.attrs].append(attribute.values)

            for constraint_type, constraint in constraints.items():

                if isinstance(constraint, _Constraint.Average):
                    self._update_average_params(params, constraint)

                if isinstance(constraint, _Constraint.Gap):
                    self._update_gap_params(params, constraint)

                if isinstance(constraint, _Constraint.Median):
                    self._update_median_params(params, constraint)

                if isinstance(constraint, _Constraint.Span):
                    self._update_span_params(params, constraint)

        # Given all the parameters, setup the c++ object through the intermediary cython seq_to_pat.pyx
        for constraint, value in params.items():
            # print(constraint, " ", value)
            setattr(cython_imp, constraint, value)

        # Set frequency as a row count or row percentage. 1.0 will be used as percentage.
        if isinstance(min_frequency, float) and min_frequency <= 1.0:
            cython_imp.theta = cython_imp.N * min_frequency
        else:
            cython_imp.theta = min_frequency

        return cython_imp

    @staticmethod
    def _update_average_params(params: dict, constraint: _Constraint.Average) -> NoReturn:
        """Updates average constraint inputs for C++ backend
        :param constraint: average constraint obj
        """

        # attribute id for attribute that a constraint will be enforced on
        att_id = params[_Constants.num_att] - 1
        params[_Constants.tot_avr].append(att_id)

        if constraint.has_lower_bound():
            params[_Constants.lavr].append(constraint.lower_bound)
            params[_Constants.lavri].append(att_id)
            params[_Constants.num_avr][-1] += 1

        if constraint.has_upper_bound():
            params[_Constants.uavr].append(constraint.upper_bound)
            params[_Constants.uavri].append(att_id)
            params[_Constants.num_avr][-1] += 1

    @staticmethod
    def _update_gap_params(params: dict, constraint: _Constraint.Gap) -> NoReturn:
        """Update gap constraint inputs for C++ backend
        :param constraint: gap constraint obj
        """
        # attribute id for attribute that a constraint will be enforced on
        att_id = params[_Constants.num_att] - 1
        params[_Constants.tot_gap].append(att_id)

        if constraint.has_lower_bound():
            params[_Constants.lgap].append(constraint.lower_bound)
            params[_Constants.lgapi].append(att_id)

        if constraint.has_upper_bound():
            params[_Constants.ugap].append(constraint.upper_bound)
            params[_Constants.ugapi].append(att_id)

    @staticmethod
    def _update_median_params(params: dict, constraint: _Constraint.Median) -> NoReturn:
        """Updates median constraint inputs for C++ backend
        :param constraint: median constraint obj
        """
        # attribute id for attribute that a constraint will be enforced on
        att_id = params[_Constants.num_att] - 1

        if constraint.has_lower_bound():
            params[_Constants.lmed].append(constraint.lower_bound)
            params[_Constants.lmedi].append(att_id)
            params[_Constants.num_med][-1] += 1

        if constraint.has_upper_bound():
            params[_Constants.umed].append(constraint.upper_bound)
            params[_Constants.umedi].append(att_id)
            params[_Constants.num_med][-1] += 1

    @staticmethod
    def _update_span_params(params: dict, constraint: _Constraint.Span) -> NoReturn:
        """Updates span constraint inputs for C++ backend
        :param constraint: span constraint obj
        """
        """attribute id for attribute that a constraint will be enforced on, we want att_id to start from zero but are 
        using the number of attribute so we simply start from one."""
        att_id = params[_Constants.num_att] - 1
        params[_Constants.tot_spn].append(att_id)

        if constraint.has_lower_bound():
            params[_Constants.lspn].append(constraint.lower_bound)
            params[_Constants.lspni].append(att_id)
            params[_Constants.num_minmax][-1] += 2

        if constraint.has_upper_bound():
            params[_Constants.uspn].append(constraint.upper_bound)
            params[_Constants.uspni].append(att_id)

    def __str__(self) -> str:
        """return human-readable string representation of the class
        """
        str = "\n\nSeq2Pat"
        for attribute, constraints in self.attr_to_cts.items():
            str += "\nConstraints of Attribute: " + repr(attribute)
            str += "\nConstraints: " + repr(constraints)
            for constraint_type, constraint in constraints.items():
                str += "\nConstraint: " + constraint_type + " " + repr(constraint)
                str += "\nLB: " + repr(constraint.lower_bound)
                str += "\nUB: " + repr(constraint.upper_bound)
        return str
