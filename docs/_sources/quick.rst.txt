.. _quick:

Quick Start 
===========

Constraint-based Sequential Pattern Mining

.. code-block:: python

    # Example to show how to find frequent sequential patterns
    # from a given sequence database subject to constraints
    from sequential.seq2pat import Seq2Pat, Attribute

    # Seq2Pat over 3 sequences
    seq2pat = Seq2Pat(sequences=[["A", "A", "B", "A", "D"],
                                 ["C", "B", "A"],
                                 ["C", "A", "C", "D"]])

    # Price attribute corresponding to each item
    price = Attribute(values=[[5, 5, 3, 8, 2],
                              [1, 3, 3],
                              [4, 5, 2, 1]])

    # Average price constraint
    seq2pat.add_constraint(3 <= price.average() <= 4)

    # Patterns that occur at least twice (A-D)
    patterns = seq2pat.get_patterns(min_frequency=2)

Dichotomic Pattern Mining

.. code-block:: python

    # Example to show how to run Dichotomic Pattern Mining
    # on sequences with positive and negative outcomes
    from sequential.seq2pat import Seq2Pat
    from sequential.pat2feat import Pat2Feat
    from sequential.dpm import dichotomic_pattern_mining, DichotomicAggregation

    # Create seq2pat model for positive sequences
    sequences_pos = [["A", "A", "B", "A", "D"]]
    seq2pat_pos = Seq2Pat(sequences=sequences_pos)

    # Create seq2pat model for negative sequences
    sequences_neg = [["C", "B", "A"], ["C", "A", "C", "D"]]
    seq2pat_neg = Seq2Pat(sequences=sequences_neg)

    # Run DPM to get mined patterns
    aggregation_to_patterns = dichotomic_pattern_mining(seq2pat_pos, seq2pat_neg,
                                                        min_frequency_pos=1,
                                                        min_frequency_neg=2)

    # DPM patterns with Union aggregation
    dpm_patterns = aggregation_to_patterns[DichotomicAggregation.union]

    # Encodings of all sequences
    sequences = sequences_pos + sequences_neg
    pat2feat = Pat2Feat()
    encodings = pat2feat.get_features(sequences, dpm_patterns,
                                      drop_pattern_frequency=False)
