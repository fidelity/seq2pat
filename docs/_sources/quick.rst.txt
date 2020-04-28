.. _quick:

Quick Start 
===========

.. code-block:: python

	# Example to show how to find frequent sequential patterns 
	# from a given sequence database subject to constraints
	from sequential.seq2pat import Seq2Pat, Attribute

	# Seq2Pat over 3 sequences
	seq2pat = Seq2Pat(sequences=[["A", "A", "B", "A", "D"],
	                            ["C", "B", "A"],
			            ["C", "A", "C", "D"]])

	# Price attribute corresponding to each event
	price = Attribute(values=[[5, 5, 3, 8, 2],
			          [1, 3, 3],
			          [4, 5, 2, 1]])

	# Average price constraint 
	seq2pat.add_constraint(3 <= price.average() <= 4)

	# Patterns that occur at least twice (A-D)
	patterns = seq2pat.get_patterns(min_frequency=2)
